from flask import Blueprint, render_template, request, jsonify
from flask import current_app as app
from flask_login import login_required
from app.db import mongo

bp = Blueprint('dashboard', __name__)

page_number = 0

# Route for handling the home page logic
@bp.route('/dashboard')
@login_required
def dashboard():
    documents = []

    if mongo.mongo_db is None:
        mongo.init_mongo_db()

    return render_template('app/dashboard.html',
                           mongo_version = mongo.mongo_db_version,
                           collections = mongo.get_mongo_collections(),
                           documents = documents)

@bp.route('/datafilter', methods=['POST'])
@login_required
def datafilter():
    global page_number

    page_number = 0
    page_size = app.config['PAGE_SIZE']

    filter = request.form['filter']
    oid = (request.form['oid']).replace('#','')

    print('Dashboard Py - Received data for oid: ', oid)
    print('Dashboard Py - Received data for filter: ', filter)

    if mongo.mongo_db is None:
        mongo.init_mongo_db()

    doc_data = mongo.find_documents(filter, page_size, oid)
    total_doc_count = mongo.count_documents(filter)

    return jsonify({'total_doc_count': total_doc_count, 'doc_data': doc_data, 'page_number': page_number, 'page_size': page_size})


@bp.route('/datafilter_next', methods=['POST'])
@login_required
def datafilter_next():
    global page_number

    page_number += 1
    page_size = app.config['PAGE_SIZE']

    filter = request.form['filter']
    oid = (request.form['oid']).replace('#', '')

    print('Dashboard Py - Received data for oid: ', oid)
    print('Dashboard Py - Received data for filter: ', filter)

    if mongo.mongo_db is None:
        mongo.init_mongo_db()

    doc_data = mongo.find_documents(filter, page_size, oid)
    total_doc_count = mongo.count_documents(filter)

    return jsonify({'total_doc_count': total_doc_count, 'doc_data': doc_data, 'page_number': page_number, 'page_size': page_size})


@bp.route('/datafilter_previous', methods=['POST'])
@login_required
def datafilter_previous():
    global page_number

    page_number -= 1
    page_size = app.config['PAGE_SIZE']

    filter = request.form['filter']
    oid = (request.form['oid']).replace('#', '')

    print('Dashboard Py - Received data for oid: ', oid)
    print('Dashboard Py - Received data for filter: ', filter)

    if mongo.mongo_db is None:
        mongo.init_mongo_db()

    doc_data = mongo.find_documents(filter, page_size, oid)
    total_doc_count = mongo.count_documents(filter)

    return jsonify({'total_doc_count': total_doc_count, 'doc_data': doc_data, 'page_number': page_number, 'page_size': page_size})
