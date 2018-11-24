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

home = os.path.expanduser('~/SPC')
# print(home)
if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

if len(sys.argv) != 2:
	exit("Provide file or directory path")

root = sys.argv[1]
root = os.path.abspath(root)
if os.path.isfile(home+'/Pickles/session.pkl'):
	fp = open(home+'/Pickles/session.pkl','rb')
	cred = pickle.load(fp)
	usrnm = cred[0]
	passwd = cred[1]
else:
	usrnm = input('Enter username: ')
	passwd = getpass.getpass(prompt='Enter password: ',stream=None)
# print("Done")
# print(usrnm)
# print(passwd)

payload = {'username':usrnm,'password':passwd,'submit':'Submit'}
s = requests.session()
# home = os.path.expanduser('~')
# fp = open(home+'/session.pkl','rb')
# s = pickle.load(fp)
r = s.post("http://"+url+"/login.php", data = payload)
# print(r.text)
# print("Yes")
if 'logout.php' in r.text:
	print("Starting upload for user: "+usrnm)
	print("")
else:
	exit("Invalid user -- Please try again")
# print("Valid")
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r',flush=True)
    # Print New Line on Complete
    if iteration == total: 
        print()

schema = input('Which schema are you using?(AES or DES or BLOWFISH) ')
confirm = input('Are you sure?(yes or no) ')

if confirm == "no" or confirm == "n":
	exit('Check first.')

if schema != "BLOWFISH" and schema != "AES" and schema != "DES":
	exit("Unknown schema")

total=0
done=0
# print(root)
if not os.path.isdir(root):
	# # print(root)
	# name = root.rsplit('/', 1)[-1]
	# md5sum = hashlib.md5(open(root,'rb').read()).hexdigest()
	# data = {'path':name,'md5sum':md5sum,'submit':True}
	# # print("Yes")
	# print("Uploading "+name+" "+md5sum+"\033[K")
	# if schema == "AES":
	# 	os.system('javac -d . '+home+'/AES/Cryptoe.java')
	# 	os.system('java Cryptoe '+root)
	# files = {'uploaded_file': open(root,'rb')}
	# r = s.post("http://"+url+"/up_linux.php", files = files, data = data)
	# # print(r.text)
	exit("It is not a directory")
elif os.path.isdir(root):
	if root[-1]!='/':
		root = root+"/"
	os.chdir(root)
	for path, subdirs, files in os.walk(root):
		for name in files:
			fullname = os.path.join(path, name)
			x=os.path.getsize(fullname)
			total+=x
	for path, subdirs, files in os.walk(root):
		if len(files)==0 and len(subdirs)==0:
			fullname = os.path.join(path)
			l = len(root)
			fullname = fullname[l:] + '/'
			# fullname = fullname+'/'
			# files = {'uploaded_file': open(fullname,'rb')}
			# hash = hashlib.md5(open(fullname,'rb').read()).hexdigest()
			data = {'path':fullname,'md5sum':'','submit':True}
			# # print("Yes")
			print("Uploading "+fullname+"\033[K")
			r = s.post("http://"+url+"/up_linux.php", data = data)
			# print(r.txt)
			printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
			# print(r.text)
		for name in files:
			if name != 'Cryptod.class' and name != 'Cryptoe.class' and name != 'DESd.class' and name != 'DESe.class' and name != 'Blowd.class' and name != 'Blowe.class':
				fullname = os.path.join(path, name)
				# print(fullname)
				l = len(root)
				# print(l)
				fullname = fullname[l:]
				# x = fullname.find(root)
				# print(fullname)
				# print(x)
				# print(root+fullname)
				md5sum = hashlib.md5(open(fullname,'rb').read()).hexdigest()
				print("Uploading "+fullname+" "+md5sum+"\033[K")
				done+=os.path.getsize(fullname)
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
				# os.system('python '+home+'/ch9_decrypt_blob.py '+fullname)
				# print(r.text.split("\n")[0])
				# print(hashlib.md5(open(fullname,'rb').read()).hexdigest())
				if r.text.split("\n")[0] == hashlib.md5(open(fullname,'rb').read()).hexdigest():
					print("VERIFIED")
				else:
					print("WRONG UPLOAD. Try again later.")
				if schema == "AES":
					os.system('javac -d . '+home+'/AES/Cryptod.java')
					os.system('java Cryptod '+fullname)
				elif schema == "DES":
					os.system('javac -d . '+home+'/DES/DESd.java')
					os.system('java DESd '+fullname)
				elif schema == "BLOWFISH":
					os.system('javac -d . '+home+'/Blowfish/Blowd.java')
					os.system('java Blowd '+fullname)
				printProgressBar(done,total,prefix='Uploaded:',suffix='Complete',length=50)
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

