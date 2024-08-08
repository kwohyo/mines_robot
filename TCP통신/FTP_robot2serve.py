import ftplib
import os

HOST = '192.168.0.55'
PORT = 21
ID = 'mines' 
PW = 'mines' 

f = ftplib.FTP() 
f.set_debuglevel(1) 

f.connect(HOST,PORT) 
print('connected!')

f.login(ID,PW) 
print('login!')

entries = f.nlst() 
print(entries)
dir = f.dir() 
print(dir)

f.cwd('/home/mines/Desktop/chat/') 


file_path = '/home/ubuntu/Desktop/mines_lab/mines_robot/MIC/'

filename = os.path.join(file_path,'output.wav')
with open(filename, 'rb') as read_f:
	f.storbinary('STOR output.wav',read_f)



f.quit() 
