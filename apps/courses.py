from flask_restful import reqparse, abort, Resource

from common import api, db
from constants import HttpStatus
from helpers import handle_bson

COLL_COURSES = 'courses'


course_parser = reqparse.RequestParser()
course_parser.add_argument('id', required=True)
course_parser.add_argument('title')
course_parser.add_argument('watchHref')
course_parser.add_argument('authorId')
course_parser.add_argument('category')
course_parser.add_argument('length')


class Course(Resource):
    @staticmethod
    def get(course_id):
        course = db[COLL_COURSES].find_one({id: course_id})
        if course:
            return handle_bson(course), HttpStatus.OK
        else:
            abort(HttpStatus.NOT_FOUND, message='Course "{}" not found'.format(course_id))

    @staticmethod
    def delete(course_id):
        db[COLL_COURSES].remove({id: course_id}, multi=False)
        return '', HttpStatus.NO_CONTENT

    @staticmethod
    def post():
        args = course_parser.parse_args()
        course = {
            'id': args.get('id'),
            'authorId': args.get('authorId'),
            'category': args.get('category'),
            'watchHref': args.get('watchHref'),
            'title': args.get('title'),
            'length': args.get('length'),
        }
        if db[COLL_COURSES].find_one({'id': args.get('id')}) is None:
            db[COLL_COURSES].insert_one(course)
            return handle_bson(course), HttpStatus.CREATED
        else:
            return handle_bson(course), HttpStatus.CONFLICT

    @staticmethod
    def put(course_id):
        args = course_parser.parse_args()
        course = {
            'id': args.get('id'),
            'authorId': args.get('authorId'),
            'category': args.get('category'),
            'watchHref': args.get('watchHref'),
            'title': args.get('title'),
            'length': args.get('length'),
        }
        db[COLL_COURSES].update_one({id: course_id}, course, upsert=True)
        return handle_bson(course), HttpStatus.OK


class Courses(Resource):
    @staticmethod
    def get():
        courses = list(db[COLL_COURSES].find({}))
        return {'courses': handle_bson(courses)}, HttpStatus.OK


api.add_resource(Course, '/api/course', '/api/course/<course_id>')
api.add_resource(Courses, '/api/courses', '/api/courses/')


# @app.route('/api/courses', methods=['GET', 'POST'])
# def courses_handler():
#     with open('courses.json', 'r') as f:
#         courses = json.loads(f.read())
#
#     if request.method == 'POST':
#         new_course = request.json
#         if new_course.get('id'):
#             if new_course.get('id') in [x['id'] for x in courses]:
#                 # Update existing
#                 for course in courses:
#                     if course['id'] == new_course['id']:
#                         course.update(new_course)
#                         break
#             else:
#                 # Add new
#                 courses.append(new_course)
#
#         with open('courses.json', 'w') as f:
#             f.write(json.dumps(courses, indent=4, separators=(',', ': ')))
#
#     return Response(
#         json.dumps(courses),
#         mimetype='application/json',
#         headers={
#             'Cache-Control': 'no-cache',
#             'Access-Control-Allow-Origin': '*'
#         }
#     )

