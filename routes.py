'''Python Flask application routes for 12DB_WEBPROJECT.'''
# routes.py
from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


# route for home
@app.route('/')
def home():
    # Render the home page.
    # Needed so the user doesn't get confused when they first open the website
    return render_template("home.html", title="HOME")


# route for all hardware
@app.route('/allhardware', methods=['GET'])
def all_hardware():
    # Render the all hardware page.
    # Needed so user can see all hardware in database, choose one
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    # Query --> get items needed from table Hardware
    cur.execute('SELECT hw_id, hw_name, hw_image FROM Hardware;')
    hardwares = cur.fetchall()
    conn.close()
    return render_template("all_hardware.html", title="all_hardware",
                           hardwares=hardwares)


# route for specific hardware
@app.route('/hardware/<int:id>')
def hardware(id):
    # render the hardware details page.
    # Shows details about a specific hardware item
    if id < 1 or id > 19:  # abourt 404 if id not in range of hw_id
        return render_template('404.html'), 404
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    # Query --> get hardware details in a readable format
    # finding one row in Hardware with hw_id in the url
    cur.execute('''SELECT
                    h.hw_id,
                    h.hw_name,
                    h.release_yr,
                    h.description,
                    h.sale,
                    c.console_type,
                    m.media_name,
                    h.hw_image
                FROM Hardware h
                LEFT JOIN ConsoleType c ON h.con_id = c.con_id
                LEFT JOIN MediaType m ON h.media_id = m.media_id
                WHERE h.hw_id = ?
                ''', (id,))
    hardware = cur.fetchone()
    # Query --> get all softwareseries related to hw_id in the url
    # To present with the hardware details
    cur.execute('''SELECT sw_id, sw_name FROM SoftwareSeries WHERE sw_id IN (
                 SELECT sw_id FROM HardSoft WHERE hw_id = (
                 SELECT hw_id FROM Hardware WHERE hw_id = ?));''', (id,))
    softwareseries = cur.fetchall()  # creating a list of tuples
    conn.close()
    return render_template(
        "hardware.html",
        title="hardware",
        id=id,
        hardware=hardware,
        softwareseries=softwareseries
    )


# route for specific hardware
@app.route('/softwareseries/<int:id>')
def software(id):
    # To show detail of specific software series from the hardware details page
    if id < 1 or id > 21:  # abourt 404 if id not in range of sw_id
        return render_template('404.html'), 404
    conn = sqlite3.connect('HARDWARE.db')
    cur = conn.cursor()
    # Query --> get one row in SoftwareSeries with sw_id relevant
    cur.execute('''SELECT * FROM SoftwareSeries WHERE sw_id = ?''', (id,))
    software_series = cur.fetchone()
    # also get all hardware related to this software series if have time
    conn.close()
    return render_template(
        "software.html",
        title="software",
        software_series=software_series
        )


# route for search bar
@app.route('/search_result', methods=['GET'])
def search():  # initaly copy student teacher's code --> adapt and improve it
    # Render the search results page.
    # Needed so the user can search for hardware by name or by software
    search_query = request.args.get('query', '')
    if not (1 <= len(search_query) <= 50):
        return render_template('search_result.html')
    search_type = request.args.get('type', 'name')  # 'name' or 'series'
    conn = sqlite3.connect('HARDWARE.db')
    try:  # try and except to prevent crashing if error in SQL query
        if search_query:
            if search_type == 'series':
                # Query --> get hardware related to software from search_query
                cursor = conn.execute('''SELECT hw_id, hw_name, hw_image
                    FROM Hardware WHERE hw_id IN (
                    SELECT hw_id FROM HardSoft WHERE sw_id IN (
                        SELECT sw_id FROM SoftwareSeries WHERE sw_name LIKE ?)
                        );''', ('%' + search_query + '%',)
                    )
            elif search_type == 'name':
                # Query --> get all hardware related from search_query
                cursor = conn.execute('''SELECT hw_id,
                                    hw_name,
                                    hw_image
                                    FROM Hardware
                                    WHERE hw_name
                                    LIKE ?''', ('%' + search_query + '%',))
        else:
            cursor = conn.execute('''SELECT hw_id,
                                  hw_name,
                                  hw_image
                                  FROM Hardware''')
        hardwares = cursor.fetchall()
        conn.close()
        if search_query and not hardwares:
            # if statement to pass error when no results found
            error = "No results found for your search."
            return render_template(
                'search_result.html',
                hardwares=hardwares,
                search_query=search_query,
                error=error
            )
        # render template normally if no errors
        return render_template(
            'search_result.html',
            hardwares=hardwares,
            search_query=search_query
        )
    except (UnboundLocalError, sqlite3.OperationalError):
        # if the user trys to break the SQL query, create error message
        conn.close()
        error = "An error occurred while processing your request."
        return render_template('search_result.html', error=error)


# attributons page route
@app.route('/attributions')
def attributions():
    # Render the attributions page.
    # Needed so the user can see where all the data and images came from
    return render_template("attributions.html", title="attributions")


# route for 404 error
@app.errorhandler(404)
def page_not_found(e):
    # Render the 404 error page.
    # Needed so when user tried to access a page that doesn't exist
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
