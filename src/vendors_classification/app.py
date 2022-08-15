import logging
import lambda_function
import json

LOGGER = logging.getLogger(__name__)


def execute(data: dict):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info('event parameter: {}'.format(data))
    # print("Received event: " + json.dumps(event, indent=2))
    body = data
    print("Received body:  " + str(body))
    try:
        return lambda_function.lambda_handler(body)
    except Exception as e:
        logger.error(e)
        print(json.dumps({'error': str(e)}))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


if __name__ == '__main__':
    data = {
        "source_video_bucket_folder_path": "tenants/36921cf7-d2af-4acf-9107-1c07a88190c8/projects/1658693523328/",
        "queue_message_receipt_handle": "AQEBejEI+jPh3F4ANYIagqtRRMpk2Di0YOXx6HRKyMdQ6o5h1/xgfbKhRNBkrDxeKeZCSf+OCNe2ZyeDQm6k+9x4jyanCrYI/nYOSc1IWxL37cSwIINgGz41GBnWjqdVEjyaP8tnWWKg1ZRvotxsowFDkMjA4sPAbkpnmw9CN8yqA87D5eyt0zoWDT/H5X8vNx8hfdy1clGVpg0vICNeYq50j07pOtwafgaXsCGO6an9BCDhFFxJC2XQI928ASi/kPeeY1ZOqq1JathE50GNIZq+BqWm8ZaDkllcPcPtSAPOZDvAoXsCEpyUTpAiX8BMDC5Vb56Qm8iZJyOuYHAxilk9oZp/v/xw98uYUholAx+adx4P+3kq9ecZ1lCQH6xgzMq7BlcQCDjPrXos/iDlATgqwA==",
        "source_video_name": "1658693511934.mp4"
    }

    execute(data)