from flask import Blueprint, request, render_template
from flask_paginate import Pagination
from model import sparql
from pyldapi import *
import _config as conf


routes = Blueprint('controller', __name__)


#
#   Pages
#
@routes.route('/')
def home():
    return render_template('page_home.html')


@routes.route('/about')
def about():
    return render_template('page_about.html')


#
#   Registers
#
@routes.route('/reg/')
def reg():
    return RegisterOfRegistersRenderer(
        request,
        'http://localhost:5000/',
        'Register of Registers',
        'The master register of this API',
        conf.APP_DIR + '/rofr.ttl'
    ).render()


@routes.route('/policy/')
def policies():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_policies()
    if total is None:
        return Response('data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Boards')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX auorg: <http://test.linked.data.gov.au/def/auorg#>
        SELECT ?uri ?label
        WHERE {{
            ?uri a auorg:Board ;
                 rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    orgs = sparql.query_dummy()

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/policy/',
        'Register of Policies',
        'This contains all the itesm in this API, including general Policies, Licenses and so on.',
        register,
        ['http://www.w3.org/ns/odrl/2/Policy', 'http://creativecommons.org/ns#License'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()
