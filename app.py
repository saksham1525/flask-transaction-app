from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
import jwt
from datetime import datetime, timedelta
from functools import wraps

# 1. Create Flask app
app = Flask(__name__)

# 2. Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-key"
db = SQLAlchemy(app)

# 3. Define DB model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

# 4. Marshmallow schema
class TransactionSchema(Schema):
    description = fields.Str(required=True)
    amount = fields.Int(required=True)

schema = TransactionSchema()

# 5. Authentication
USERNAME = "admin"
PASSWORD = "password123"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            return f(*args, **kwargs)
        except:
            return jsonify({"message": "Invalid or missing token"}), 401
    return decorated

# 6. Routes
@app.route("/")
def home():
    return "Flask API is running"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") == USERNAME and data.get("password") == PASSWORD:
        token = jwt.encode({
            "user": USERNAME,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }, app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/transactions")
def get_transactions():
    all_txn = Transaction.query.all()
    result = [{"description": t.description, "amount": t.amount} for t in all_txn]
    return jsonify(result)

@app.route("/transactions", methods=["POST"])
@token_required
def add_transaction():
    # Validate incoming JSON data
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Create and save transaction
    txn = Transaction(description=data["description"], amount=data["amount"])
    db.session.add(txn)
    db.session.commit()
    return jsonify(data), 201

@app.route("/view")
def view_transactions():
    all_txn = Transaction.query.all()
    return render_template("index.html", transactions=all_txn)

# 7. Run
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
