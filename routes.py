from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", title="HOME")


@app.route('/allhardware')
def all_hardware():
    return render_template("all_hardware.html", title="all hardware")


@app.route('/hardware')
def hardware():
    return render_template("hardware.html", title="hardware")


@app.route('/software')
def software():
    return render_template("software.html", title="software")


if __name__ == "__main__":
    app.run(debug=True)
