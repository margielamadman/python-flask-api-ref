# python-flask-api-ref

___Simple task list___

> Nearly all code and explanations come from SOURCE.
> I just made this repo for personal reference.
> SOURCE: [Designing a RESTful API](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)

## Install

```bash
# Install dependencies
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Start
python api.py
```

## Example

```bash
# Get list of all tasks
curl -i http://localhost:5000/todo/api/v1.0/tasks

# Get single task
curl -i http://localhost:5000/todo/api/v1.0/tasks/2

# Create a task
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks

# Update a task
curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2

# Delete a task
curl -i -X DELETE http://localhost:5000/todo/api/v1.0/tasks/2
```
