from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF, CSV, TSV


def total_policies():
    return 12


def query_dummy():
    return [
        {
            'uri': {'value': 'http://fake.com'},
            'label': {'value': 'Fake'}
        }
    ]
