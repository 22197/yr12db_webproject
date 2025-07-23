from flask import Flask, render_template, request
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
    cur.execute('SELECT hw_id, hw_name, hw_image FROM Hardware;') 
    hardwares = cur.fetchall()
    conn.close()
    return render_template("all_hardware.html", title="all_hardware", hardwares=hardwares)

#route for specific hardware
@app.route('/hardware/<int:id>')
def hardware(id):
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    #Query --> get all the items in table Hardware connected to table MediaType and ConsoleType
    cur.execute('''SELECT
                    h.hw_id, 
                    h.hw_name, 
                    h.release_yr, 
                    h.description, 
                    h.sale_after_yr, 
                    c.console_type, 
                    m.media_name,
                    h.hw_image

                FROM Hardware h

                LEFT JOIN ConsoleType c ON h.con_id = c.con_id

                LEFT JOIN MediaType m ON h.media_id = m.media_id
                
                WHERE h.hw_id = ?
                ''', (id,))
    hardware = cur.fetchone() #finding one row in the table Hardware with the id that was passed in the url
    cur = conn.cursor()
    #Query --> get all softwareseries that are related to Hardware
    cur.execute('''SELECT sw_id, sw_name FROM SoftwareSeries WHERE sw_id IN (
                 SELECT sw_id FROM HardSoft WHERE hw_id = (
                 SELECT hw_id FROM Hardware WHERE hw_id = ?));''', (id,))
    softwareseries = cur.fetchall()#creating a list of tuples "softwareseries"
    conn.close()
    return render_template("hardware.html", title="hardware", id=id, hardware=hardware, softwareseries=softwareseries)

#route for specific hardware
@app.route('/softwareseries/<int:id>')
def software(id):

    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM SoftwareSeries WHERE sw_id = ?''', (id,))
    SoftwareSeries = cur.fetchone()
    conn.close()
    return render_template("software.html", title="software", SoftwareSeries=SoftwareSeries)
    


#route for search bar
'''@app.route('search_result.html', methods = ['POST', 'GET'])
def search():
    search_query = request.args.get('search', '')
    if search_query:
        print("hi")'''


if __name__ == "__main__":
    app.run(debug=True)
