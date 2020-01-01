import sqlite3
import hashlib 
conn = sqlite3.connect("captcha.db") # create database with captcha
cursor = conn.cursor()
cursor.execute("""CREATE TABLE captcha
                  (s text, s_md5 text)
               """)
alphbt = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'] #A set of characters that can occur in an md5 hash
def generate(string_w,length):
	if(length==4):
		md5s = hashlib.md5(string_w.encode())
		cursor.execute("INSERT INTO captcha VALUES('%s','%s')"%(string_w,md5s.hexdigest()))
		print string_w;
		return;
	for i in alphbt:
		generate(string_w+i,length+1)
	return
generate("",0)
conn.commit()