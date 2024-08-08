import ftplib
import os

HOST = '192.168.0.72'
PORT = 21
ID = 'ubuntu' 
PW = 'robot' 

f = ftplib.FTP() 
f.set_debuglevel(1) 

f.connect(HOST,PORT) 

f.login(ID,PW) 

f.cwd('') 


file_path = '/home/ubuntu/Desktop/mines_lab/mines_robot/CHAT/'

filename = os.path.join(file_path,'response.wav')
with open(filename, 'rb') as read_f:
	f.storbinary('STOR response.wav',read_f)

f.quit() 