from crypt import methods
import sqlite3
from turtle import title
from flask import Flask, jsonify, request

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("lands.db")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/sites", methods=['GET', 'POST'])
def sites():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        conn = cursor.execute("SELECT * FROM land")
        sites = [dict(id=row[0], owner=row[1], location=row[2], contacts=row[3])
                 for row in cursor.fetchall()
                 ]
        if sites is not None:
            return jsonify(sites)

    if request.method == 'POST':
        new_owner = request.form["owner"]
        new_location = request.form["location"]
        new_contacts = request.form["contacts"]

        sql = """INSERT INTO land (owner, location, contacts)
            VALUES(?,?,?)"""
        cursor = cursor.execute(sql, (new_owner, new_location, new_contacts))
        conn.commit()
        return f"land with the id {cursor.lastrowid} created successfully"


@app.route("/sites/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_site(id):
    conn = db_connection()
    cursor = conn.cursor()
    site = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM land WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            site = r
            if site is not None:
                return jsonify(site), 200
            else:
                return "something went wrong", 404
        
    if request.method == 'PUT':
        sql = """UPDATE land
                SET owner = ?
                    location = ?
                    contacts = ?
                WHERE id=?"""
        n_owner = request.form["owner"]
        n_location = request.form["location"]
        n_contacts = request.form["contacts"]
        
        updated_site ={
            "id": id,
            "owner":n_owner,
            "location":n_location,
            "contacts":n_contacts
        }
        cursor.execute(sql, (n_owner, n_location, n_contacts))
        conn.commit()
        return jsonify(updated_site)

    if request.method == 'DELETE':
        sql = """DELETE FROM land
                 WHERE id=?"""
        conn.execute(sql, (id,))
        conn.commit()
        return f"The site with the id{cursor.lastrowid} has been deleted"


if __name__ == "__main__":
    app.run(debug=True)
