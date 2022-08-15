import boto3
import os
import json
import time
import configuration as config
import data_preprocess as preprocessor
import model_predict

"""GLOBALS"""
LOCAL_FILES_DIR = '/tmp/'
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
runtime_sagemaker_client = boto3.client('runtime.sagemaker')
lambda_client = boto3.client('lambda')


def get_top_n_rekognition(rekognition_data_json, n=5):
    """
    :param rekognition_data_json: rekognition input from project video
    :param n: number of most common to return
    :return: list of n most common objects which exist in config.labels_to_keep
    """
    rekognition_unique_labels = {}
    for label in rekognition_data_json['Labels']:
        name = label['Label']['Name'].lower()
        if name not in config.labels_to_keep:
            continue
        if name in rekognition_unique_labels:
            rekognition_unique_labels[name] += 1
        else:
            rekognition_unique_labels[name] = 1
    temp_list = sorted(rekognition_unique_labels.items(), key=lambda x: x[1], reverse=True)[:n]
    return [x[0] for x in temp_list]


def lambda_handler(event):
    try:
        returnObj = lambda_main(event)
        ### RETURN ###
        return returnObj
    except:
        err_obj = json.dumps({
            'Event': event
        })
        print(f'[ERROR]: {err_obj}')
        raise


def lambda_main(event):
    ### ENVIRONMENT / EVENT ###
    ## Example: 'home365-frontdoorapp'
    BUCKET_NAME = os.environ['BUCKET_NAME']
    ## Example: ml_inference_queue_url = 'https://sqs.us-east-1.amazonaws.com/090922436798/Video-ML-Inference'
    ml_inference_queue_url = os.environ['ml_inference_queue_url']
    ## Example: source_video_bucket_folder_path = 'testmedia/0035378D-66DB-4B53-8E40-ADDCF1378AD0/1605434051/'
    source_video_bucket_folder_path = event['source_video_bucket_folder_path']
    queue_message_receipt_handle = event['queue_message_receipt_handle']
    ## Example: 'lambda_invoke-transcribe-rekognition/transcribe_file_output/'
    transcribe_bucket_output_folder_path = os.environ['transcribe_bucket_output_folder_path']
    ## Example: 'lambda_invoke-transcribe-rekognition/rekognition_file_output/'
    rekognition_bucket_output_folder_path = os.environ['rekognition_bucket_output_folder_path']
    ## Example: '1582349423.mp4'
    video_file = event['source_video_name']
    ## Example: 'projects-ai'
    endpoint_name = os.environ['endpoint_name']

    print(f'[INFO]: source_video_bucket_folder_path: {source_video_bucket_folder_path}')

    ### INITIALIZE VARS ###
    returnObj = {}
    bucket_resource = s3_resource.Bucket(BUCKET_NAME)
    video_file_path_string = '_'.join(source_video_bucket_folder_path.split('/'))

    ### GENERAL STRING MANIPULATION VARIABLES ###
    video_file_split = video_file.split('.')
    video_file_split.pop()
    video_file_base_name = '.'.join(video_file_split)

    ### RETRIEVING TRANSCRIBE OUTPUT FILE ###
    expected_output_file = os.path.join(transcribe_bucket_output_folder_path, video_file_path_string)
    print(f'[INFO]: Retrieving Transcribe output data with prefix: {expected_output_file}')
    try:
        objects = bucket_resource.objects.filter(Prefix=expected_output_file)
    except Exception:
        print('[INFO]: Waiting 30 sec for Transcribe Output...')
        time.sleep(30)
        objects = bucket_resource.objects.filter(Prefix=expected_output_file)
    if len(list(objects)) == 0:
        raise Exception(f'Missing Transcribe Output File...')
    print(
        f'[INFO]: Found existing transcribe output data for request. Request: "{source_video_bucket_folder_path}" Existing Data: "{list(objects)}"')
    for obj in objects:
        path, source_filename = os.path.split(obj.key)
        print(f'[INFO]: Path: {path} Filename: {source_filename}')
        transcribe_data = obj.get()['Body'].read()

    ### RETRIEVING REKOGNITION OUTPUT FILE ###
    expected_output_file = os.path.join(rekognition_bucket_output_folder_path, video_file_path_string)
    print(f'[INFO]: Retrieving Rekognition output data with prefix: {expected_output_file}')
    objects = bucket_resource.objects.filter(Prefix=expected_output_file)
    if len(list(objects)) == 0:
        raise Exception(f'Missing Rekognition Output File...')
    print(
        f'[INFO]: Found existing rekognition output data for request. Request: "{source_video_bucket_folder_path}" Existing Data: "{list(objects)}"')
    for obj in objects:
        path, source_filename = os.path.split(obj.key)
        print(f'[INFO]: Path: {path} Filename: {source_filename}')
        rekognition_data = obj.get()['Body'].read()

    ### TRANSCRIBE DATA LOAD ###
    transcription = json.loads(transcribe_data)['results']['transcripts'][0]['transcript']

    ### REKOGNITION DATA LOAD ###
    rekognition_data_json = json.loads(rekognition_data)
    rekognition_unique_labels = get_top_n_rekognition(rekognition_data_json)
    objects = ', '.join(rekognition_unique_labels)

    cleaned_text = preprocessor.clean(transcription)
    cleaned_objects = preprocessor.clean(objects)
    cleaned_input = cleaned_text + ' ' + cleaned_objects
    answer = model_predict.model_prediction(cleaned_text, cleaned_input)

    ### UPLOAD INFERENCE DATA TO S3 ###
    s3_client.put_object(
        Body=str(json.dumps(answer)),
        Bucket=BUCKET_NAME,
        Key=source_video_bucket_folder_path + video_file_base_name + '.prediction'
    )

    print(f'[INFO]: Deleting Message from Queue.')
    response = sqs_client.delete_message(
        QueueUrl=ml_inference_queue_url,
        ReceiptHandle=queue_message_receipt_handle
    )

    print(response)
    source_filename_for_lambda = source_filename.replace('_', '/')[:-5]
    print(f'[INFO]: Invoking AssignVendorInSQL Lambda for assign vendor for object: {source_filename_for_lambda}')
    payload = json.dumps({'source_key': source_filename_for_lambda})
    result = lambda_client.invoke(
        FunctionName='AssignVendorInSQL',
        InvocationType='Event',
        LogType='None',
        Payload=payload
    )

    ### RETURN ###
    return returnObj


# event = {
#     "source_video_bucket_folder_path": "tenants/36921cf7-d2af-4acf-9107-1c07a88190c8/projects/1658693523328/",
#     "queue_message_receipt_handle": "AQEBejEI+jPh3F4ANYIagqtRRMpk2Di0YOXx6HRKyMdQ6o5h1/xgfbKhRNBkrDxeKeZCSf+OCNe2ZyeDQm6k+9x4jyanCrYI/nYOSc1IWxL37cSwIINgGz41GBnWjqdVEjyaP8tnWWKg1ZRvotxsowFDkMjA4sPAbkpnmw9CN8yqA87D5eyt0zoWDT/H5X8vNx8hfdy1clGVpg0vICNeYq50j07pOtwafgaXsCGO6an9BCDhFFxJC2XQI928ASi/kPeeY1ZOqq1JathE50GNIZq+BqWm8ZaDkllcPcPtSAPOZDvAoXsCEpyUTpAiX8BMDC5Vb56Qm8iZJyOuYHAxilk9oZp/v/xw98uYUholAx+adx4P+3kq9ecZ1lCQH6xgzMq7BlcQCDjPrXos/iDlATgqwA==",
#     "source_video_name": "1658693511934.mp4"
# }
#
# lambda_handler(event, None)
