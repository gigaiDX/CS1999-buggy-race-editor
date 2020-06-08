from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
    with sql.connect(DATABASE_FILE) as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      record = cur.fetchone(); 
    return render_template("buggy-form.html", buggy = record)
#Section to request data from form and set it to respective variables
  elif request.method == 'POST':
    msg=""
    qty_wheels = request.form['qty_wheels']
    tyres = request.form ['tyres']
    qty_tyres = request.form['qty_tyres']
    power_type = request.form['power_type']
    power_units = request.form['power_units']
    aux_power_type = request.form['aux_power_type']
    aux_power_units = request.form['aux_power_units']
    hamster_booster = request.form['hamster_booster']
    flag_color = request.form['flag_color']
    flag_color_secondary = request.form['flag_color_secondary']
    flag_pattern = request.form['flag_pattern']
    armour = request.form['armour']
    attack = request.form['attack']
    qty_attacks = request.form['qty_attacks']
    fireproof = request.form['fireproof']
    insulated = request.form['insulated']
#Validation section
    try:
      with sql.connect(DATABASE_FILE) as con:
        if qty_wheels.isdigit() == True:
          if int(qty_wheels) % 2 != 0:  
            msg = f"Wheel quantity is not even (qty_wheels: {qty_wheels})"
            raise ValueError("qty_wheels is not even")
        elif qty_wheels.isdigit() == False:
          msg = f"Wheel quantity is not an integer (qty_wheels: {qty_wheels})"
          raise TypeError("qty_wheels not an integer") 
        if qty_tyres.isdigit() == True:
          if int(qty_tyres) < int(qty_wheels):
            msg =f"Total number of tyres is less than number of wheels! (qty_tyres: {qty_tyres}, qty_wheels: {qty_wheels})"
            raise ValueError("qty_tyres invalid - smaller than qty_wheels")
        elif qty_tyres.isdigit() == True:
          msg = f"Tyre quantity is not an integer (qty_tyres: {qty_tyres})"
          raise TypeError("qty_tyres not an integer")
    except:
      con.rollback()
      con.close()
      return render_template("updated.html", msg = msg)
#Setting new values to database
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=?, tyres=?, qty_tyres=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=? WHERE id=?", 
          (qty_wheels, tyres, qty_tyres, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_color_secondary, flag_pattern, armour, attack, qty_attacks, fireproof, insulated, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
