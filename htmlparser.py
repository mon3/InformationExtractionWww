# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk import pos_tag, ne_chunk
from urllib.request import urlopen


def get_nonfiltered_text(url):
    """
    Zwraca tekst po sanityzacji, ale bez filtracji.

    :param url: adres strony
    :returns: tekst strony po sanityzacji
    """
    html = urllib.request.urlopen(url).read()
    text = get_text_from_html(html)
    return text


def get_filtered_text(url, stemming=True):
    """
    Zwraca tekst strony po sanityzacji i filtracji.

    :param url: adres strony
    :returns: tekst strony po filtracji
    """
    text = get_nonfiltered_text(url)
    print("TEXT = ", text)
    filtered = filter_text(text, stemming)
    return " ".join(filtered)

def get_filtered_text_from_ds(text, stemming=True):
    """
    Zwraca tekst strony po sanityzacji i filtracji.

    :param url: adres strony
    :returns: tekst strony po filtracji
    """
    # text = get_nonfiltered_text(url)
    filtered = filter_text(text, stemming)
    return " ".join(filtered)

def get_link_text_length(html):
    """
    Zwraca długość tekstu w linkach i całego tekstu.

    :param html: kod html strony
    :returns: długość tekstu w linkach, długość całego tekstu
    """
    bs = BeautifulSoup(html, 'html.parser')
    # print(bs.prettify()) można podejrzeć zawartość strony

    links = bs.find_all('a')
    link_text = []
    for l in links:
        l_text = l.get_text()
        if l_text:
            link_text.append("".join([c for c in l_text if c.isalnum()]))
    link_text_length = get_list_elements_len(link_text)

    full_text = get_raw_text_from_html(html)

    full_text_length = len("".join([c for c in full_text if c.isalnum()]))
    return float(link_text_length), float(full_text_length)


def char_before(text, i):
    """
    Zwraca poprzedni znak względem indeksu.

    :param text: tekst
    :param i: indeks
    :returns: poprzedni znak lub pusty string
    """
    if i != 0:
        return text[i - 1]
    else:
        return ""


def break_on_upper(text):
    """
    Wstawia spacje przed dużymi literami.

    :param text: tekst
    :returns: poprawiony tekst
    """
    return [space_before_upper(c, char_before(text, i)) for i, c in
            enumerate(text)]


def space_before_upper(char, char_before):
    """
    Wstawia spację przed dużą literą, rozdzielając w ten sposób słowa,
    wyjątek - poprzedni znak też był dużą literą.

    :param char: znak
    :param char_before: poprzedni znak
    :returns: spacja + znak lub znak
    """
    if char.isupper() and not (
                        char_before.isupper() or char_before.isspace() or char_before == '"' or char_before == "'"):
        return " " + char
    else:
        return char


def sanitize_text(raw_text):
    """
    Dokonuje podstawowej sanityzacji tekstu.

    :param raw_text: tekst przed obróbką
    :returns: tekst po sanityzacji
    """
    lines = (line.strip() for line in raw_text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    text = '\n'.join(chunk for chunk in chunks if chunk)

    text = "".join(break_on_upper(text))

    return text


def get_text_from_html(html):
    """
    Zwraca tekst strony po sanityzacji.

    :param html: kod strony
    :returns: tekst
    """
    text = get_raw_text_from_html(html)
    text = sanitize_text(text)
    return text


def get_raw_text_from_html(html):
    """
    Wyciąga surowy tekst z html.

    :param html: kod strony
    :returns: tekst
    """
    bs = BeautifulSoup(html, 'html.parser')
    # wyrzuca elementy script oraz style
    for script in bs(["script", "style"]):
        script.extract()  # pozbywa się elementu script

    text = bs.get_text()
    bs = BeautifulSoup(text, 'html.parser')
    text = bs.get_text()
    return text


def filter_short(token):
    """
    Funkcja służąca do wycina krótkich słów i znaków o długości mniejszej niż 2.
    Na wejściu dostajemy tokeny, dla których sprawdzamy długość.

    :param token: token
    :returns: True jeśli dłuższe niż 1, False w.p.p.
    """
    if len(token) > 1:
        return True
    else:
        return False


def tokenize(text):
    """
    Dzieli tekst na tokeny - pojedyncze slowa.

    :param text: tekst
    :returns: lista tokenow
    """
    # Tokenizacja tekstu przy użyciu nltk
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    # print("TAGGED: ", tagged)

    #  ENTITY RECOGNITION
    # nie wyłapuje dat!
    # namedEnt = ne_chunk(tagged, binary=True)
    # rysuje zdanie z tagami i obiektami przypisanymi do klas (tak jak w
    # pracy odnośnie klasyfikacji stron konferencji)
    # namedEnt.draw()

    return tokens


def get_link_text_length(html):
    """
    Zwraca długość tekstu w linkach i całego tekstu.

    :param html: kod html strony
    :returns: długość tekstu w linkach, długość całego tekstu
    """
    bs = BeautifulSoup(html, 'html.parser').find('html')
    # print(bs.prettify())

    links = bs.find_all('a')
    link_text = []
    for l in links:
        l_text = l.get_text()
        if l_text:
            link_text.append("".join([c for c in l_text if c.isalnum()]))
    link_text_length = get_list_elements_len(link_text)

    full_text = get_raw_text_from_html(html)

    full_text_length = len("".join([c for c in full_text if c.isalnum()]))
    return float(link_text_length), float(full_text_length)


def get_list_elements_len(l):
    """
    Zwraca sumaryczną długość elementów listy.

    :param l: lista elementów
    :returns: sumaryczna długość
    """
    s = 0
    for e in l:
        s += len(e)
    return s


def filter_nonalnum(token):
    """
    Wycina znaki niealfanumeryczne ze słów.

    :param token: token
    :returns: token pozbawiony znaków niealfanumerycznych
    """
    return "".join([c for c in token if c.isalnum()])


def filter_text(text, stemming=True):
    """
    Filtruje tekst - dokonuje tokenizacji oraz opcjonalnie - stemmingu.

    :param text: tekst
    :param stemming: flaga, wskazująca na to, czy ma się odbyć stemming
    :returns: przefiltrowane tokeny
    """
    stop_words = set(stopwords.words('english'))

    word_tokens = tokenize(text)
    # print("TOKENIZED: ", [(t) for t in word_tokens])

    # word_tokens = [filter_nonalnum(t).lower() for t in word_tokens]
    word_tokens = [filter_nonalnum(t).lower() for t in word_tokens]

    if stemming:
        ps = SnowballStemmer("english")
        word_tokens = [ps.stem(plural) for plural in word_tokens]
    word_tokens = [word for word in word_tokens if not word in stop_words]
    word_tokens = filter(filter_short, word_tokens)
    return word_tokens


if __name__ == '__main__':
    # print
    # html_doc = urllib.request.urlopen('http://www.icitm.org/').read()  # print
    # zawartosci strony z listy kazdego agenta
    # print("zawartosc strony domowej: ", html)
    # html_text = get_text_from_html(html_doc)
    # print(html_text)


    # text = get_link_text_length(html_doc)
    # zwraca ze stemmingiem dla arg2 = True
    html = 'http://www.icitm.org/'
    # html = 'conferences-data/pagestorage-annotated/0/1.html'



    # html = open('conferences-data/pagestorage-annotated/0/1.html', 'r').read()
    # request = urllib.request(html)
    # request.add_header('Accept-Encoding', 'utf-8')
    # response = urlopen(request)
    #
    # soup = BeautifulSoup(response)
    text = get_filtered_text(html, False)
    print(text)