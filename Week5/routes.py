from flask import Blueprint, render_template, jsonify
main_bp = Blueprint('main',__name__) 

@main_bp.route('/')
def home():
    return render_template("main.html")

ops_bp = Blueprint("ops", __name__)
@ops_bp.get("/health")
def health():
    return jsonify(status="ok"), 200

