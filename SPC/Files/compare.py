import re
# from mechanize import Browser
import os
import re
import requests
import urllib
import hashlib
import sys
import pickle
import os
import getpass

if len(sys.argv) != 2:
	print("Provide file or directory path")
	exit()
root = sys.argv[1]
# print(root)
root = os.path.abspath(root)
# print(root)
home = os.path.expanduser('~/SPC')

if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

if os.path.isfile(home+'/Pickles/session.pkl'):
	fp = open(home+'/Pickles/session.pkl','rb')
	cred = pickle.load(fp)
	usrnm = cred[0]
	passwd = cred[1]
else:
	usrnm = input('Enter username: ')
	passwd = getpass.getpass(prompt='Enter password: ',stream=None)

payload = {'username':usrnm,'password':passwd,'submit':'Submit'}
s = requests.session()
# home = os.path.expanduser('~')
# fp = open(home+'/session.pkl','rb')
# s = pickle.load(fp)
r = s.post("http://"+url+"/login.php", data = payload)
# print(r.text)

if not 'logout.php' in r.text:
	exit("Invalid user -- Please try again")
# os.chdir(root)
print("Observing directory for user '"+usrnm+"' ...")
if root[-1]!='/':
	root = root+"/"

cliName=[]
climd5=[]
os.chdir(root)
for path, subdirs, files in os.walk(root):
	if len(files)==0 and len(subdirs)==0:
		fullname = os.path.join(path)
		# print(fullname)
		l = len(root)
		fullname = fullname[l:]
		if fullname=="" or fullname=="/":
			continue
		cliName.append(fullname+'/')
		# print(fullname+'/')
		# hash = hashlib.md5(open(fullname,'rb').read()).hexdigest()
		climd5.append("")
	for name in files:
		if name != 'Cryptod.class' and name != 'Cryptoe.class' and name != 'DESd.class' and name != 'DESe.class':
			fullname = os.path.join(path, name)
			# print(fullname)
			l = len(root)
			# print(l)
			fullname = fullname[l:]
			# print(fullname)
			cliName.append(fullname)
			hash = hashlib.md5(open(fullname,'rb').read()).hexdigest()
			climd5.append(hash)

r = s.post("http://"+url+"/list_files.php")	
# print(r.text)
result = r.text.split('|')
# id = result[0::3]
servName = result[1::4]
servmd5 = result[2::4]

server = dict(zip(servName,servmd5))
client = dict(zip(cliName,climd5))

AIBsame = [] # A:client B:server
AIBdiff = []
AMB = []
BMA = [value for value in servName if value not in cliName]
for value in cliName:
	if value in servName:
		if server[value]==client[value]:
			AIBsame.append(value)
		else:
			AIBdiff.append(value)
	else:
		AMB.append(value)

print("Same files :- ")
for f in AIBsame:
	print(f)
print("\n")
print("Same file names but diff. content :- ")
for f in AIBdiff:
	print(f)
print("\n")
print("Files in computer, not on server :- ")
for f in AMB:
	print(f)
print("\n")
print("Files on server, not in computer :- ")
for f in BMA:
	print(f)
