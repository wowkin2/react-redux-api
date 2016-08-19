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
        new_course['id'] = int(time.time() * 1000)
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))
