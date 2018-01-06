from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import Tag

def get_text_and_tags_recursive(text, textTags, currentSoup, currentTags):
    if type(currentSoup) == NavigableString:
        if len(currentSoup.split()) > 0:
            text.append(currentSoup)
            textTags.append(currentTags[:])
    elif type(currentSoup) == Tag:
        currentTags.append(currentSoup.name)
        for tag in currentSoup.contents:
            get_text_and_tags_recursive(text, textTags, tag, currentTags)
        currentTags.pop()



def get_classificated_text(html):

    soup = BeautifulSoup(html, 'html').find('html')
    text = []
    text_tags = []
    get_text_and_tags_recursive(text, text_tags, soup, [])

    single_words = []
    classes = []

    for a in text_tags:
        a = [x.lower() for x in a]

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

        for word in tag_text.split():
            single_words.append(word)
            classes.append(this_class)

    return single_words, classes



html = open('../conferences-data/pagestorage-annotated/0/1.html', 'r').read()
words, classes = get_classificated_text(html)

for word, word_class in zip(words, classes):
    if word_class != 'DIFF':
        print (word, word_class)