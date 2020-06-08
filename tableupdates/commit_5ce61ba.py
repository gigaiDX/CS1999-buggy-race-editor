#This is a ridiculous test if I can do things properly - here's to hoping
import sqlite3 as sql

#commit 5ce61ba
	
DATABASE_FILE = "database.db"

def upgrade():
	with sql.connect(DATABASE_FILE) as con:
		con.execute("ALTER TABLE buggies ADD COLUMN insulated BIT;")

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
    		fireproof             BIT DEFAULT 0
  		  )
		""")
		con.execute("""
			INSERT into dummy(id, qty_wheels, tyres, qty_tyres, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_color_secondary, flag_pattern, armour, attack, qty_attacks, fireproof)
			SELECT id, qty_wheels, tyres, qty_tyres, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_color_secondary, flag_pattern, armour, attack, qty_attacks, fireproof
			FROM buggies;
			""")
		con.execute("DROP TABLE buggies;")
		con.execute("ALTER TABLE dummy RENAME TO buggies;")
		con.commit()
