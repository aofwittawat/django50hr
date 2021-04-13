
import sqlite3
import csv 

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()




def writetodb(token,approved,user_id):
	with conn:
		c.execute("""INSERT INTO myapp_verifyemail (id,token,approved,user_id) VALUES (?,?,?,?)""",(None,token,approved,user_id))
	conn.commit() # save to data base
	print('Complete')


#  wirtetodb('alskdfjhsdfakfjhdslaf',0,10) ลอง write ดู



############ read CSV #########
with open('newtoken.csv',newline='',encoding='utf-8') as f:
	fr = csv.reader(f) # file reader
	# print(list(fr)) # try read data of fr 
	data = list(fr)
	print(data)

	for t,a,u in data:
		print(t,a,u)
		writetodb(t,int(a),int(u))