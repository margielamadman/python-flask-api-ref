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

        
'''
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

# Example task list
# 'u' is for unicode strings
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
        # Replying with JSON data
        return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404) # Resource not found
    return jsonify({'task': task[0]})

# This makes the error response more API friendly
@app.errorhandler(404)
def not_found(error):
    '''Custom handler for 404, return JSON'''
    return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == "__main__":
    app.run(debug=True)
    