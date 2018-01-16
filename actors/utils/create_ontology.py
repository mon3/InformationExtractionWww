from owlready import *

def run_onto(onto_dict):
    onto = get_ontology("file:///Users/paulina/Documents/WEDT/InformationExtractionWww/working_files/onto.owl")
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

    conf = Conference(onto_dict['NAME'])
    conf.has_abbreviation.append(Abbreviation(onto_dict['SHORT']))
    conf.has_year.append(Year(onto_dict['TIME']))
    conf.has_place.append(Place(onto_dict['PLACE']))

    onto.save()


