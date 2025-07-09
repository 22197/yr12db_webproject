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
    cur.execute('''SELECT
                h.hw_id, 
                h.hw_name, 
                h.release_yr, 
                h.description, 
                h.sale_after_yr, 
                c.console_type, 
                m.media_name

                FROM Hardware h

                LEFT JOIN ConsoleType c ON h.con_id = c.con_id

                LEFT JOIN MediaType m ON h.media_id = m.media_id''')
    hardwares = cur.fetchall() #fetch all hardware, creating a list of tuples
    hardware = hardwares[id-1] #since id starts from 1, subtract 1 to get the correct index

    cur1 = conn.cursor()
    cur1.execute('')
    softwareseries = cur1.fetchall()


    conn.close()
    return render_template("hardware.html", title="hardware", id=id, hardware=hardware, softwareseries=softwareseries)

#route for specific hardware
@app.route('/software')
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
