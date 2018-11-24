import sys
import os

home = os.path.expanduser('~')

if len(sys.argv) == 1:
	# print("Yes")
	os.system("spc --help")
	exit()

arg1 = sys.argv[1]

if arg1 == "sync" :
	if len(sys.argv) != 2:
		os.system("python3 "+home+"/SPC/Files/sync.py " + sys.argv[2])
	else:
		print("Provide file or directory path")
	exit()

elif arg1 == "status":
	if len(sys.argv) != 2:
		os.system("python3 "+home+"/SPC/Files/compare.py " + sys.argv[2])
	else:
		print("Provide file or directory path")
	exit()
	
elif arg1 == "en-de":
	if len(sys.argv) == 2:
		os.system("spc --help")
		exit()
	arg2 = sys.argv[2]
	if arg2 == "list":
		print("Supported encryption schemes are :-")
		print("1.AES (Advanced Encryption Standard)")
		print("2.DES (Data Encryption Standard)")
		print("3.BLOWFISH")
		exit()
	elif arg2 == "update":
		# schema = input("Schema used: ")
		# if schema == "RSA" :
		# 	key1 = input("Public Key: ")
		# 	key2 = input("Private Key: ")
		# 	#Change the keys
		# elif schema == "AES" or schema == "DES" :
		# 	key = input("Key: ")
		# 	f = open(""+home+"/SPC/" +schema+"/"+schema.lower()+"key.txt","w")
		# 	f.write(key)
		# 	f.close()
		# else:
		# 	os.system("spc --help")
		# 	exit()
		if len(sys.argv) == 3:
			os.system("python3 "+home+"/SPC/Files/change_schema.py")
			exit()
		else:
			arg3 = sys.argv[3]
			os.system("python3 "+home+"/SPC/Files/changekey.py " + arg3)
			exit()

	elif arg2 == "dump":
		if len(sys.argv) == 3:
			print("Please provide the file path without any spaces")
			exit()
		else:
			arg3 = sys.argv[3]
			Confirm = input("Do you want to print key? (yes or no): ")
			if Confirm == "y" or Confirm == "yes":
				os.system("touch arg3");
				outschema = input("Schema used: ")
				if outschema == "BLOWFISH":
					os.system("cp "+home+"/SPC/Blowfish/bkey.txt " + arg3)
					os.system("cat "+home+"/SPC/Blowfish/bkey.txt")
				elif outschema == "AES" or outschema == "DES" :
					os.system("cp "+home+"/SPC/" + outschema +"/"+outschema.lower()+"key.txt " + arg3)
					os.system("cat "+home+"/SPC/" + outschema +"/"+outschema.lower()+"key.txt")
				else:
					print("Please select one among the schema")
					os.system("spc en-de list")
				exit()
			else:
				os.system("touch " + arg3);
				outschema = input("Schema used: ")
				if outschema == "BLOWFISH":
					os.system("cp "+home+"/SPC/Blowfish/bkey.txt " + arg3)
					# os.system("cat "+home+"/SPC/Blowfish/bkey.txt " + arg3)
				elif outschema == "AES" or outschema == "DES" :
					os.system("cp "+home+"/SPC/" + outschema +"/"+outschema.lower()+"key.txt " + arg3)
					# os.system("cat "+home+"/SPC/" + outschema +"/"+schema.lower()+"key.txt")
				else:
					print("Please select one among the schema")
					os.system("spc en-de list")
				exit()

else :
	print("spc: '"+ arg1 + "' is not a spc command. See 'spc help' or 'spc --help'.")