import os
import re
import requests
import urllib
import hashlib
import pickle
import os
import getpass
import shutil

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
# # print(key)
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
	pass
else:
	exit("Invalid user -- Please try again")

r = s.post("http://"+url+"/list_files.php")	
# print(r.text)
result = r.text.split('|')
id = result[0::4]
name = result[1::4]
md5sum = result[2::4]

result = zip(id,name,md5sum)

schema = input('Which is your current schema?(AES or DES or BLOWFISH) ')
confirm = input('Are you sure?(yes or no) ')

if confirm == "no" or confirm == "n":
	exit('Check first.')

if schema != "BLOWFISH" and schema != "AES" and schema != "DES":
	exit("Unknown schema")

try:
	os.makedirs('spc_backup')
except OSError:
	pass

os.chdir('spc_backup')

def func(id,path):
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
			# os.system('python '+home+'/ch9_decrypt_blob.py '+x[1])
			# urllib.request.urlretrieve ("http://192.168.0.103:8000/linux_get_file.php?id=" + str(x[0]), x[1])
		else:
			func(x[0],name)
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
	elif name[-1]=='/':
		try:
			os.makedirs(name)
			print("Creating directory "+name)
		except OSError:
			print(name+" already exists")
	else:
		func(x[0],name)

schema = input('Enter new schema:(AES or DES or BLOWFISH) ')
key1 = input('Enter new key1: ')
# key2 = input('Enter new key2:(Hit ENTER in case of AES or DES) ')

# with open(home+'/aeskey.txt','w') as file:
# 	file.write(newkey)
# file.close()

if schema == "AES":
	with open(home+'/AES/aeskey.txt','w') as file:
		file.write(key1)
	file.close()
if schema == "DES":
	with open(home+'/DES/deskey.txt','w') as file:
		file.write(key1)
	file.close()
if schema == "BLOWFISH":
	with open(home+'/Blowfish/bkey.txt','w') as file:
		file.write(key1)
	file.close()

root = os.path.abspath('./')

# print(root)

if root[-1]!='/':
	root+='/'

for path, subdirs, files in os.walk(root):
	if len(files)==0 and len(subdirs)==0:
		fullname = os.path.join(path)
		l = len(root)
		fullname = fullname[l:] + '/'
		data = {'path':fullname,'md5sum':'','submit':True}
		print("Uploading "+fullname+"\033[K")
		r = s.post("http://"+url+"/up_linux.php", data = data)
	for name in files:
		if name != 'Cryptod.class' and name != 'Cryptoe.class'  and name != 'DESd.class' and name != 'DESe.class' and name != 'Blowd.class' and name != 'Blowe.class':
			fullname = os.path.join(path, name)
			l = len(root)
			fullname = fullname[l:]
			md5sum = hashlib.md5(open(fullname,'rb').read()).hexdigest()
			print("Uploading "+fullname+" "+md5sum+"\033[K")
			# done+=os.path.getsize(fullname)
			# os.system('python '+home+'/ch9_encrypt_blob.py '+fullname)
			if schema == "AES":
				os.system('javac -d . '+home+'/AES/Cryptoe.java')
				os.system('java Cryptoe '+fullname)
			elif schema == "DES":
				os.system('javac -d . '+home+'/DES/DESe.java')
				os.system('java DESe '+fullname)
			elif schema == "BLOWFISH":
				os.system('javac -d . '+home+'/Blowfish/Blowe.java')
				os.system('java Blowe '+fullname)
			files = {'uploaded_file': open(fullname,'rb')}
			# os.system('python '+home+'/ch9_decrypt_blob.py '+fullname)
			data = {'path':fullname,'md5sum':md5sum,'submit':True}
			# # print("Yes")
			r = s.post("http://"+url+"/up_linux.php", files = files, data = data)
			# print(r.text)
			# printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
			# os.system('python '+home+'/ch9_decrypt_blob.py '+fullname)
			if schema == "AES":
				os.system('javac -d . '+home+'/AES/Cryptod.java')
				os.system('java Cryptod '+fullname)
			elif schema == "DES":
				os.system('javac -d . '+home+'/DES/DESd.java')
				os.system('java DESd '+fullname)
			elif schema == "BLOWFISH":
				os.system('javac -d . '+home+'/Blowfish/Blowd.java')
				os.system('java Blowd '+fullname)



os.chdir('..')
shutil.rmtree('spc_backup')




print("Updated successfully!! Please don't do it again ... It takes a lot of work :(")