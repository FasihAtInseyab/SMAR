from flask.views import MethodView
from flask_smorest import Blueprint, abort
from utils import get_terms_openai
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import KeyTermGenModel
from schemas import KeytermGenSchema


blp = Blueprint("Keyterms", "keyterms", description="Operations on Keyterms")


@blp.route("/keyterm/generate")
class Keyterm(MethodView):
    # @jwt_required(fresh=True)
    @blp.arguments(KeytermGenSchema)
    @blp.response(201, KeytermGenSchema)
    def post(self, term_data):
        text = term_data['text']
        # terms = KeyTermGenModel.find_by_text(text)
        # if terms:
        #     return terms.json()

        key_terms = get_terms_openai(text=text.upper())
        terms = KeyTermGenModel(**term_data, keyterms=key_terms)

        try:
            terms.save_to_db()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="An error occurred while inserting the item.")

        return terms.json()