from flask_restful import reqparse, abort, Resource

from common import api, db
from constants import HttpStatus, EMPTY_JSON
from helpers import handle_bson

COLL_AUTHORS = 'authors'


author_parser = reqparse.RequestParser()
author_parser.add_argument('id', required=True)
author_parser.add_argument('firstName')
author_parser.add_argument('lastName')


class Author(Resource):
    @staticmethod
    def get(author_id):
        author = db[COLL_AUTHORS].find_one({'id': author_id})
        if author:
            return handle_bson(author), HttpStatus.OK
        else:
            abort(HttpStatus.NOT_FOUND, message='Author "{}" not found'.format(author_id))

    @staticmethod
    def delete(author_id):
        db[COLL_AUTHORS].remove({'id': author_id}, multi=False)
        return EMPTY_JSON, HttpStatus.NO_CONTENT

    @staticmethod
    def post():
        args = author_parser.parse_args()
        author = {
            'id': args.get('id'),
            'firstName': args.get('firstName'),
            'lastName': args.get('lastName')
        }

        if db[COLL_AUTHORS].find_one({'id': args.get('id')}) is None:
            db[COLL_AUTHORS].insert_one(author)
            return handle_bson(author), HttpStatus.CREATED
        else:
            return handle_bson(author), HttpStatus.CONFLICT

    @staticmethod
    def put(author_id):
        args = author_parser.parse_args()
        author = {
            'id': args.get('id'),
            'firstName': args.get('firstName'),
            'lastName': args.get('lastName')
        }
        db[COLL_AUTHORS].update_one({'id': author_id}, {'$set': author}, upsert=True)
        return handle_bson(author), HttpStatus.OK


class Authors(Resource):
    @staticmethod
    def get():
        authors = list(db[COLL_AUTHORS].find({}))
        return {'authors': handle_bson(authors)}, HttpStatus.OK


api.add_resource(Author, '/api/author', '/api/author/<author_id>')
api.add_resource(Authors, '/api/authors', '/api/authors/')


# @app.route('/api/authors', methods=['GET', 'POST'])
# def authors_handler():
#     with open('authors.json', 'r') as f:
#         authors = json.loads(f.read())
#
#     if request.method == 'POST':
#         new_author = request.form.to_dict()
#         if new_author.get('id'):
#             if new_author.get('id') in authors.values():
#                 # Update existing
#                 for author in authors:
#                     if author['id'] == new_author['id']:
#                         author.update(new_author)
#                         break
#             else:
#                 # Add new
#                 authors.append(new_author)
#
#         with open('authors.json', 'w') as f:
#             f.write(json.dumps(authors, indent=4, separators=(',', ': ')))
#
#     return Response(
#         json.dumps(authors),
#         mimetype='application/json',
#         headers={
#             'Cache-Control': 'no-cache',
#             'Access-Control-Allow-Origin': '*'
#         }
#     )
#
