# SPC (Secure Personal Cloud)

## Description
This directory contains the source-code for the clients(`Files/`) and server(`server/`) of SPC.

3 encryption schemas are used for the encryption: AES, DES and Blowfish. The files for the same are present in respective directories.

The Linux commands can be installed from `commands/` directory.

## Features
### User
1. Set server's address
2. User Login
3. User Logout

### Data
1. Upload files to server
2. Download files from server
3. Compare files available on client and server side
4. Sync files available on client and server side

Sync asks the user to update the server or the client in case common files.

## Encryptiom
1. Change Encryption key
2. Change Encryption Schema

For further usage, use `man spc`.