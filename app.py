from flask import Flask, render_template, request, jsonify
from ClockIn import ClockIn
app = Flask(__name__)


@app.route("/in", methods=['GET', 'POST'])
def clock_that_bitch_in():
    clock = ClockIn()
    message = clock.punch_in()
    return message


@app.route("/out", methods=['GET', 'POST'])
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
    return jsonify(msg=clock.total_time_today())


@app.route("/total_time_this_week")
def total_time_this_week():
    clock = ClockIn()
    return clock.total_time_this_week()


@app.route("/select_day", methods=['POST'])
def select_day():
    return request.form.get("day")


if __name__ == "__main__":
    app.run(debug=True)
    pass
