from flask import Flask, render_template
from ClockIn import ClockIn
app = Flask(__name__)


@app.route("/in")
def clock_that_bitch_in():
    clock = ClockIn()
    message = clock.punch_in()
    return message

@app.route("/out")
def clock_that_bitch_out():
    clock = ClockIn()
    message = clock.punch_out()
    return message

@app.route("/")
def main():
    return render_template('base.html')

@app.route("/list_entries")
def list_entries():
    clock = ClockIn()
    return clock.list_entries_for_day()

@app.route("/total_time_today")
def total_time_today():
    clock = ClockIn()
    return clock.total_time_today()


if __name__ == "__main__":
    app.run()
    # pass
