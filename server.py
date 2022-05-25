import sqlite3
import json
from flask import Flask, g, request, render_template

app = Flask(__name__)

DATABASE = 'tags.db'
ta
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection( exception ):
    db = getattr(g,'_database', None)
    if db is not None:
        db.close()

# Endpoint: www.x/totes 
# Use: returns json object containing all totes and their associated information
@app.route("/totes")
def get_totes():
    totes = []
    for tote in query_db("select * from totes"):
        totes.append(tote)
    return json.dumps(totes)

@app.route("/add", methods = ['GET','POST'])
def add_tote():
    if request.method == 'POST':
        warehouse = request.form['warehouse']
        tote_num = request.form['tote_num']
        physical_id = request.form['physical_id']
        thing_board_id = request.form['thing_board_id']
        
        query_db("insert into totes(warehouse,tote_num,physical_id,thing_board_id) values ({warehouse},{tote_num},{physical_id},{thing_board_id})".format(warehouse=warehouse,tote_num=tote_num,physical_id=physical_id,thing_board_id=thing_board_id))
        return render_template('add.html')
    if request.method == 'GET':
        return render_template('add.html')
