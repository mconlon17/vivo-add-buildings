#!/usr/bin/env/python
"""
    add-buildings.py -- From a data file consisting of UF buildings
    add missing buildings to VIVO

    Version 0.1 MC 2014-01-14
    --  works as expected
    Version 0.2 MC 2014-02-06
    --  code formatting

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.2"

__harvest_text__ = "Python Buildings " + __version__

from vivotools import vivo_sparql_query
from vivotools import get_vivo_uri
from vivotools import assert_resource_property
from vivotools import assert_data_property
from vivotools import update_data_property
from vivotools import read_csv
from vivotools import rdf_header
from vivotools import rdf_footer
from vivotools import get_vivo_value

from datetime import datetime

def make_building_dict(debug=False):
    """
    Extract all the buildings in VIVO and organize them into a dictionary
    keyed by building number value URI.
    """
    query = """
    SELECT ?uri ?number
    WHERE {
        ?uri a vivo:Building .
        ?uri ufVivo:buildingNumber ?number
    }"""
    result = vivo_sparql_query(query)
    building_dict = {}
    if 'results' in result and 'bindings' in result['results']:
        rows = result["results"]["bindings"]
    else:
        return building_dict
    if debug:
        print query
        if len(rows) >= 2:
            print rows[0],rows[1]
        elif len(rows) == 1:
            print rows[0]
    for row in rows:
        number = row['number']['value']
        uri = row['uri']['value']
        building_dict[number] = uri
    if debug:
        print building_dict.items()[1:3]
    return building_dict

def add_building(label, number):
    """
    Given a label and a number, add a building with the label and number
    """
    ardf = ""
    building_uri = get_vivo_uri()
    add = assert_data_property(building_uri, "rdfs:label", label)
    ardf = ardf + add
    add = assert_resource_property(building_uri, "rdf:type",
        "http://vivoweb.org/ontology/core#Building")
    ardf = ardf + add
    add = assert_data_property(building_uri, "ufVivo:buildingNumber",
                                   number)
    ardf = ardf + add
    add = assert_data_property(building_uri, "ufVivo:dateHarvested",
                                             datetime.now().isoformat())
    ardf = ardf + add
    add = assert_data_property(building_uri, "ufVivo:harvestedBy",
        __harvest_text__)
    ardf = ardf + add
    return [ardf, building_uri]

print datetime.now(), "Start"
print datetime.now(), "Make building dictionary"
building_dict = make_building_dict(debug=True)
print datetime.now(), "Building dictionary has ", len(building_dict), "entries"
print datetime.now(), "Read Building file"
campus = read_csv("main-campus.csv")
buildings = {}
for row in campus.values():
    buildings[row['BLDG']] = row
print datetime.now(), "Building file has ", len(buildings.items()), "entries"
print datetime.now(), "Begin processing"
ardf = rdf_header()
srdf = rdf_header()
building_found = 0
building_not_found = 0
building_not_in_uf_data = 0
all_numbers = buildings.keys()
for building_number in all_numbers:
    if building_number not in all_numbers:
        all_numbers.append(building_number)
for building_number in all_numbers:
    if building_number in building_dict and building_number in buildings:
        building_found = building_found + 1
        building_uri = building_dict[building_number]
        
        vivo_building_label = get_vivo_value(building_uri, "rdfs:label")
        [add, sub] = update_data_property(building_uri, "rdfs:label",
                                          vivo_building_label,
                                          buildings[building_number]['NAME'])
        ardf = ardf + add
        srdf = srdf + sub
        
        vivo_date_harvested = get_vivo_value(building_uri,
                                             "ufVivo:dateHarvested")
        [add, sub] = update_data_property(building_uri, "ufVivo:dateHarvested",
                                          vivo_date_harvested,
                                          datetime.now().isoformat())
        ardf = ardf + add
        srdf = srdf + sub
        
        vivo_harvested_by = get_vivo_value(building_uri, "ufVivo:harvestedBy")
        [add, sub] = update_data_property(building_uri, "ufVivo:harvestedBy",
                                          vivo_harvested_by,
                                          __harvest_text__)
        ardf = ardf + add
        srdf = srdf + sub
        
    elif building_number not in building_dict:
        building_not_found = building_not_found + 1
        [add, building_uri] = add_building(buildings[building_number]['NAME'],
                                           building_number)
        ardf = ardf + add
    else:
        building_not_in_uf_data = building_not_in_uf_data + 1

print datetime.now(), "Found = ", building_found
print datetime.now(), "Not Found in VIVO, will be added = ", building_not_found
print datetime.now(), "Not Found in UF data = ", building_not_in_uf_data
print datetime.now(), "Write files"
adrf = ardf + rdf_footer()
srdf = srdf + rdf_footer()
add_file = open("building_add.rdf", "w")
sub_file = open("building_sub.rdf", "w")
print >>add_file, adrf
print >>sub_file, srdf
add_file.close()
sub_file.close()
print datetime.now(), "Finished"
