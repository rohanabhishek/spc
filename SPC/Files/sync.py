import re
import os
import re
import requests
import urllib
import hashlib
import sys
import pickle
import os
import getpass

home = os.path.expanduser('~/SPC')

if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

if len(sys.argv) != 2:
	exit("Provide file or directory path")

root = sys.argv[1]

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

timeout=4

root = os.path.abspath(root)

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
r = s.post("http://"+url+"/login.php", data = payload,timeout=timeout)

# print(usrnm)
# print(passwd)
# print(r.text)
if not 'logout.php' in r.text:
	exit("Invalid user -- Please try again")

print("Observing directory for user '"+usrnm+"' ...")
if root[-1]!='/':
	root = root+"/"

r = s.post("http://"+url+"/syncing.php",timeout=timeout)
if r.text == 'True':
	exit("You are syncing with some other client also")

cliName=[]
climd5=[]
cliSize=[]
# print(root)
os.chdir(root)
for path, subdirs, files in os.walk(root):
	# print(path)
	if len(files)==0 and len(subdirs)==0:
		fullname = os.path.join(path)
		l = len(root)
		fullname = fullname[l:]
		if fullname != "" and fullname != "/":
			cliName.append(fullname+'/')
			climd5.append("")
			cliSize.append(0)
	for name in files:
		if name != 'Cryptod.class' and name != 'Cryptoe.class' and name != 'DESd.class' and name != 'DESe.class' and name != 'Blowd.class' and name != 'Blowe.class':
			fullname = os.path.join(path, name)
			x=os.path.getsize(fullname)
			# total+=x
			l = len(root)
			fullname = fullname[l:]
			cliName.append(fullname)
			# print(fullname)
			hash = hashlib.md5(open(fullname,'rb').read()).hexdigest()
			climd5.append(hash)
			cliSize.append(x)

r = s.post("http://"+url+"/list_files.php",timeout=timeout)
result = r.text.split('|')
id = result[0::4]
servName = result[1::4]
servmd5 = result[2::4]
servSize = result[3::4]

# print(servName)
# print(cliName)

server = dict(zip(servName,servmd5))
client = dict(zip(cliName,climd5))
name_id = dict(zip(servName,id))
servNameSize = dict(zip(servName,servSize))
cliNameSize = dict(zip(cliName,cliSize))

# print(server)
# print(client)

total=0
done=0

AIBsame = [] # A:client B:server
AIBdiff = []
AMB = []
BMA = [value for value in servName if value not in cliName]
for value in BMA:
	total+=int(servNameSize[value])
for value in cliName:
	if value in servName:
		if server[value]==client[value]:
			AIBsame.append(value)
		else:
			AIBdiff.append(value)
	else:
		AMB.append(value)
		total+=cliNameSize[value]

ans = input("Do you want to update the files present on server or on the computer?(server or computer) ")
# print(ans)

schema = input('Which schema are you using?(AES or DES or BLOWFISH) ')
confirm = input('Are you sure?(yes or no) ')

if confirm == "no" or confirm == "n":
	exit('Check first!')

if schema != "BLOWFISH" and schema != "AES" and schema != "DES":
	exit("Unknown schema")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	if total == 0:
		r = s.post("http://"+url+"/end_sync.php")
		exit("Sync completed successfully!")
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r',flush=True)

def func(id,path,hash):
	if path[-1]=='/':
		try:
			os.makedirs(path)
			print("Creating directory "+path)
			return
		except OSError:
			print(path+" already exists")
			return
	x = path.rfind("/")
	dirName = path[:x+1]
	try:
		os.makedirs(dirName)
		print("Creating directory "+dirName+"\n"+"Downloading "+path.split('/')[-1])
		url1 = "http://"+url+"/linux_get_file.php?id=" + str(id)
		# payload = {'key':key,'submit':True}
		r = s.post(url1,timeout=timeout)
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
	except OSError:
		print("Downloading "+path.split('/')[-1]);
		url1 = "http://"+url+"/linux_get_file.php?id=" + str(id)
		# payload = {'key':key,'submit':True}
		r = s.post(url1,timeout=timeout)
		open(path, 'wb').write(r.content)
		# os.system('python '+home+'/ch9_decrypt_blob.py '+path)
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

