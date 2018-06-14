import _config as conf
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace


def query(q):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_URI)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results["results"]["bindings"]


def total_policies():
    q = '''
    PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
    SELECT (COUNT(*) as ?count) WHERE {?s a odrl:Policy .}
    '''
    count = query(q)[0].get('count')
    if count is None:
        return None
    return int(count.get('value'))


def total_licenses():
    q = '''
    PREFIX cc: <http://creativecommons.org/ns#>
    SELECT (COUNT(*) as ?count) WHERE {?s a cc:License .}
    '''
    count = query(q)[0].get('count')
    if count is None:
        return None
    return int(count.get('value'))


def total_actions():
    q = '''
    PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
    SELECT (COUNT(*) as ?count) WHERE {?s a odrl:Action .}
    '''
    count = query(q)[0].get('count')
    if count is None:
        return None
    return int(count.get('value'))


def instance_details(uri):
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX opol: <http://linked.data.gov.au/def/odrl-policies#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT *
        WHERE {{
            {{
                <{0[uri]}>  rdfs:label ?label .
                OPTIONAL {{ <{0[uri]}> dct:created ?created . }}
            }}
            UNION  # to deal with sameAs declarations for short top-level register URIs like /license/ for individuals
            {{
                ?x owl:sameAs <{0[uri]}> .
                ?x  rdfs:label ?label .
                OPTIONAL {{ ?x dct:created ?created . }}            
            }}
        }}
    '''.format({'uri': uri})

    d = query(q)
    if d is None or len(d) < 1:
        return None

    d = d[0]
    deets = {
        'label': d.get('label').get('value'),
        'created': d.get('created').get('value') if d.get('created') else None,
    }
    return deets


# TODO: change to useing SPARQLWrapper
def query_turtle(sparql_query):
    import requests

    """Make a SPARQL query with turtle format response"""
    data = {'query': sparql_query, 'format': 'text/turtle'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    r = requests.post(conf.SPARQL_QUERY_URI, data=data, auth=auth, headers=headers, timeout=1)
    try:
        return r.content
    except Exception as e:
        raise


def object_describe(uri, rdf_format):
    q = 'DESCRIBE <{}>'.format(uri)
    # convert the result from the SPARQL query to turtle and back to tidy it up for viewing
    triples = query_turtle(q)
    if len(triples) < 1 or triples is None:
        return None
    g = Graph().parse(data=triples.decode('utf-8'), format='turtle')

    g.bind('odrl-policies', Namespace('http://linked.data.gov.au/def/odrl-policies#'))
    g.bind('dct', Namespace('http://purl.org/dc/terms/'))

    if rdf_format in ['application/rdf+json', 'application/json']:
        return g.serialize(format='json-ld')
    else:
        return g.serialize(format=rdf_format)


if __name__ == '__main__':
    print(total_actions())
