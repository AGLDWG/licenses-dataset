"""
Reads all the individual _data files in _data/ and joins them into one file called licenses.ttl
"""
import rdflib
from os import path
import os

licenses_folder = path.dirname(path.realpath(__file__))  # this dir

g = rdflib.Graph()
for f in os.listdir(licenses_folder):
    if f.endswith('.ttl') and f != 'licenses.ttl':
        print('loading ' + str(f) + '... '),
        g.parse(os.path.join(licenses_folder, f), format='turtle')
        print(len(g))
    # print('ok')

# add ODRL ontology
g.parse(os.path.join(licenses_folder, 'ontologies', 'odrl22.ttl'), format='turtle')

with open(os.path.join(licenses_folder, 'licenses.ttl'), 'w') as n:
    n.write(g.serialize(format='turtle').decode('utf-8'))

print('made licenses.ttl')
