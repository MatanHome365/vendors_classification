import configuration as config
import nltk
import pickle
import boto3.session

s3_client = boto3.client('s3')

'''loading models and vectorizers'''
response = s3_client.get_object(Bucket=config.bucket_name, Key=config.model_plumber_s3_address)
body = response['Body'].read()
model_plumber = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.vect_plumber_s3_address)
body = response['Body'].read()
vect_plumber = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.model_hvac_s3_address)
body = response['Body'].read()
model_hvac = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.vect_hvac_s3_address)
body = response['Body'].read()
vect_hvac = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.model_exterminator_s3_address)
body = response['Body'].read()
model_exterminator = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.vect_exterminator_s3_address)
body = response['Body'].read()
vect_exterminator = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.model_appliance_s3_address)
body = response['Body'].read()
model_appliance_installer = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.vect_appliance_s3_address)
body = response['Body'].read()
vect_appliance_installer = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.model_pool_s3_address)
body = response['Body'].read()
model_pool = pickle.loads(body)

response = s3_client.get_object(Bucket=config.bucket_name, Key=config.vect_pool_s3_address)
body = response['Body'].read()
vect_pool = pickle.loads(body)


def check_category_assignment_bigram(_input, features):
    """
    :param _input: transcribe text
    :param features: words represent category in bi-gram format
    :return: True if to assign category according to big-ram features, otherwise return False
    """
    words_list = _input.split(' ')
    bi_grams = nltk.ngrams(words_list, 2)

    for w in bi_grams:
        temp = w[0] + ' ' + w[1]
        if temp in features:
            return True
    return False


def gardener_check_assignment(_input, features):
    """
    :param _input: transcribe text
    :param features: words represent gardener category
    :return: 1 if to assign gardener category according to features, otherwise return 0
    """
    words_list = _input.split(' ')

    for w in features:
        if w in words_list:
            return 1
    return 0


def carpet_check_assignment(_input, features):
    """
    :param _input: transcribe text
    :param features: words represent carpet cleaner category
    :return: 1 if to assign carpet cleaner category according to features, otherwise return 0
    """
    words_list = _input.split(' ')
    for w in features:
        if w in words_list and check_category_assignment_manual(_input, config.clean_features) == 1:
            return 1
    return 0


def check_category_assignment_manual(_input, features):
    """
    :param _input: transcribe text
    :param features: words represent general category
    :return: 1 if to assign general category according to features, otherwise return 0
    """
    words_list = _input.split(' ')
    for w in features:
        if w in words_list:
            return 1
    return 0


def check_category_assignment(vectorizer, model, _input):
    """
    :param vectorizer: saved vectorizer for specific model
    :param model: saved model classification of specific category
    :param _input: transcribe chained with rekogintion
    :return: probability for choose category from 0 to 1
    """
    test_data_features = vectorizer.transform(_input)
    prob = model.predict_proba(test_data_features)[0][1]
    return prob


def get_chosen_category_from_vector(vector):
    """
    :param vector: vector which his cells represent chosen category (1) or not (0)
    :return: the first chosen category from left to right
    """
    for i, value in enumerate(vector):
        if value == 1:
            return config.index_categories[i]


def check_big_categories(text, _input):
    """
    :param text: transcribe text
    :param _input: transcribe chained with rekogintion
    :return: probability and chosen category name only if probability is greater or equals from thresh, otherwise return
     None, None
    """
    prob = None
    default_prob = 0.8

    prob = check_category_assignment(vect_appliance_installer, model_appliance_installer, _input)
    if prob >= config.thresh:
        return prob, config.appliance_name

    prob = check_category_assignment(vect_hvac, model_hvac, _input)
    if prob >= config.thresh:
        return prob, config.hvac_name

    prob = check_category_assignment(vect_exterminator, model_exterminator, _input)
    if prob >= config.thresh:
        return prob, config.exterminator_name

    prob = check_category_assignment(vect_pool, model_pool, _input)
    if prob >= config.thresh:
        return prob, config.pool_name

    if check_category_assignment_bigram(text, config.water_heater_features):
        return default_prob, config.plumber_water_heater_name

    prob = check_category_assignment(vect_plumber, model_plumber, _input)
    if prob >= config.thresh:
        return prob, config.plumber_name

    if check_category_assignment_manual(text, config.garage_features):
        return default_prob, config.garage_name

    return None, None


def model_prediction(text, _input):
    """

    :param text:
    :param _input:
    :return:
    """
    prediction, prob = check_big_categories(text, [_input])

    if prediction is not None:
        return {'best': prediction, 'probabilites': {prediction: prob}}

    else:
        default_prob = 0.8
        vector = [0, 0, 0, 0, 0, 0, 0, 0]
        vector[config.categories_index[config.mold_name]] = check_category_assignment_manual(text, config.mold_remediation_features)
        vector[config.categories_index[config.locksmith_name]] = check_category_assignment_manual(text, config.locksmith_features)
        vector[config.categories_index[config.painter_name]] = check_category_assignment_manual(text, config.painter_features)
        vector[config.categories_index[config.electrician_name]] = check_category_assignment_manual(text, config.electrician_features)
        vector[config.categories_index[config.carpet_name]] = carpet_check_assignment(text, config.carpet_cleaner_features)
        vector[config.categories_index[config.cleaner_name]] = check_category_assignment_manual(text, config.clean_features)
        vector[config.categories_index[config.gardener_name]] = gardener_check_assignment(text, config.garden_features)
        vector[config.categories_index[config.roofer_name]] = check_category_assignment_manual(text, config.roofer_features)

        sum_vector = sum(vector)
        if vector[config.categories_index[config.carpet_name]] == 1 and vector[config.categories_index[config.cleaner_name]] == 1:
            sum_vector -= 1
        if sum_vector == 0 or sum_vector > config.contractor_thresh:
            return {'best': config.contractor_name, 'probabilites': {config.contractor_name: default_prob}}
        else:
            prediction = get_chosen_category_from_vector(vector)
            return {'best': prediction, 'probabilites': {prediction: default_prob}}