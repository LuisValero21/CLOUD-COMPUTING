from flask import Flask, jsonify, request, abort
from users import users
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Mock database
directories = []
directory_id_counter = 1

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world"})

@app.route('/status/', methods=['GET'])
def status():
    return jsonify({"response": "pong"})

@app.route('/directories/', methods=['GET'])
def list_directories():
    count = len(directories)
    next_page = request.base_url + "?page=2" if count > 5 else None
    prev_page = None  # Mock pagination logic

    return jsonify({
        "count": count,
        "next": next_page,
        "previous": prev_page,
        "results": directories
    })

@app.route('/directories/', methods=['POST'])
def create_directory():
    global directory_id_counter
    if not request.json or 'name' not in request.json or 'emails' not in request.json:
        abort(400)
    
    directory = {
        "id": directory_id_counter,
        "name": request.json['name'],
        "emails": request.json['emails']
    }
    directories.append(directory)
    directory_id_counter += 1
    
    return jsonify(directory), 201

@app.route('/directories/<int:id>/', methods=['GET'])
def get_directory(id):
    directory = next((dir for dir in directories if dir['id'] == id), None)
    if directory is None:
        raise NotFound()
    return jsonify(directory)

@app.route('/directories/<int:id>/', methods=['PUT'])
def update_directory(id):
    directory = next((dir for dir in directories if dir['id'] == id), None)
    if directory is None:
        raise NotFound()
    
    if not request.json or 'name' not in request.json or 'emails' not in request.json:
        abort(400)
    
    directory['name'] = request.json['name']
    directory['emails'] = request.json['emails']
    
    return jsonify(directory)

@app.route('/directories/<int:id>/', methods=['PATCH'])
def partial_update_directory(id):
    directory = next((dir for dir in directories if dir['id'] == id), None)
    if directory is None:
        raise NotFound()

    if 'name' in request.json:
        directory['name'] = request.json['name']
    if 'emails' in request.json:
        directory['emails'] = request.json['emails']
    
    return jsonify(directory)

@app.route('/directories/<int:id>/', methods=['DELETE'])
def delete_directory(id):
    global directories
    directory = next((dir for dir in directories if dir['id'] == id), None)
    if directory is None:
        raise NotFound()
    
    directories = [dir for dir in directories if dir['id'] != id]
    
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
