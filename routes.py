from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

#route for home
@app.route('/')
#define function home()
def home():
    return render_template("home.html", title="HOME")

#route for all hardware
@app.route('/allhardware')
#define function all_hardware()
def all_hardware():
    conn = sqlite3.connect('HARDWARE.db') #connect database
    cur = conn.cursor()
    cur.execute('SELECT hw_id, hw_name FROM Hardware;') #Query
    hardwares = cur.fetchall()
    conn.close()
    return render_template("all_hardware.html", title="all_hardware", hardwares=hardwares)

#route for specific hardware
@app.route('/hardware/<int:id>')
#define function hardware()
def hardware(id):
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Hardware;')
    hardwares = cur.fetchall()
    hardware = hardwares[id-1]
    conn.close()
    return render_template("hardware.html", title="hardware", id=id, hardware=hardware)

#route for specific hardware
@app.route('/software')
#define function software()
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
