from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

#route for home
@app.route('/')
def home():
    return render_template("home.html", title="HOME")

#route for all hardware
@app.route('/allhardware')
def all_hardware():
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('SELECT hw_id, hw_name FROM Hardware;') 
    hardwares = cur.fetchall()
    conn.close()
    return render_template("all_hardware.html", title="all_hardware", hardwares=hardwares)

#route for specific hardware
@app.route('/hardware/<int:id>')
def hardware(id):
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Hardware;')
    hardwares = cur.fetchall() #fetch all hardware, creating a list of tuples
    hardware = hardwares[id-1] #since id starts from 1, subtract 1 to get the correct index
    conn.close()
    return render_template("hardware.html", title="hardware", id=id, hardware=hardware)

#route for specific hardware
@app.route('/software')
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
