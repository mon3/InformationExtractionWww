import xml.etree.ElementTree as etree
import re


def read_xml_http(path):
    """

    :param path: path to xml file with the structure containin name,
    abbreviation, date, place and url of the conference
    :return: dict defining the Conference class instance that should be added to owl
    """

    tree = etree.parse(path)
    root = tree.getroot()
    keys = ['name', 'abbreviation', 'date', 'place', 'url']
    onto_dict = dict(zip(keys, [None] * len(keys)))
    for child in root:
        if child.tag == "date" or child.tag == "abbreviation" or child.tag ==\
                'place' or child.tag == 'url':
            child_string = str(child.text)
            child_string = child_string.strip('\n')  # pozbywamy się znaków
            # nowej linii
            child_string = child_string.strip('\t')  # pozbywamy się tabulacji
            child_string = re.findall('\S+', child_string)  # znajdujemy
            # tylko wyrazy

            onto_dict[child.tag] = " ".join(child_string)
        elif child.tag == 'names':
            for child2 in child:
                if child2.tag == 'name':
                    child_string = str(child2.text)
                    child_string = child_string.strip('\n')
                    child_string = child_string.strip('\t')
                    child_string = re.findall('\S+', child_string)  # znajdujemy
            # tylko wyrazy
                    onto_dict[child2.tag] = " ".join(child_string)  # łączymy
                    #  listę w stringa ze spacją jako separator wyrazów

    return onto_dict


