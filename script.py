import requests
import sqlite3
from bs4 import BeautifulSoup #sudo python3 -m pip install bs4
import hashlib
secret=""; 
conn = sqlite3.connect("captcha.db")
cursor = conn.cursor()
s = requests.session()
site_const_url = "http://tasks.open.kksctf.ru:20005/"
seed=5000;# you can set ~2500
def find_secret_word(text):
	secret_word="";
	if(text.find('secret is:')==-1):
		print(secret);
		return -1;
	for i in range(text.find('secret is:') + 18,len(text)):
		if(text[i]=='<'):
			break
		secret_word+=text[i]
	return secret_word;
def gen(last_chars):
	for i in range(33,122):
		for j in range(1,seed):
			string = chr(i)*j
			now_str =hashlib.md5(string.encode()).hexdigest()
			#print(now_last_chars)
			if(hashlib.md5(string.encode()).hexdigest()[28::]==last_chars):
				#print("ACCESS:"+now_str + "\nACCESS_STRING:"+string)
				return string

def req(site_url):
	global secret
	r = s.get(site_const_url+site_url+".php")
	soup = BeautifulSoup(r.text,"html.parser")
	md5_hash = soup.find("input", attrs={ "name" : "hash"})['value']
	#print("md5 hash:"+md5_hash)
	cursor.execute("SELECT s FROM captcha WHERE s_md5='%s'"%(md5_hash))
	last_chars = cursor.fetchone()[0];
	#print ("last 4 chars:"+last_chars);
	now_str = gen(last_chars)
	r_new = s.post(site_const_url+site_url+".php", data = {'hash':md5_hash,'ch':now_str,'s':'OK'})
	#print(r_new.text)
	secret_word = find_secret_word(r_new.text)
	print(secret_word)
	secret+=secret_word
	new_url =  site_url + secret_word
	req(hashlib.md5(new_url.encode()).hexdigest())
req("c3e97dd6e97fb5125688c97f36720cbe")
print(secret)