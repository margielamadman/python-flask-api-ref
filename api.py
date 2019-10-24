'''
Nearly all code and explanations come from SOURCE.
I just made this repo for personal reference.
SOURCE: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

Designing a RESTful API
REST = REpresentational State Transfer
6 Design Rules of REST:
1. Client-Server:
    Server: offers a service
    Client: consumes the service
2. Stateless:
    Each request made by the client should include everything
    the server needs to complete the request.
    The server should not store info from one request and
    use it in another request.
3. Cacheable:
    The server must indicate to the client if requests can be cached or not.
4. Layered System:
    Communication between Client/Server should be standardized.
    This allows for proxies to be respond to the client,
    without the client having to do anything different.
5. Uniform Interface:
    Client/Serve comms must be uniform.
6. Code on Demand:
    Servers can provide executable code/scripts for clients
    to then execute. OPTIONAL.

What is a RESTful web service?
CORE CONCEPT: Resources!!!
    * All resources are accessible through a URI
    * The client sends requests to URI's via HTTP methods

HTTP Methods:
1. GET
    Obtain information about a resource
2. POST
    Create a new resource
3. PUT
    Update a resource
4. DELETE
    Delete a resource

Design:
* What are you resources?
    How will they be exposed and how will the different HTTP requests
    affect them?

Todo List Example:
* Choose a root URL to access the service.
    http://[hostname]/todo/api/v1.0/
    * We include the app name to seperate the service from others
    that could be running on the same system.
    * We include the version of the API to allow for making updates
    in the future without affecting applications that rely on the
    older versions.

* Choose the resources that will be exposed by this service:
    * GET http://[hostname]/todo/api/v1.0/tasks
        Retrieve a list of tasks
    * GET http://[hostname]/todo/api/v1.0/tasks/[task_id]
        Retrieve a list of tasks
    * POST http://[hostname]/todo/api/v1.0/tasks
        Create a new task
    * PUT http://[hostname]/todo/api/v1.0/tasks/[task_id]
        Update an existing task
    * DELETE http://[hostname]/todo/api/v1.0/tasks/[task_id]
        Delete a task

* Define your resource:
Our task will be:
    * id: unique identifier. Numeric type.
    * title: short desc. String type.
    * description: long desc. Text type.
    * done: task completetion state. Bool type.

* Make your routes
* Improve the interface:
    * When returning the list of tasks you should return the URI
    instead of the id, this makes it easier to make calls
    client side
        
'''
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

# Example task list
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
        # Replying with JSON data
        return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # Only accept JSON data
    if not request.json or not 'title' in request.json:
        abort(400) # Bad request
    task = {
        'id': tasks[-1]['id'] + 1, # id is the last task plus one
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201 # 201 means Created

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404) # Resource not found
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404) # task does not exist
    if not request.json:
        abort(400) # We only accept json
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

# This makes the error response more API friendly
@app.errorhandler(404)
def not_found(error):
    '''Custom handler for 404, return JSON'''
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    '''Custom handler for 400, return JSON'''
    return make_response(jsonify({'error': 'Bad request'}), 400)

# Return URIs in task list
def make_public_task(task):
    '''
    replace 'id' in task to be a URI that the client can call
    '''
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

if __name__ == "__main__":
    app.run(debug=True)
    