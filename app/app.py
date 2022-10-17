# coding: utf8
import os
import atexit
import datetime
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

app = Flask('app')

SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
engine = create_engine(SQLALCHEMY_DATABASE_URI, client_encoding = 'utf-8')
Session = sessionmaker(bind=engine)

Base = declarative_base()

atexit.register(lambda:engine.dispose())

class HttpError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

class Adv(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    a_text = Column(String, nullable=False, unique=True)
    pub_date = Column(DateTime, default=datetime.datetime.now)
    owner_adv = Column(String, nullable=False)

Base.metadata.create_all(engine)



@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.error_message

    })
    error.status_code = 400
    return response


class AdvView(MethodView):

    def get(self):
        with Session() as session:

            list_adv = [x.a_text for x in session.query(Adv.a_text).distinct()]

            return list_adv

    def post(self):
        json_data = request.json
        with Session() as session:
            adv = Adv(header=json_data['header'], a_text=json_data['a_text'], owner_adv=json_data['owner_adv'])
            session.add(adv)
            try:
                session.commit()
                return jsonify({
                    'id':adv.id,
                    'pub_date':adv.pub_date.isoformat()
                })
            except IntegrityError:
                raise HttpError(400, 'Advertisement exists')

    def delete(self):
        json_data = request.json

        with Session() as session:
            id = json_data['id']
            session.query(Adv).filter(Adv.id == id).delete()
            session.commit()
            return id


app.add_url_rule('/advertisement/', view_func=AdvView.as_view('create_adv'), methods = ['POST'])

app.add_url_rule("/advertisement/", view_func=AdvView.as_view("get_adv"), methods=["GET"])

app.add_url_rule("/advertisement/", view_func=AdvView.as_view("del_adv"), methods=["Delete"])


app.run(
    host ='0.0.0.0',
    port = '5000'
)



