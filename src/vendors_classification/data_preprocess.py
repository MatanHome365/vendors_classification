from string import digits
import string
import spacy
from gensim.parsing.preprocessing import remove_stopwords

nlp = spacy.load("en_core_web_sm")
table = str.maketrans('', '', digits)
exclude = set(string.punctuation)


def _convert_to_lemma(text):
    """
    :param text: input text as string
    :return: input text as string after applying lemmatization
    """
    doc = nlp(text)
    text = ' '.join([token.lemma_ for token in doc])  # convert word to its original form
    return text


def clean(doc):
    """
    :param doc: input text
    :return: input text after cleaning: remove punctuation, numbers and stop words. Lower casing and Lemmatization.
    """
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    remove_numbers = punc_free.translate(table)
    stop_free = remove_stopwords(remove_numbers.lower())
    normalized = _convert_to_lemma(stop_free)
    normalized = normalized.replace('-PRON- ', '')
    return normalized


def combine_transrcribe_recogintion(row):
    objects = row['objects']
    text = row['text']
    return text + ' ' + objects