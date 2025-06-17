from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title="HOME")


@app.route('/allhardware')
def all_hardware():
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('SELECT hw_id, hw_name FROM Hardware;')
    hardwares = cur.fetchall()
    conn.close()
    return render_template("all_hardware.html", title="all_hardware", hardwares=hardwares)


@app.route('/hardware/<int:id>')
def hardware(id):
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Hardware;')
    hardwares = cur.fetchall()
    hardware = hardwares[id-1]
    conn.close()
    return render_template("hardware.html", title="hardware", id=id, hardware=hardware)


@app.route('/software')
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
