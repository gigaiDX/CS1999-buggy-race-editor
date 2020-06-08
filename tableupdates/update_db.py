#This is a ridiculous test if I can do things properly - here's to hoping
import sqlite3 as sql

#current commit
	
DATABASE_FILE = "database.db"

def upgrade():
	with sql.connect(DATABASE_FILE) as con:
		con.execute("ALTER TABLE buggies ADD COLUMN total_cost INTEGER;")
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
def downgrade() :
	with sql.connect(DATABASE_FILE) as con:
		con.execute("""	
  		  CREATE TABLE IF NOT EXISTS dummy (
    		id                    INTEGER PRIMARY KEY,
    		qty_wheels            INTEGER DEFAUlT 4,
    		tyres 				  VARCHAR(20) DEFAULT "knobbly",
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
    		algo                  VARCHAR(20) DEFAULT "steady"
  		  )
		""")
		con.execute("""
			INSERT into dummy(id, qty_wheels, tyres, qty_tyres, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_color_secondary, flag_pattern, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo)
			SELECT id, qty_wheels, tyres, qty_tyres, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_color_secondary, flag_pattern, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo
			FROM buggies;
			""")
		con.execute("DROP TABLE buggies;")
		con.execute("ALTER TABLE dummy RENAME TO buggies;")
		con.execute("DROP TABLE attackDetail;")
		con.execute("DROP TABLE powerDetail;")
		con.execute("DROP TABLE armourDetail;")
		con.execute("DROP TABLE tyreDetail;")
		con.commit()