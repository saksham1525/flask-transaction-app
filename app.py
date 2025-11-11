from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError

# 1. Create Flask app
app = Flask(__name__)

# 2. Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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

# 5. Routes
@app.route("/")
def home():
    return "Flask API is running"

@app.route("/transactions")
def get_transactions():
    all_txn = Transaction.query.all()
    result = [{"description": t.description, "amount": t.amount} for t in all_txn]
    return jsonify(result)

@app.route("/transactions", methods=["POST"])
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

# 6. Run
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
