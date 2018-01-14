from owlready import *
from http_to_ontology import read_xml_http

def run_onto(path):
    # Skrypt powinien być odpalany wtedy, gdy chcemy utworzyć/zmodyfikować
    # ontologię

    onto = Ontology("http://conferences_wedt.org/onto.owl")
    onto_path.append(os.path.join(os.getcwd(), 'conf_ontology/'))
    # onto_path.append("/home/monikas/Desktop/studia/WEDT/project/conf_ontology/")
    # onto = get_ontology("file:/home/monikas/Desktop/studia/WEDT/project" \
    #                         "/conf_ontology/onto.owl")
    onto.load()

    class Conference(Thing):
        ontology = onto


    class Abbreviation(Thing):
        ontology = onto


    class has_abbreviation(Property):
        ontology = onto
        domain = [Conference]
        range = [Abbreviation]


    class is_abbreviation_of(Property):
        ontology = onto
        domain = [Abbreviation]
        range = [Conference]
        inverse_property = has_abbreviation


    class Year(Thing):
        ontology = onto


    class has_year(Property):
        ontology = onto
        domain = [Conference]
        range = [Year]


    class is_year_of(Property):
        ontology = onto
        domain = [Year]
        range = [Conference]
        inverse_property = has_year


    class Place(Thing):
        ontology = onto


    class has_place(Property):
        ontology = onto
        domain = [Conference]
        range = [Place]


    class is_place_of(Property):
        ontology = onto
        domain = [Place]
        range = [Conference]
        inverse_property = has_place


    class URL(Thing):
        ontology = onto


    class has_url(Property):
        ontology = onto
        domain = [Conference]
        range = [URL]


    class is_url_of(Property):
        ontology = onto
        domain = [URL]
        range = [Conference]
        inverse_property = has_url

    # ################################################################
    # dla plików xml z korpusu conferences-data
    # for i in range(1000):
    #     if (os.path.exists('/home/monikas/Desktop/studia/WEDT/project'
    #                           '/conferences-data'
    #                   '/pagestorage-annotated/'+str(i)+'/conferenceData.xml')):
    #         onto_dict = read_xml_http('/home/monikas/Desktop/studia/WEDT/project'
    #                           '/conferences-data'
    #                   '/pagestorage-annotated/'+str(i)+'/conferenceData.xml')
    #
    #         conf = Conference(onto_dict['name'])
    #         conf.has_abbreviation.append(Abbreviation(onto_dict['abbreviation']))
    #         conf.has_year.append(Year(onto_dict['date']))
    #         conf.has_place.append(Place(onto_dict['place']))
    #         conf.has_url.append(URL(onto_dict['uri']))

    # #################################################################
    # dla pojedynczego pliku
    if os.path.exists(path):
        onto_dict = read_xml_http(path)
        conf = Conference(onto_dict['name'])
        conf.has_abbreviation.append(Abbreviation(onto_dict['abbreviation']))
        conf.has_year.append(Year(onto_dict['date']))
        conf.has_place.append(Place(onto_dict['place']))
        conf.has_url.append(URL(onto_dict['url']))


    # print(my_conf.has_abbreviation)
    # print(Place("Germany").is_place_of)
    onto.save()


if __name__ == "__main__":
    xml_path = os.path.join(os.getcwd(), 'conferences-data' \
            '/pagestorage-annotated/0/conferenceData.xml')
    run_onto(xml_path)
