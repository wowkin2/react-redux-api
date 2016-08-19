import json
import os
import time

from flask import Flask, Response, request

DIST_FOLDER = os.environ.get('REACTJS_DIST')


app = Flask(__name__, static_url_path='/static', static_folder=DIST_FOLDER+'dist')


@app.route('/api/courses', methods=['GET', 'POST'])
def courses_handler():
    with open('courses.json', 'r') as f:
        courses = json.loads(f.read())

    if request.method == 'POST':
        new_course = request.form.to_dict()
        if new_course.get('id'):
            if new_course.get('id') in courses.values():
                # Update existing
                for course in courses:
                    if course['id'] == new_course['id']:
                        course.update(new_course)
                        break
            else:
                # Add new
                courses.append(new_course)

        with open('courses.json', 'w') as f:
            f.write(json.dumps(courses, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(courses),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


@app.route('/api/authors', methods=['GET', 'POST'])
def authors_handler():
    with open('authors.json', 'r') as f:
        authors = json.loads(f.read())

    if request.method == 'POST':
        new_author = request.form.to_dict()
        if new_author.get('id'):
            if new_author.get('id') in authors.values():
                # Update existing
                for author in authors:
                    if author['id'] == new_author['id']:
                        author.update(new_author)
                        break
            else:
                # Add new
                authors.append(new_author)

        with open('authors.json', 'w') as f:
            f.write(json.dumps(authors, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(authors),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))
