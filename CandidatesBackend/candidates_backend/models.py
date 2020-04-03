from sqlalchemy import func
from candidates_backend.db import db


class CandidateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    name = db.Column(db.String(50))
    title = db.Column(db.String(250))
    location = db.Column(db.String(250))
    profile_url = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, server_default=func.now())