print("Total files uploaded:",total)
# print(root)
# print(os.path.abspath(root))
# for path, subdirs, files in os.walk(root):
#     for name in files:
#         print(os.path.join(path, name))

# br = Browser()
# br.open("http://192.168.0.103:8000/login.php")
# br.select_form(id="form")
# br.form.add('username'='anurag')
# br.open("http://192.168.0.103:8000/up_linux.php")
# br.select_form(name="f")
# br.form.add_file(open("slp.txt"), 'text/plain',"slp.txt")
# response = br.submit()



# url = "http://192.168.0.103:8000/login.php"

# payload = {'username':'rohit','password':'Rao12@boy','submit':True}
# s = requests.session()
# r = s.post(url, data = payload)
# r = s.post("http://192.168.0.103:8000/list_files.php")	
# print(r.text)
# result = r.text.split('|')
# id = result[0::3]
# name = result[1::3]
# md5sum = result[2::3]

# result = zip(id,name,md5sum)

# def func(id,path):
# 	path = path.replace(":","/")
# 	x = path.rfind("/")
# 	dirName = path[:x+1]
# 	try:
# 		os.makedirs(dirName)
# 		print("Creating directory "+dirName+"\n"+"Downloading "+path.split('/')[-1]);
# 		url = "http://192.168.0.103:8000/get_file.php?id=" + str(id)
# 		r = s.get(url)
# 		open(path, 'wb').write(r.content)
# 	except OSError:
# 		print("Downloading "+path.split('/')[-1]);
# 		url = "http://192.168.0.103:8000/get_file.php?id=" + str(id)
# 		r = s.get(url)
# 		open(path, 'wb').write(r.content)

# for x in result:
# 	name = x[1]
# 	name = name.replace(":","/")
# 	if os.path.isfile(name):
# 		hash = hashlib.md5(open(name,'rb').read()).hexdigest()
# 		if x[2] == hash:
# 			print(name+" already exists")
# 		elif ":" not in x[1]:
# 			print("Downloading "+x[1]+" "+str(x[0]));
# 			url = "http://192.168.0.103:8000/get_file.php?id=" + str(x[0])
# 			r = s.get(url)
# 			open(x[1], 'wb').write(r.content)
# 		else:
# 			func(x[0],name)
# 	elif ":" not in x[1]:
# 		print("Downloading "+x[1]+" "+str(x[0]));
# 		url = "http://192.168.0.103:8000/get_file.php?id=" + str(x[0])
# 		r = s.get(url)
# 		open(x[1], 'wb').write(r.content)
# 	else:
# 		func(x[0],name)
# <?php
# // Check if a file has been uploaded
# session_start();
# $username = $_SESSION['username'];
# if(isset($_FILES['uploaded_file'])) {
#     // Make sure the file was sent without errors
#     if($_FILES['uploaded_file']['error'] == 0) {
#         // Connect to the database
#         $dbLink = new mysqli('192.168.0.103', 'root', 'password', 'spcUsers');
#         if(mysqli_connect_errno()) {
#             die("MySQL connection failed: ". mysqli_connect_error());
#         }
 
#         // Gather all required data
#         $name = $dbLink->real_escape_string($_FILES['uploaded_file']['name']);
#         $mime = $dbLink->real_escape_string($_FILES['uploaded_file']['type']);
#         $data = $dbLink->real_escape_string(file_get_contents($_FILES['uploaded_file']['tmp_name']));
#         $size = intval($_FILES['uploaded_file']['size']);
#         $myhash = md5_file($_FILES['uploaded_file']['tmp_name']);
 		
#         // Create the SQL query
#         $query = "
#             INSERT INTO $username (
#                 `name`, `mime`, `size`, `data`, `created`, `md5sum`
#             )
#             VALUES (
#                 '{$name}', '{$mime}', '{$size}', '{$data}', NOW(), '{$myhash}'
#             )";
 
#         // Execute the query
#         $result = $dbLink->query($query);
 
#         // Check if it was successfull
#         if($result) {
#             echo 'Success! Your file was successfully added!';
#         }
#         else {
#         	echo $myhash;
#             echo '<br/>Error! Failed to insert the file'
#                . "<pre>{$dbLink->error}</pre>";
#         }
#     }
#     else {
#         echo 'An error accured while the file was being uploaded. '
#            . 'Error code: '. intval($_FILES['uploaded_file']['error']);
#     }
 
#     // Close the mysql connection
#     $dbLink->close();
# }
# else {
#     echo 'Error! A file was not sent!';
# }
 
# // Echo a link back to the main page
# echo '<p>Click <a href="up.php">here</a> to go back</p>';
# ?>