r = s.post("http://"+url+"/start_sync.php")

if ans=='server' or ans=='Server':
	for name in AIBdiff:
		total+=cliNameSize[name]
	for name in AIBdiff:
		print("Updating file present on server "+name)
		if os.path.isdir(name):
			# md5sum = client[name]
			if name[-1]!='/':
				name=name+'/'
			data = {'path':name,'md5sum':'','submit':True}
			r = s.post("http://"+url+"/up_linux.php", data = data,timeout=timeout)
			printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
		else:
			if schema == "AES":
				os.system('javac -d . '+home+'/AES/Cryptoe.java')
				os.system('java Cryptoe '+name)
			elif schema == "DES":
				os.system('javac -d . '+home+'/DES/DESe.java')
				os.system('java DESe '+name)
			elif schema == "BLOWFISH":
				os.system('javac -d . '+home+'/Blowfish/Blowe.java')
				os.system('java Blowe '+name)
			md5sum = client[name]
			files = {'uploaded_file': open(name,'rb')}
			data = {'path': name,'md5sum':md5sum,'submit': True}
			r = s.post("http://"+url+"/up_linux.php", files = files, data = data,timeout=timeout)
			if r.text.split("\n")[0] == hashlib.md5(open(name,'rb').read()).hexdigest():
				print("VERIFIED")
			else:
				print("WRONG UPLOAD. Try again later.")
			if schema == "AES":
				os.system('javac -d . '+home+'/AES/Cryptod.java')
				os.system('java Cryptod '+name)
			elif schema == "DES":
				os.system('javac -d . '+home+'/DES/DESd.java')
				os.system('java DESd '+name)
			elif schema == "BLOWFISH":
				os.system('javac -d . '+home+'/Blowfish/Blowd.java')
				os.system('java Blowd '+name)
			done+=cliNameSize[name]
			printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
elif ans=='computer' or ans=='Computer':
	for name in AIBdiff:
		total+=int(servNameSize[name])
	for name in AIBdiff:
		func(name_id[name],name,server[name])
		done+=int(servNameSize[name])
		printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)

for name in BMA:
	func(name_id[name],name,server[name])
	done+=int(servNameSize[name])
	printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
for name in AMB:
	print("Uploading file on server "+name)
	if os.path.isdir(name):
		if name[-1]!='/':
			name+='/'
		data = {'path':name, 'md5sum':'', 'submit':True}
		r = s.post("http://"+url+"/up_linux.php", data = data,timeout=timeout)
		printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
	else:
		# os.system('python '+home+'/ch9_encrypt_blob.py '+name)
		if schema == "AES":
			os.system('javac -d . '+home+'/AES/Cryptoe.java')
			os.system('java Cryptoe '+name)
		elif schema == "DES":
			os.system('javac -d . '+home+'/DES/DESe.java')
			os.system('java DESe '+name)
		elif schema == "BLOWFISH":
			os.system('javac -d . '+home+'/Blowfish/Blowe.java')
			os.system('java Blowe '+name)
		md5sum = client[name]
		files = {'uploaded_file': open(name,'rb')}
		data = {'path': name, 'md5sum':md5sum, 'submit': True}
		r = s.post("http://"+url+"/up_linux.php", files = files, data = data,timeout=timeout)
		if r.text.split("\n")[0] == hashlib.md5(open(name,'rb').read()).hexdigest():
			print("VERIFIED")
		else:
			print("WRONG UPLOAD. Try again later.")
		# os.system('python '+home+'/ch9_decrypt_blob.py '+name)
		if schema == "AES":
			os.system('javac -d . '+home+'/AES/Cryptod.java')
			os.system('java Cryptod '+name)
		elif schema == "DES":
			os.system('javac -d . '+home+'/DES/DESd.java')
			os.system('java DESd '+name)
		elif schema == "BLOWFISH":
			os.system('javac -d . '+home+'/Blowfish/Blowd.java')
			os.system('java Blowd '+name)
		done+=cliNameSize[name]
		printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)

r = s.post("http://"+url+"/end_sync.php")

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

print("Sync completed successfully")