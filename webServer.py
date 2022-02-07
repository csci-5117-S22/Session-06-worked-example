from flask import Flask, g, render_template, request, redirect, url_for
import dice
import dice.utilities
import random
import psycopg2
import os

app = Flask(__name__)


##### Database functions
## This is a kinda lame way to do it, that is better exist, but it
## Shows off some cool ideas
def connect_db():
    """Connects to the specific database."""
    return psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    # The "g" object is a "global" Note -- this is global within the context of
    # a single request, not what we normally call global.
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db

# This teardown happens after each request, and closes the DB
@app.after_request
def close_db(response):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        app.logger.warn("teardown")
        g.pg_db.close()
    return response


@app.route('/')
def frontPage():
    return viewRolls()

@app.route('/roll',methods=['GET'])
def viewRolls():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT roll_id, roll_memo, roll_config, roll_result FROM roll;")
    rolls = cur.fetchall()
    olls = [record for record in cur]
    cur.close()

    return render_template("all_rolls.html", rolls=rolls)

@app.route('/roll', methods=['POST'])
def doRoll():
    roll_config = request.form.get('roll_config', 'd6')
    memo = request.form.get('roll_memo', 'nobody')
    result = dice.roll(roll_config, raw=True)
    roll_result_long = dice.utilities.verbose_print(result)
    roll_result = result.result

    conn = get_db()
    cur = conn.cursor()
    cur.execute("insert into roll (roll_memo, roll_config, roll_result_long, roll_result) values (%s,%s,%s,%s) returning roll_id;", (memo, roll_config, roll_result_long, roll_result))
    id = cur.fetchone()
    id = id[0]
    cur.close()
    conn.commit()

    return redirect(url_for("viewRollDetails", roll_id = id))

@app.route('/roll/<roll_id>')
def viewRollDetails(roll_id):
    conn = get_db()

    cur = conn.cursor()
    cur.execute("SELECT roll_id, roll_memo, roll_config, roll_result, roll_result_long FROM roll where roll_id = %s;", (roll_id,))
    roll = cur.fetchone()
    cur.close()
    # I _REALLY_ should be repackaging this row into at least a named tuple or a dictionary.
    # having to do lookup by index in the front-end is terrible practice.

    return render_template("one_rolls.html", roll=roll)

if __name__ == '__main__':
    app.run()
