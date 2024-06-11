from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de directorio
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    emails = db.Column(db.ARRAY(db.String), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "emails": self.emails
        }

db.create_all()

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world"})

@app.route('/status/', methods=['GET'])
def status():
    return jsonify({"response": "pong"})

@app.route('/directories/', methods=['GET'])
def list_directories():
    directories = Directory.query.all()
    count = len(directories)
    next_page = None  # Implementa la lógica de paginación si es necesario
    prev_page = None  # Implementa la lógica de paginación si es necesario

    return jsonify({
        "count": count,
        "next": next_page,
        "previous": prev_page,
        "results": [directory.to_dict() for directory in directories]
    })

@app.route('/directories/', methods=['POST'])
def create_directory():
    if not request.json or 'name' not in request.json or 'emails' not in request.json:
        abort(400)
    
    directory = Directory(
        name=request.json['name'],
        emails=request.json['emails']
    )
    db.session.add(directory)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400)
    
    return jsonify(directory.to_dict()), 201

@app.route('/directories/<int:id>/', methods=['GET'])
def get_directory(id):
    directory = Directory.query.get_or_404(id)
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>/', methods=['PUT'])
def update_directory(id):
    directory = Directory.query.get_or_404(id)
    
    if not request.json or 'name' not in request.json or 'emails' not in request.json:
        abort(400)
    
    directory.name = request.json['name']
    directory.emails = request.json['emails']
    
    db.session.commit()
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>/', methods=['PATCH'])
def partial_update_directory(id):
    directory = Directory.query.get_or_404(id)

    if 'name' in request.json:
        directory.name = request.json['name']
    if 'emails' in request.json:
        directory.emails = request.json['emails']
    
    db.session.commit()
    return jsonify(directory.to_dict())

@app.route('/directories/<int:id>/', methods=['DELETE'])
def delete_directory(id):
    directory = Directory.query.get_or_404(id)
    db.session.delete(directory)
    db.session.commit()
    
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
