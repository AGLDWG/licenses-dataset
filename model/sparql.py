import _config as conf
from SPARQLWrapper import SPARQLWrapper, JSON


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


if __name__ == '__main__':
    print(total_actions())
