import os
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag
from glob import glob
from random import shuffle
from sklearn.model_selection import train_test_split

from actors.utils import htmlparser


def get_text_and_tags_recursive(text, textTags, currentSoup, currentTags):
    if type(currentSoup) == NavigableString:
        if len(currentSoup.split()) > 0:
            # print(currentSoup)
            text.append(currentSoup)
            textTags.append(currentTags[:])
    elif type(currentSoup) == Tag:
        currentTags.append(currentSoup.name)
        for tag in currentSoup.contents:
            get_text_and_tags_recursive(text, textTags, tag, currentTags)
        currentTags.pop()




def get_classificated_text(html):

    soup = BeautifulSoup(html, 'html.parser').find('html')

    text = []
    text_tags = []
    get_text_and_tags_recursive(text, text_tags, soup, [])

    single_words = []
    classes = []

    for a in text_tags:
        a = [x.lower() for x in a]

    docs = []
    for tag_text, tags in zip(text, text_tags):
        if 'cname' in tags:
            this_class = 'NAME'
        elif 'when' in tags:
            this_class = 'TIME'
        elif 'wher' in tags:
            this_class = 'PLACE'
        elif 'abbre' in tags:
            this_class = 'SHORT'
        else:
            this_class = "DIFF"

        classified_words = []
        for word in tag_text.split():
            # print("WORD in TAG_TEXT = ", word)
            single_words.append(word)
            classes.append(this_class)  # przypisujemy klasy do słów
            classified_words.append((word, this_class))

        docs.extend(classified_words)  # słowa z klasami

    return docs

def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]

    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    # Features for words that are not
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word.isdigit=%s' % word1.isdigit(),
            '+1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS')

    return features

# A function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]

# A function fo generating the list of labels for each document
def get_labels(doc):
    return [label for (token, postag, label) in doc]



def get_files(head_directory):

    html_file_names = [y for x in os.walk(head_directory) for y in glob(os.path.join(x[0], '*.html'))]
    html_file_names = set(html_file_names)

    html_files = []
    for file in html_file_names:
        html = open(file, 'r').read()
        html_files.append(html)

    #shuffle(html_files) !!!!!possible that we should be shuffling
    print("Number of html files: ", len(html_files))
    return html_files


def tag_annotated(parent_folder):
    parent = parent_folder
    os.chdir(parent_folder)
    print(os.getcwd())


def split_text_to_entities(directory, file_nr):
    html = open(os.path.join(os.path.join(directory, "0"), file_nr), 'r').read()
    print(html)
    htmlparser.get_filtered_text(html, False)


def prepare_training_data(docs_path):
    print("Starting preparation")
    html_files = get_files(docs_path)
    X, y = prepare_training_data_from_html(html_files)
    return train_test_split(X, y, test_size=0.2)

def prepare_training_data_from_html(html_files):
    from nltk import pos_tag
    docs = []

    for i in range(len(html_files)):
        if i%10 == 0:
            print(i)
        doc = get_classificated_text(html_files[i])
        docs.append(doc)

    print("Text parsed")
    data = []

    i = 0
    for doc in docs:
        i += 1
        if i % 10 == 0:
            print(i)

        tokens = [t for t, label in doc]

        # Perform POS tagging
        tagged = pos_tag(tokens)

        # Take the word, POS tag, and its label
        data.append(
            [(w, pos, label) for (w, label), (word, pos) in
             zip(doc, tagged)])

    print("Text tagged")

    X = [extract_features(doc) for doc in data]
    y = [get_labels(doc) for doc in data]
    return X, y


