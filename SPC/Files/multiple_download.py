import os
import re
import requests
import urllib
import hashlib
import pickle
import os
import getpass

# home = os.path.expanduser('~')
# fp = open(home+'/session.pkl','rb')
# s = pickle.load(fp)

home = os.path.expanduser('~/SPC')
# key=""
# if os.path.isfile(home+'/aeskey.txt'):
# 	# print("Yes")
# 	with open(home+'/aeskey.txt','r') as file:
# 		for r in file:
# 			key = r
# else:
# 	exit("No key found")
# if key[-1]=="\n":
# 	key=key[:-1]
# print(key)
# exit()
if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

# home = os.path.expanduser('~')
if os.path.isfile(home+'/Pickles/session.pkl'):
	fp = open(home+'/Pickles/session.pkl','rb')
	cred = pickle.load(fp)
	usrnm = cred[0]
	passwd = cred[1]
else:
	usrnm = input('Enter username: ')
	passwd = getpass.getpass(prompt='Enter password: ',stream=None)

# usrnm = input('Enter username: ')
# passwd = getpass.getpass(prompt='Enter password: ',stream=None)
payload = {'username':usrnm,'password':passwd,'submit':'Submit'}
s = requests.session()
r = s.post("http://"+url+"/login.php", data = payload)
# print(r.text)

if 'logout.php' in r.text:
	print("Starting download for user: "+usrnm)
else:
	exit("Invalid user -- Please try again")

r = s.post("http://"+url+"/list_files.php")
# print(r.text)
result = r.text.split('|')
id = result[0::4]
name = result[1::4]
md5sum = result[2::4]

result = zip(id,name,md5sum)

schema = input('Which schema are you using?(AES or DES or BLOWFISH) ')
confirm = input('Are you sure?(yes or no) ')

if confirm == "no" or confirm == "n":
	exit('Check first.')

if schema != "BLOWFISH" and schema != "AES" and schema != "DES":
	exit("Unknown schema")

def func(id,path,hash):
	# print path
	# path = path.replace(":","/")
	x = path.rfind("/")
	dirName = path[:x+1]
	try:
		os.makedirs(dirName)
		print("Creating directory "+dirName+"\n"+"Downloading "+path.split('/')[-1]);
		url1 = "http://"+url+"/linux_get_file.php?id=" + str(id)
		# payload = {'key':key,'submit':True}
		r = s.post(url1)
		open(path, 'wb').write(r.content)
		if schema == "AES":
			os.system('javac -d . '+home+'/AES/Cryptod.java')
			os.system('java Cryptod '+path)
		elif schema == "DES":
			os.system('javac -d . '+home+'/DES/DESd.java')
			os.system('java DESd '+path)
		elif schema == "BLOWFISH":
			os.system('javac -d . '+home+'/Blowfish/Blowd.java')
			os.system('java Blowd '+path)
		if hash == hashlib.md5(open(path,'rb').read()).hexdigest():
			print("VERIFIED")
		else:
			print("WRONG DOWNLOAD. Try again later.")
		# os.system('python '+home+'/ch9_decrypt_blob.py '+path)
	except OSError:
		print("Downloading "+path.split('/')[-1]);
		url1 = "http://"+url+"/linux_get_file.php?id=" + str(id)
		# payload = {'key':key,'submit':True}
		r = s.post(url1)
		open(path, 'wb').write(r.content)
		if schema == "AES":
			os.system('javac -d . '+home+'/AES/Cryptod.java')
			os.system('java Cryptod '+path)
		elif schema == "DES":
			os.system('javac -d . '+home+'/DES/DESd.java')
			os.system('java DESd '+path)
		elif schema == "BLOWFISH":
			os.system('javac -d . '+home+'/Blowfish/Blowd.java')
			os.system('java Blowd '+path)
		if hash == hashlib.md5(open(path,'rb').read()).hexdigest():
			print("VERIFIED")
		else:
			print("WRONG DOWNLOAD. Try again later.")
		# os.system('python '+home+'/ch9_decrypt_blob.py '+path)
		# urllib.request.urlretrieve ("http://192.168.0.103:8000/linux_get_file.php?id=" + str(id), path)
		# print("Directory " , dirName ,  " already exists")

for x in result:
	name = x[1]
	# name = name.replace(":","/")
	if os.path.isfile(name):
		hash = hashlib.md5(open(name,'rb').read()).hexdigest()
		if x[2] == hash:
			print(name+" already exists")
		elif "/" not in x[1]:
			print("Downloading "+x[1]+" "+str(x[0]));
			url1 = "http://"+url+"/linux_get_file.php?id=" + str(x[0])
			# payload = {'key':key,'submit':True}
			r = s.post(url1)
			open(x[1], 'wb').write(r.content)
			if schema == "AES":
				os.system('javac -d . '+home+'/AES/Cryptod.java')
				os.system('java Cryptod '+x[1])
			elif schema == "DES":
				os.system('javac -d . '+home+'/DES/DESd.java')
				os.system('java DESd '+x[1])
			elif schema == "BLOWFISH":
				os.system('javac -d . '+home+'/Blowfish/Blowd.java')
				os.system('java Blowd '+x[1])
			if x[2] == hashlib.md5(open(name,'rb').read()).hexdigest():
				print("VERIFIED")
			else:
				print("WRONG DOWNLOAD. Try again later.")
			# os.system('python '+home+'/ch9_decrypt_blob.py '+x[1])
			# urllib.request.urlretrieve ("http://192.168.0.103:8000/linux_get_file.php?id=" + str(x[0]), x[1])
		else:
			func(x[0],name,x[2])
	elif "/" not in x[1]:
		print("Downloading "+x[1]+" "+str(x[0]));
		# urllib.request.urlretrieve ("http://192.168.0.103:8000/linux_get_file.php?id=" + str(x[0]), x[1])
		url1 = "http://"+url+"/linux_get_file.php?id=" + str(x[0])
		# payload = {'key':key,'submit':True}
		r = s.post(url1)
		open(x[1], 'wb').write(r.content)
		# os.system('python '+home+'/ch9_decrypt_blob.py '+x[1])
		if schema == "AES":
			os.system('javac -d . '+home+'/AES/Cryptod.java')
			os.system('java Cryptod '+x[1])
		elif schema == "DES":
			os.system('javac -d . '+home+'/DES/DESd.java')
			os.system('java DESd '+x[1])
		elif schema == "BLOWFISH":
			os.system('javac -d . '+home+'/Blowfish/Blowd.java')
			os.system('java Blowd '+x[1])
		if x[2] == hashlib.md5(open(name,'rb').read()).hexdigest():
			print("VERIFIED")
		else:
			print("WRONG DOWNLOAD. Try again later.")
	elif name[-1]=='/':
		try:
			os.makedirs(name)
			print("Creating directory "+name)
		except OSError:
			print(name+" already exists")
	else:
		func(x[0],name,x[2])

# r = s.post("http://192.168.0.103:8000/linux_get_file.php?id=1")
# print(r.text)

if os.path.exists("Cryptod.class"):
	os.remove("Cryptod.class")
else:
	pass
if os.path.exists("Cryptoe.class"):
	os.remove("Cryptoe.class")
else:
	pass
if os.path.exists("Blowd.class"):
	os.remove("Blowd.class")
else:
	pass
if os.path.exists("Blowe.class"):
	os.remove("Blowe.class")
else:
	pass
if os.path.exists("DESd.class"):
	os.remove("DESd.class")
else:
	pass
if os.path.exists("DESe.class"):
	os.remove("DESe.class")
else:
	pass

print("Download completed")