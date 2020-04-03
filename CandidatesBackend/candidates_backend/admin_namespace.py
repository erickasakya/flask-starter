import http.client
from flask_restplus import Namespace, Resource
from candidates_backend.models import CandidateModel
from candidates_backend.db import db

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/candidates/<int:candidate_id>/')
class CandidatesDelete(Resource):

    @admin_namespace.doc('delete_candidate',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, candidate_id):
        '''
        Delete a candidate
        '''
        candidate = CandidateModel.query.get(candidate_id)
        if not candidate:
            # The candidate is not present
            return '', http.client.NO_CONTENT

        db.session.delete(candidate)
        db.session.commit()

        return '', http.client.NO_CONTENT
