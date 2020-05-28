#This is a ridiculous test if I can do things properly - here's to hoping
import sqlite3 as sql

#current commit
	
DATABASE_FILE = "database.db"

def upgrade():
	with sql.connect(DATABASE_FILE) as con:
		con.execute("ALTER TABLE buggies ADD COLUMN power_units INTEGER;")
		con.execute("ALTER TABLE buggies ADD COLUMN aux_power_units INTEGER")

def downgrade() :
	with sql.connect(DATABASE_FILE) as con:
		con.execute("""
  		  CREATE TABLE IF NOT EXISTS dummy (
    		id                    INTEGER PRIMARY KEY,
    		qty_wheels            INTEGER DEFAUlT 4,
    		power_type            VARCHAR(20) DEFAULT "petrol",
    		aux_power_type        VARCHAR(20),
    		flag_color            VARCHAR(20) DEFAULT "white",
    		flag_color_secondary  VARCHAR(20) DEFAULT "black",
    		flag_pattern          VARCHAR(20)
  		  )
		""")
		con.execute("""
			INSERT into dummy(id, qty_wheels, power_type, aux_power_type, flag_color, flag_color_secondary, flag_pattern)
			SELECT id, qty_wheels, power_type, aux_power_type, flag_color, flag_color_secondary, flag_pattern
			FROM buggies;
			""")
		con.execute("DROP TABLE buggies;")
		con.execute("ALTER TABLE dummy RENAME TO buggies;")
		con.commit()
