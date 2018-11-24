import os

home = os.path.expanduser('~/SPC/Pickles/session.pkl')
if os.path.isfile(home):
	os.remove(home)
	print("Successfully logged out")
else:
	print("You are already logout")

# home = os.path.expanduser('~')

# if os.path.isfile(home+'/url.pkl'):
# 	fp = open(home+'/url.pkl','rb')
# 	url = pickle.load(fp)
# else:
# 	print("First set the server-url")
# 	exit()
