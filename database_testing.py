import sqlite3
import file_menu
import json
import getpass
from datetime import date

def setup_db():

	#conn = sqlite3.connect(":memory:")
	conn = sqlite3.connect(r"C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.03\test.db")
	#conn = sqlite3.connect(r"C:\Users\domhnall.morrisey.WOODGROUP\Downloads\PYCabin_Tk-master\PYCabin_Tk-master\test.db")
	c = conn.cursor()
	return conn, c


def create_tables(c):

#    c.execute('CREATE TABLE IF NOT EXISTS seats("Part Number" TEXT, "Aircraft Type" TEXT, "Description" TEXT, "Manufacturer" TEXT, "Side" TEXT, "Seat Type" TEXT, "IAT" TEXT, "Profile" TEXT, "Width" REAL, "Width Inbd" REAL, "Armrest Width" REAL, "Length Fwd" REAL, "Length Aft" REAL, "Cushion Height" REAL, "Height" REAL, "Stud Distance" REAL, "SRP X" REAL, "SRP Y" REAL, "Weight" REAL, "Comments" TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS seats(Title TEXT, Data TEXT, "Date" TEXT, "User" TEXT, "Project" TEXT)')

# def add_component_to_db(c, seat):
	
#	c.execute('INSERT INTO seats ("Part Number", "Aircraft Type", "Description", "Manufacturer", "Side", "Seat Type", "IAT", "Profile", "Width", "Width Inbd", "Armrest Width", "Length Fwd", "Length Aft", "Cushion Height", "Height", "Stud Distance", "SRP X", "SRP Y", "Weight", "Comments") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
   #       (seat.part_no, seat.aircraft_type, seat.description, seat.manufacturer, seat.side, seat.seat_type, seat.iat, seat.profile, seat.width, 
	#		seat.width_inbd, seat.armrest_width, seat.length_fwd, seat.length_aft, seat.cushion_height, seat.height, seat.stud_distance, 
	#		seat.srp_x, seat.srp_y, seat.weight_lbs, seat.comments))

def read_all_from_db(c):
    c.execute('SELECT * FROM seats')
    data = c.fetchall()
 
    for row in data:
        print(row)
		
def delete_component_from_db(c, value):

	c.execute(f'DELETE FROM seats WHERE part_no = "{value}"')
	#c.execute('DELETE FROM seats WHERE part_no = "A320 Seat 2"')
	
def search_for_component(c, search):
	
	#c.execute(f"SELECT * FROM seats WHERE part_no LIKE '%{search}%'")
	c.execute(f"SELECT * FROM seats WHERE part_no LIKE '%{search}%'")
	data = c.fetchall()
	print(data)
	for row in data:
		print(row)

# def load_json():

	# seats = []
	# #with open(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.03\test.json') as f:
	# with open(r'C:\Users\domhnall.morrisey.WOODGROUP\Downloads\PYCabin_Tk-master\PYCabin_Tk-master\test.json') as f:
		# data = json.load(f)
		
	# if 'Seats' in data.keys():
	
		# for seat in data['Seats']:
			# seat = file_menu.Load('Seat', seat)
	
			# seats.append(seat)
			
	# return seats

def load_json(conn, c):
	user = getpass.getuser()
	
	with open(r'C:\Users\domhn\Documents\Python\Pycabin_Tkinter\V0.03\test.json') as f:
		data = json.load(f)
		if 'Seats' in data.keys():
			print(data['Seats'])
			for seat in data['Seats']:
					print(seat)
					c.execute('INSERT INTO seats ("Title", "Data", "Date", "User", "Project") VALUES (?, ?, ?, ?, ?)',
								(seat['Title'], str(seat), date.today().strftime("%b-%d-%Y"), user, "Project"))
   #       (seat.part_no, seat.aircraft_type, seat.description, 
		
			
conn, c = setup_db()
create_tables(c)

#seats = load_json()
load_json(conn, c)
# for seat in seats:
	# add_component_to_db(c, seat)
conn.commit()

#read_all_from_db(c)
#search_for_component(c, 'A320 Seat 2')
# delete_component_from_db(c, 'A320 Seat 2')
# conn.commit()
# read_all_from_db(c)
c.close()
conn.close()