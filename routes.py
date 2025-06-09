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
    cur.execute()
    hardwares = cur.fetchall()
    conn.close()
    hardware = hardwares[id-1]
    return render_template("all_hardware.html", title="all_hardware", hardware=hardware, hardwares=hardwares)


@app.route('/hardware>')
def hardware():
    return render_template("hardware.html", title="hardware")


@app.route('/software')
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
