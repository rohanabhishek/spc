import os
import pickle

home = os.path.expanduser('~/SPC')
if os.path.isfile(home+'/Pickles/url.pkl'):
	fp = open(home+'/Pickles/url.pkl','rb')
	url = pickle.load(fp)
else:
	exit("First set the server-url")

print("IP: "+url[:-5])