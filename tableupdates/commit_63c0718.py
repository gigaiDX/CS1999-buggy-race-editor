#This is a ridiculous test if I can do things properly - here's to hoping
import sqlite3 as sql

#commit 63c0718

DATABASE_FILE = "database.db"

def upgrade():
	with sql.connect(DATABASE_FILE) as con:
		con.execute("ALTER TABLE buggies ADD COLUMN power_type VARCHAR(20);")

def downgrade() :
	with sql.connect(DATABASE_FILE) as con:
		con.execute("""
  		  CREATE TABLE IF NOT EXISTS dummy (
    		id                    INTEGER PRIMARY KEY,
    		qty_wheels            INTEGER DEFAUlT 4,
    		flag_color            VARCHAR(20) DEFAULT "white",
    		flag_color_secondary  VARCHAR(20) DEFAULT "black",
    		flag_pattern          VARCHAR(20)
  		  )
		""")
		con.execute("""
			INSERT into dummy(id, qty_wheels, flag_color, flag_color_secondary, flag_pattern)
			SELECT id, qty_wheels, flag_color, flag_color_secondary, flag_pattern
			FROM buggies;
			""")
		con.execute("DROP TABLE buggies;")
		con.execute("ALTER TABLE dummy RENAME TO buggies;")
		con.commit()
