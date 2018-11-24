import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.spec.AlgorithmParameterSpec;

import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.CipherOutputStream;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;




import java.security.SecureRandom; 
import java.security.spec.KeySpec; 

import javax.crypto.Cipher; 
import javax.crypto.KeyGenerator; 
import javax.crypto.SecretKey; 
import javax.crypto.SecretKeyFactory; 
import javax.crypto.spec.DESKeySpec; 


import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.util.Scanner;

import java.io.IOException;
import java.io.FileNotFoundException;

public class DESd {
	// private static Cipher encryptCipher;
	private static Cipher decryptCipher;
	private static final byte[] iv = { 11, 22, 33, 44, 99, 88, 77, 66 };

	public static void main(String[] args) {

		try {
			// create SecretKey using KeyGenerator
			KeyGenerator gen = KeyGenerator.getInstance("DES");
			gen.init(56);
			SecretKey key = gen.generateKey();
			
			String filename = new String();
			filename = args[0];
			String myEncryptionKey = new String();
			// System.out.println(args.length);
	     	// for(int i=1;i<args.length-1;i++){
	     	// 	myEncryptionKey = args[i] + " ";
	     	// }
	     	// myEncryptionKey += args[args.length-1];

	     	String home = System.getProperty("user.home");
			//System.out.println(home);
		    File file = new File(home+"/SPC/DES/deskey.txt");
		    // String key;
		    myEncryptionKey = new Scanner(file).useDelimiter("\\A").next();	
		    // myEncryptionKey = myEncryptionKey.substring(0,myEncryptionKey.length()-1);
	     	
			// File inputFile = new File(filename);
			File encryptedFile = new File(filename);

			String UNICODE_FORMAT = "UTF8";
			KeySpec myKeySpec; 
			SecretKeyFactory mySecretKeyFactory; 
			Cipher cipher; 


			try{
				byte[] keyAsBytes;  
				keyAsBytes = myEncryptionKey.getBytes("UTF8");
				myKeySpec = new DESKeySpec(keyAsBytes); 
				mySecretKeyFactory = SecretKeyFactory.getInstance("DES"); 
				cipher = Cipher.getInstance("DES"); 
				key = mySecretKeyFactory.generateSecret(myKeySpec); 
			}
			catch (Exception e){
				// System.out.println("Catch");
				e.printStackTrace();
			}

			AlgorithmParameterSpec paramSpec = new IvParameterSpec(iv);




			// get Cipher instance and initiate in decrypt mode
			decryptCipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
			decryptCipher.init(Cipher.DECRYPT_MODE, key, paramSpec);


			 try {	

            FileInputStream fileInputStreamReader = new FileInputStream(encryptedFile);
            byte[] bytes = new byte[(int)encryptedFile.length()];
            fileInputStreamReader.read(bytes);
            // encodedBase64 = new String(Base64.encodeBase64(bytes));
            byte [] encodedBase64 = Base64.getDecoder().decode(new String(bytes));
            fileInputStreamReader.close();
            FileOutputStream stream = new FileOutputStream(encryptedFile);
			try {
			    stream.write(encodedBase64);
			} finally {
			    stream.close();
			}
			// System.out.println(bytes.length);
   //          FileWriter fw = new FileWriter(encryptedFile);
   //          fw.write(encodedBase64);
   //          fw.flush();
			// fw.close();
            // System.out.println(encodedBase64);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }






			
			decrypt(new FileInputStream(filename), new FileOutputStream(filename + ".tmp"));
			// File file1 = new File(filename);
	        encryptedFile.delete();
	        File file2 = new File(filename+".tmp");
	        file2.renameTo(encryptedFile);

			// System.out.println("DONE");
		} catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException
				| InvalidAlgorithmParameterException | IOException e) {
			e.printStackTrace();
		}

	}

	// private static void encrypt(InputStream is, OutputStream os) throws IOException {

	// 	// create CipherOutputStream to encrypt the data using encryptCipher
	// 	os = new CipherOutputStream(os, encryptCipher);
	// 	writeData(is, os);
	// }

	private static void decrypt(InputStream is, OutputStream os) throws IOException {

		// create CipherOutputStream to decrypt the data using decryptCipher
		is = new CipherInputStream(is, decryptCipher);
		writeData(is, os);
	}

	// utility method to read data from input stream and write to output stream
	private static void writeData(InputStream is, OutputStream os) throws IOException {
		byte[] buf = new byte[1024];
		int numRead = 0;
		// read and write operation
		// System.out.println("Rohan");
		while ((numRead = is.read(buf)) >= 0) {
			// System.out.println("Rohan");
			
			os.write(buf, 0, numRead);
		}
		os.close();
		is.close();
	}

}

