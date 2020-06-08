import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
#-------------------------------------------------------------

con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:
#create buggies table
con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    tyres                 VARCHAR(20) DEFAULT "knobbly",
    qty_tyres             INTEGER DEFAULT 4,
    power_type            VARCHAR(20) DEFAULT "petrol",
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20),
    aux_power_units       INTEGER DEFAULT 0,
    hamster_booster       INTEGER DEFAULT 0,
    flag_color            VARCHAR(20) DEFAULT "white",
    flag_color_secondary  VARCHAR(20) DEFAULT "black",
    flag_pattern          VARCHAR(20) DEFAULT "plain",
    armour                VARCHAR(20) DEFAULT "none",
    attack                VARCHAR(20) DEFAULT "none",
    qty_attacks           INTEGER DEFAULT 0,
    fireproof             BIT DEFAULT 0,
    insulated             BIT DEFAULT 0,
    antibiotic            BIT DEFAULT 0,
    banging               BIT DEFAULT 0,
    algo                  VARCHAR(20) DEFAULT "steady",
    total_cost            INTEGER
  )

""")
#create table of details for power
con.execute("""

  CREATE TABLE IF NOT EXISTS powerDetail (
    name        VARCHAR(20),
    cost        INTEGER,
    kg          INTEGER,
    consumable  BIT
  )
""")
#populate table with data
con.execute("""

  INSERT INTO powerDetail (name, cost, kg, consumable)
  VALUES
    ("petrol", 4, 2, 1),
    ("fusion", 400, 100, 0),
    ("steam", 3, 4, 1),
    ("bio", 5, 2, 1),
    ("electric", 20, 20, 1),
    ("rocket", 16, 2, 1),
    ("hamster", 3, 1, 1),
    ("thermo", 300, 100, 0),
    ("solar", 40, 30, 0),
    ("wind", 20, 30, 0)

""")
#create table for details of tyre
con.execute("""

  CREATE TABLE IF NOT EXISTS tyreDetail (
    name        VARCHAR(20),
    cost        INTEGER,
    kg          INTEGER
  )
""")
#populate table with data
con.execute("""

  INSERT INTO tyreDetail (name, cost, kg)
  VALUES
    ("knobbly", 15, 20),
    ("slick", 10, 14),
    ("steelband", 20, 28),
    ("reactive", 40, 20),
    ("maglev", 50, 30)

""")
#create table for details of armour
con.execute("""

  CREATE TABLE IF NOT EXISTS armourDetail (
    name        VARCHAR(20),
    cost        INTEGER,
    kg          INTEGER
  )
""")
#populate table with data
con.execute("""

  INSERT INTO armourDetail (name, cost, kg)
  VALUES
    ("none", 0, 0),
    ("wood", 40, 100),
    ("aluminium", 200, 50),
    ("thinsteel", 100, 200),
    ("thicksteel", 200, 400),
    ("titanium", 290, 300)

""")
#create table of details for attacks
con.execute("""

  CREATE TABLE IF NOT EXISTS attackDetail (
    name        VARCHAR(20),
    cost        INTEGER,
    kg          INTEGER
  )
""")
#populate table with data
con.execute("""

  INSERT INTO attackDetail (name, cost, kg)
  VALUES
    ("none", 0, 0),
    ("spike", 5, 10),
    ("flame", 20, 12),
    ("charge", 28, 25),
    ("biohazard", 30, 10)

""")

con.commit()
print("- Table \"buggies\" exists OK")
print("- Table \"powerDetail\" exists OK")
print("- Table \"tyreDetail\" exists OK")
print("- Table \"armourDetail\" exists OK")
print("- Table \"attackDetail\" exists OK")


cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
  con.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")
print("- done")

con.close()