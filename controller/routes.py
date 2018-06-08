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
        return Response('_data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Boards')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
        SELECT ?uri ?label
        WHERE {{
            ?uri a odrl:Policy ;
                 rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    orgs = sparql.query(q)

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/policy/',
        'Register of Policies',
        'This contains all the items in this API, including general Policies, Licenses and so on.',
        register,
        ['http://www.w3.org/ns/odrl/2/Policy', 'http://creativecommons.org/ns#License'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/license/')
def licenses():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_licenses()
    if total is None:
        return Response('_data store is unreachable', status=500, mimetype='text/plain')

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX cc: <http://creativecommons.org/ns#>
        SELECT ?uri ?label
        WHERE {{
            ?uri a cc:License ;
                 rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(per_page, (page - 1) * per_page)
    register = []
    vocabs = sparql.query(q)

    for vocab in vocabs:
        o = str(vocab['uri']['value'])
        l = str(vocab['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/license/',
        'Register of Licenses',
        'This register contains Licenses.',
        register,
        ['http://creativecommons.org/ns#License'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/action/')
def actions():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_actions()
    if total is None:
        return Response('_data store is unreachable', status=500, mimetype='text/plain')

    # get list of Action URIs and labels from the triplestore, paginating
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
        SELECT * WHERE {{ 
        ?uri a odrl:Action ;
            rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
        '''.format(per_page, (page - 1) * per_page)
    actions = sparql.query(q)

    register = []
    for action in actions:
        o = str(action['uri']['value'])
        l = str(action['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/action/',
        'Register of Actions',
        'This register contains ODRL Actions.',
        register,
        ['http://www.w3.org/ns/odrl/2/'],
        total,
        super_register='http://localhost:5000/reg/',
    ).render()


@routes.route('/object')
def object():
    if request.args.get('uri') is not None and str(request.args.get('uri')).startswith('http'):
        uri = request.args.get('uri')
    else:
        return Response('You must supply the URI if a resource with ?uri=...', status=400, mimetype='text/plain')

    # declare the one auorg view for all the individuals in this API
    views = {
            'pol': View(
                'OdrlPolicy View',
                'A view of basic properties of main classes in the ODRL Policies Ontology',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/turtle',
                namespace='http://test.linked.data.gov.au/def/odrl-policies#'
            )
    }

    return OdrlPoliciesObjectRenderer(
        request,
        uri,
        'Named Individual',
        'An individual object from the ORDL Policies datase',
        views,
        'pol'
    ).render()


#
#   Functions
#
@routes.route('/function/login')
def login():
    return render_template('page_login.html')


@routes.route('/function/new-license')
def new_license():
    return 'Dummy Crete New License'


class OdrlPoliciesObjectRenderer(Renderer):
    def __init__(
            self,
            request,
            uri,
            label,
            comment,
            views,
            default_view_token
            ):
        super().__init__(
            request,
            uri,
            views,
            default_view_token
        )
        self.label = label
        self.comment = comment

    def render(self):
        if hasattr(self, 'vf_error'):
            return Response(self.vf_error, status=406, mimetype='text/plain')
        else:
            if self.view == 'alternates':
                return self._render_alternates_view()
            elif self.view == 'pol':
                return self._render_pol_view()

    def _render_pol_view(self):
        if self.format in Renderer.RDF_MIMETYPES:
            rdf = sparql.object_describe(self.uri, self.format)
            if rdf is None:
                return Response('No triples contain that URI as subject', status=404, mimetype='text/plain')
            else:
                return Response(rdf, mimetype=self.format)
        else:  # only the HTML format left
            deets = sparql.instance_details(self.uri)
            if deets is None:
                return Response('That URI yielded no data', status=404, mimetype='text/plain')
            else:
                return render_template(
                    'object.html',
                    deets=deets
                )
