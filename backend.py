from connection import create_connection
from connection import execute_query
from connection import execute_read_query
import flask
from flask import jsonify
from flask import request, make_response
import hashlib


#creating connection to mysql database
conn = create_connection("vacation.cnx4hijamlfr.us-east-1.rds.amazonaws.com", "admin", "randompassword", "vacation")

app = flask.Flask(__name__)   # sets up application
app.config["DEBUG"] = True    # shows error in browser


masterPassword = "cdb1fe708523643b04ff5479726edd67a4d26c3ccbb87a98c457e4dc31e7d48f"

@app.route('/authenticatedroute', methods=['GET'])
def auth_example():

    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == 'admin' and hashedResult.hexdigest() == masterPassword:
            return '<h1> LOGIN SUCCESSFUL! </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


#homepage
@app.route('/', methods=["GET"])
def homepage():
    return "<h1> Welcome to our final project </h1>"


#show all destinations from the destination table
@app.route('/destination/all', methods=['GET'])
def show_all():
    query = "SELECT * FROM destination"
    destinations = execute_read_query(conn, query)
    results = []
    for line in destinations:
        results.append(line)

    return jsonify(results)


# will be showing a destination based on an input ID, if no ID is input then message will occur
# endpoint to get a single destination by id http://127.0.0.1:5000/api/destination?1d=1
@app.route('/destination', methods=["GET"])
def show_destination():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'

    sql = "SELECT * FROM destination"
    destinations = execute_read_query(conn, sql)
    results = []
    for destination in destinations:
        if destination['id'] == id:
            results.append(destination)
    return jsonify(results)

# add a new destination fields to the destination table
@app.route('/destination', methods=["POST"])
def add_destination():
    request_data = request.get_json()
    newcountry = request_data['country']
    newcity = request_data['city']
    newsights = request_data['sightseeing']

    #lines below est connect to DB and use query on how to insert destinations into table
    query = "INSERT INTO destination (country, city, sightseeing) VALUES ('" +newcountry+ "','" +newcity+ "', '" +newsights+ "')"

    sql = "SELECT * FROM destination"
    execute_query(conn, query)
    destinations = execute_read_query(conn, sql)
    results = []
    for destination in destinations:
        results.append(destination)
    return jsonify(results)


#delete a destination from the table
@app.route('/destination', methods=["DELETE"])
def delete_des():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'
    sql = "DELETE FROM destination WHERE id= '%s'" % (id)
    execute_query(conn, sql)

    return 'Destination deleted!'


#this function will take the input from api the and update the exisiting fields with the db destination table
@app.route('/destination', methods=['PUT'])
def update_destination():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'
    request_data = request.get_json()
    update_country = request_data['country']
    update_city = request_data['city']
    update_sights = request_data['sightseeing']
    # update query that updates the destination table by ID
    query = "UPDATE destination SET country = '"+update_country+"', city = '"+update_city+"', sightseeing = '"+update_sights+"' WHERE id= '%s'" % id
    execute_query(conn, query)

    return 'Query updated!'


# shows all the trips
@app.route('/trip/all', methods=['GET'])
def show_all_trips():
    query = "SELECT transportation, startdate, enddate FROM trip "
    trips = execute_read_query(conn, query)
    # used execute read query to execute and return the query so it can be appended to results list
    results = []
    # for loop to append each line to the results variable
    for line in trips:
        results.append(line)

    return jsonify(results)


#shows the trip based on the request ID
@app.route('/trip', methods=['GET'])
def show_trips():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'

    sql = "SELECT * FROM trip"
    trips = execute_read_query(conn, sql)
    # used execute read query to execute and return the query
    # list to show the specified requested ID
    results = []
    for trip in trips:
        if trip['id'] == id:
            results.append(trip)
    return jsonify(results)

# adds all the new destination data taken from the API into the table
@app.route('/trip', methods=["POST"])
def add_trip():
    request_data = request.get_json()
    did = int(request_data['destination_id'])
    new_transp = request_data['transportation']
    new_startdate = request_data['startdate']
    new_enddate = request_data['enddate']
    new_tripname = request_data['tripname']

    query = "INSERT INTO trip (destination_id, transportation, startdate, enddate, tripname) VALUES ('%s', '%s', '%s', '%s', '%s')" % (did, new_transp, new_startdate, new_enddate, new_tripname)

    sql = "SELECT * FROM trip"
    execute_query(conn, query)
    trips = execute_read_query(conn, sql)
    # transfers the results from the trips to the results variable
    results = []
    # for loop to append each line to the results list
    for trip in trips:
        results.append(trip)
    return jsonify(results)


# delete a trip from the trip table by id
@app.route('/trip', methods=["DELETE"])
def delete_trip():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'
    sql = "DELETE FROM trip WHERE id= '%s'" % (id)
    execute_query(conn, sql)

    return 'Trip deleted!'

# updates the trip table in the DB with the new fields taken from the API
@app.route('/trip', methods=['PUT'])
def update_trip():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error no ID provided!'    # returns this error if no ID is provided
    request_data = request.get_json()
    update_dID = int(request_data['destination_id'])
    update_transp = request_data['transportation']
    update_sdate = request_data['startdate']
    update_edate = request_data['enddate']
    update_tname = request_data['tripname']
    # update query used to update the trip table
    query = "UPDATE trip SET destination_id = '%s', transportation = '%s', startdate = '%s', enddate = '%s', tripname = '%s' WHERE id= '%s'" % (update_dID, update_transp, update_sdate, update_edate, update_tname, id)
    execute_query(conn, query)

    return 'Query updated!'


app.run()
