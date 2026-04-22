from flask import Flask, send_from_directory, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Opportunity

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return send_from_directory(".", "admin.html")

@app.route("/<path:path>")
def files(path):
    return send_from_directory(".", path)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    if Admin.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Account already exists"}), 400

    user = Admin(
        fullname=data["fullname"],
        email=data["email"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = Admin.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    session["admin_id"] = user.id

    return jsonify({"message": "Login success"})


if __name__ == "__main__":
    app.run(debug=True)