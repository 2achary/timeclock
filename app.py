from flask import Flask, render_template
from ClockIn import ClockIn
app = Flask(__name__)



def renderBody(arg):
    return """
    <DOCTYPE html>
    <head>
        <title>
            Time Clock
        </title>
    </head>
    <body style="max-width:800; margin: 0 auto; font-family:Arial;">
    {}
    </body>

    """.format(arg)

@app.route("/in")
def clock_that_bitch_in():
    clock = ClockIn()
    message = clock.punch_in()
    return message

@app.route("/out")
def clock_that_bitch_out():
    clock = ClockIn()
    message = clock.punch_out()
    page = "<h4>{}</h4>".format(message)
    print page
    return message

@app.route("/")
def main():
    return render_template('base.html')

@app.route("/list_entries")
def list_entries():
    clock = ClockIn()
    return clock.list_entries_for_day()


if __name__ == "__main__":
    app.run()
    # pass
