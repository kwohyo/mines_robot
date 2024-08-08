import ftplib
import os

HOST = ''
PORT = 1234
ID = '' 
PW = '' 

f = ftplib.FTP() 
f.set_debuglevel(1) 

f.connect(HOST,PORT) 

f.login(ID,PW) 

entries = f.nlst() 
print(entries)
dir = f.dir() 
print(dir)

f.cwd('') 


file_path = ''

filename = os.path.join(file_path,'output.wav')
with open(filename, 'rb') as read_f:
	f.storbinary('STOR output.wav',read_f)



f.quit() 