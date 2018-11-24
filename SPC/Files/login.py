import requests
import getpass
import pickle
import os
import sys
# import webbrowser
# import time
home = os.path.expanduser('~/SPC')
# print(home)
# $ip=$_SERVER['REMOTE_ADDR']

if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

url1 = "http://"+url+"/login.php"
usrnm = sys.argv[1]
passwd = sys.argv[2] 
payload = {'username':usrnm,'password':passwd,'submit':True}
s = requests.session()
# print(s.cookies)
# fetch the login page
r = s.post(url1, data = payload)
# time.sleep(10)
# url1='http://192.168.0.103:8000/list_files.php'

if 'logout.php' in r.text:
	cred = list([usrnm,passwd])
	fp = open(home+'/Pickles/session.pkl','wb')
	pickle.dump(cred,fp)
	print("Successful login -- Don't forget to logout")
	# print("Don't forget to logout")
	# r = s.post(url1)
	# print(r.text)
else:
	print("Invalid user -- Please try again")