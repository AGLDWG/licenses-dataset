"""
Reads all the individual licenses files in licenses/ and joins them into one file called licenses.ttl
"""
import rdflib
from os import path
import os

licenses_folder = path.join(path.dirname(path.realpath(__file__)), 'licenses')

g = rdflib.Graph()
for f in os.listdir(licenses_folder):
    if path.isfile(path.join(licenses_folder, f)) and f != 'licenses.ttl':
        print('loading ' + str(f) + '... '),
        g.parse(os.path.join(licenses_folder, f), format='turtle')
        print('ok')

with open(path.join(licenses_folder, 'licenses.ttl'), 'w') as n:
    n.write(g.serialize(format='turtle').decode('utf-8'))
