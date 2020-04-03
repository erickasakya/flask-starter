import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from candidates_backend import config
from candidates_backend.models import CandidateModel
from candidates_backend.token_validation import validate_token_header
from candidates_backend.db import db
from flask import abort

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for Candidate

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

candidate_parser = authentication_parser.copy()
candidate_parser.add_argument('name', type=str, required=True,
                            help='Name of the candidate')
candidate_parser.add_argument('title', type=str, required=True,
                            help='Title of the candidate')
candidate_parser.add_argument('location', type=str, required=True,
                            help='Location of the candidate')
candidate_parser.add_argument('profile_url', type=str, required=True,
                            help='Profile URL of the candidate')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'name': fields.String(),
    'title': fields.String,
    'location': fields.String(),
    'profile_url': fields.String(),
    'timestamp': fields.DateTime(),
}
candidate_model = api_namespace.model('Candidate', model)


@api_namespace.route('/me/candidates/')
class MeCandidatesListCreate(Resource):

    @api_namespace.doc('list_candidates')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(candidate_model, as_list=True)
    def get(self):
        '''
        Retrieves all the candidates
        '''
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        candidates = (CandidateModel
                    .query
                    .filter(CandidateModel.username == username)
                    .order_by('id')
                    .all())
        return candidates

    @api_namespace.doc('create_candidate')
    @api_namespace.expect(candidate_parser)
    @api_namespace.marshal_with(candidate_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new candidate
        '''
        args = candidate_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_candidate = CandidateModel(username=username,
                                       name=args['name'],
                                       title=args['title'],
                                       location=args['location'],
                                       profile_url=args['profile_url'],
                                       timestamp=datetime.utcnow())
        db.session.add(new_candidate)
        db.session.commit()

        result = api_namespace.marshal(new_candidate, candidate_model)

        return result, http.client.CREATED


search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                           help='Search in the name of the candidates')


@api_namespace.route('/candidates/')
class CandidateList(Resource):

    @api_namespace.doc('list_candidates')
    @api_namespace.marshal_with(candidate_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        '''
        Retrieves all the candidates
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = CandidateModel.query
        if search_param:
            query = (query.filter(CandidateModel.name.contains(search_param)))

        query = query.order_by('id')
        candidates = query.all()

        return candidates


@api_namespace.route('/candidates/<int:candidate_id>/')
class CandidatesRetrieve(Resource):

    @api_namespace.doc('retrieve_candidate')
    @api_namespace.marshal_with(candidate_model)
    def get(self, candidate_id):
        '''
        Retrieve a candidate
        '''
        candidate = CandidateModel.query.get(candidate_id)
        if not candidate:
            # The candidate is not present
            return '', http.client.NOT_FOUND

        return candidate
