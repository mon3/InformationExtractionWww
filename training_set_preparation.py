from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag
from nltk import pos_tag
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import pycrfsuite
import os
from htmlparser import get_filtered_text_from_ds, get_filtered_text, \
    filter_nonalnum, tokenize, filter_short


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

    # soup = BeautifulSoup(html, 'html').find('html')
    soup = BeautifulSoup(html, 'html.parser').find('html')

    text = []
    text_tags = []
    get_text_and_tags_recursive(text, text_tags, soup, [])
    # print("TAGS = ", text_tags)
    # print("TEXT = ", text)

    # text_tokens = get_filtered_text_from_ds(text, True)
    # print(text_tokens)

    single_words = []
    classes = []

    for a in text_tags:
        # print("a = ", a) # list
        a = [x.lower() for x in a]

    # print("TAGS2 = ", text_tags)

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
    # print("DOCS = ", docs[0])
    # return single_words, classes
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

def prepare_crf_trainer(X_train, Y_train):
    trainer = pycrfsuite.Trainer(verbose=False)  # verbose = TRue wypisze
    # progres trenowania

    # Submit training data to the trainer
    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    # Set the parameters of the model
    trainer.set_params({
        # coefficient for L1 penalty
        'c1': 0.1,

        # coefficient for L2 penalty
        'c2': 0.01,

        # maximum number of iterations
        'max_iterations': 200,

        # whether to include transitions that
        # are possible, but not observed
        'feature.possible_transitions': True
    })

    # Provide a file name as a parameter to the train function, such that
    # the model will be saved to the file when training is finished
    trainer.train('crf.model')

def get_files(directory):
    import os

    # f = open("html_out.txt", 'a')
    #
    html_files = []
    for file in os.listdir(directory):
        # if (dir.endswith(".txt")==0):
        #     for file in os.listdir(os.path.join(directory, dir)):
            if file.endswith(".html"):
                html = open(os.path.join(directory, file),'r').read()
                # html = get_filtered_text_from_ds(html)
                # print(html)
                # f.write(html)
                html_files.append(html)
            # print(html_files[1])
    # f.close()

    return html_files


def tag_annotated(parent_folder):
    parent = parent_folder
    os.chdir(parent_folder)
    print(os.getcwd())


def split_text_to_entities(directory, file_nr):
    html = open(os.path.join(os.path.join(directory, "0"), file_nr), 'r').read()
    print(html)
    get_filtered_text(html, False)
    # html = get_filtered_text_from_ds(html)
    # print(html)

def test():
    html_files = get_files("conferences-data/pagestorage-annotated/0/")


    docs = []

    for i in range(len(html_files)):
        doc = get_classificated_text(html_files[i])
        # print(doc)
        docs.append(doc)

    # print(docs)

    data = []

    for j in docs:
        tokens = [t for t, label in doc]

        # Perform POS tagging
        tagged = pos_tag(tokens)

        # Take the word, POS tag, and its label
        data.append(
            [(w, pos, label) for (w, label), (word, pos) in
             zip(doc, tagged)])

    print(data)

    X = [extract_features(doc) for doc in data]
    y = [get_labels(doc) for doc in data]


    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
    print(len(X_train), len(X_test), len(Y_train), len(Y_test))

    print(X_train, X_test)
    prepare_crf_trainer(X_train, Y_train)
    #
    tagger = pycrfsuite.Tagger()
    tagger.open('crf.model')
    y_pred = [tagger.tag(xseq) for xseq in X_test]
    print(y_pred[-1], X_test[-1])

  # Let's take a look at a random sample in the testing set
  # i = 100

    # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
    #        print("%s (%s)" % (y, x))


if __name__== "__main__":

    test()
    # split_text_to_entities("conferences-data/pagestorage-annotated/", "0.html")


    # tag_annotated("conferences-data/pagestorage-annotated/")

    # html_files_content_whole = get_files(
    #     "conferences-data/pagestorage-annotated/")
    # # print(html_files_content_whole)


    # html = open('conferences-data/pagestorage-annotated/0/1.html', 'r').read()
    # print(html)
    # # f = open('all_html', 'w')
    # # f.write([str(i)for i in html_files_content_whole])
    # # f.close()
    # words, classes = get_classificated_text(html)
    # #
    # #
    # for word, word_class in zip(words, classes):
    #     if word_class != 'DIFF':
    #         print (word, word_class)
    #
    #
    # #
    # # docs = []
    # # f = open("html_out.txt", 'a')
    # #
    # for i in range(len(html_files_content_whole)):
    #     doc = get_classificated_text(html_files_content_whole[i])
    #     docs.append(doc)
    #     f.write(str(doc))
    # f.close()





        # for class_word in docs:
    #     for i in class_word:
    #         print(i)
    #
    # data = []
    # for j in docs:
    #     for i, doc in enumerate(j):
    #         # Obtain the list of tokens in the document
    #         tokens = [t for t, label in doc]
    #
    #         # Perform POS tagging
    #         tagged = pos_tag(tokens)
    #
    #         # Take the word, POS tag, and its label
    #         data.append(
    #             [(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])
    #
    # # print(data)
    #
    # X = [extract_features(doc) for doc in data]
    # y = [get_labels(doc) for doc in data]



    # print(X, y)
    # X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
    # prepare_crf_trainer(X_train, Y_train)
    #
    # tagger = pycrfsuite.Tagger()
    # tagger.open('crf.model')
    # y_pred = [tagger.tag(xseq) for xseq in X_test]
    # # print(y_pred[-1], X_test[-1])
    #
    # # Let's take a look at a random sample in the testing set
    # # i = 100
    # for x, y in zip(y_pred[i], [x[1].split("=")[1] for x in X_test[i]]):
    #     print("%s (%s)" % (y, x))