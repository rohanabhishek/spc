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

home = os.path.expanduser('~/SPC/Pickles')
if len(sys.argv) != 2:
	print("Provide url as argument")
	exit()
url = sys.argv[1]

fp = open(home+'/url.pkl','wb')
pickle.dump(url,fp)
print("Connected to "+url+" successfully")