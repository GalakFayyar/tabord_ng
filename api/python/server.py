from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from logger import logger, configure

from resources.pharmacie import *

import json
import psycopg2
from psycopg2.extras import RealDictCursor
import json, hashlib

### Init controller routes manager
app = Flask(__name__)

### Load app config
conf = json.load(open('conf/api-conf.json'))

# Logger configuration
configure(conf['log']['level_values'][conf['log']['level']],
          conf['log']['dir'], conf['log']['filename'],
          conf['log']['max_filesize'], conf['log']['max_files'])

### Load app config into Flask WSGI running instance
app.config['CONF'] = conf
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['CORS_HEADERS'] = 'Auth-Token, Content-Type, User, Content-Length'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

url_prefix = conf['url_prefix']

### PostgreSQL configuration
app.config['DATABASE_USER'] = 'tom'
app.config['DATABASE_PASSWORD'] = 'tom'
app.config['DATABASE_DB'] = 'tabordng_dev'
app.config['DATABASE_HOST'] = 'localhost'

try:
    # Connection loading
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %( app.config['DATABASE_DB'], 
                                                                                app.config['DATABASE_USER'],
                                                                                app.config['DATABASE_HOST'],
                                                                                app.config['DATABASE_PASSWORD']))
    cursor = conn.cursor(cursor_factory=RealDictCursor)
except:
    print "ERREUR INITIALISATION ACCES DATABASE"

try:
    # Resources loading
    pharmacie_resource = Pharmacie(app, conn, cursor)
except:
    print "ERREUR INITIALISATION ACCES RESOURCES"

### Root REST API endpoint: display all available registered routes
@app.route(url_prefix + "/")
def index():
    logger.info("index")

    routes_tmp = {}
    for rule in app.url_map.iter_rules():
        urlhash = hashlib.md5() 
        urlhash.update((rule.rule).encode("utf8"))
        route = {
            'url' : rule.rule,
            'methods' : (routes_tmp[urlhash.hexdigest()]['methods']).union(rule.methods) if urlhash.hexdigest() in routes_tmp else rule.methods
        }
        routes_tmp[urlhash.hexdigest()] = route

    routes = []
    for k, r in routes_tmp.items():
        route = {
            "url": r['url'],
            "methods": list(r['methods'])
        }
        routes.append(route)

    return jsonify({"routes" : routes})

### heartbeat status
@app.route(url_prefix + "/heartbeat")
def hello():
    return "bim boum"

### retrieve api config
@app.route(url_prefix + "/conf")
def api_conf():
    return jsonify(app.config['CONF'])

@app.route(url_prefix + "/users")
def users():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    data = cursor.fetchall()
    if data is None:
        return "No data in 'utilisateurs'"
    else:
        list_returned_obj = []
        for col in data:
            obj = {
                'id': col[0],
                'username': col[1],
                'password': col[2]
            }
            list_returned_obj.append(obj)
        return jsonify({'data':list_returned_obj})

@app.route(url_prefix + "/authenticate", methods=['POST'])
def authenticate():
    print(request.json)

    username = request.json['username']
    password = request.json['password']

    sql = "SELECT * FROM utilisateurs WHERE username = '{}' AND password = '{}';".format(username, password)
    print(sql)

    cursor.execute(sql)
    data = cursor.fetchone()
    if data is None:
        return jsonify({'data':{'authenticated': False}})
    else:
        return jsonify({'data':{'authenticated': True, 'username': username}})

#TODO : export in class
@app.route(url_prefix + "/pharmacie/get_all", methods=['GET'])
def get_all_pharmacies():
    pharmacies = pharmacie_resource.get_all()
    return jsonify(pharmacies)

#TODO : export in class
@app.route(url_prefix + "/pharmacie/update", methods=['POST'])
def update_pharmacie():
    result = pharmacie_resource.update(request.json)
    return jsonify(result)

#TODO : export in class
@app.route(url_prefix + "/pharmacie/create", methods=['POST'])
def create_pharmacie():
    result = pharmacie_resource.create(request.json)
    return jsonify(result)

#TODO : export in class
@app.route(url_prefix + "/pharmacie/delete", methods=['POST'])
def delete_pharmacie():
    result = pharmacie_resource.delete(request.json)
    return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True)