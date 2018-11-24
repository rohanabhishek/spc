import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;
import java.util.Base64;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;
import java.io.FileWriter;


public class Cryptoe {

   static void fileProcessor(int cipherMode,String key,File inputFile,File outputFile){
	 try {
	 		// System.out.println("Success1");
	       Key secretKey = new SecretKeySpec(key.getBytes(), "AES");
	       // System.out.println(secretKey);
	       Cipher cipher = Cipher.getInstance("AES");
	       cipher.init(cipherMode, secretKey);
	       // System.out.println("Success1");
	       FileInputStream inputStream = new FileInputStream(inputFile);
	       byte[] inputBytes = new byte[(int) inputFile.length()];
	       inputStream.read(inputBytes);

	       byte[] outputBytes = cipher.doFinal(inputBytes);
	       // System.out.println("Success1");
	       FileOutputStream outputStream = new FileOutputStream(outputFile);
	       outputStream.write(outputBytes);

	       inputStream.close();
	       outputStream.close();

	    } catch (NoSuchPaddingException | NoSuchAlgorithmException 
                     | InvalidKeyException | BadPaddingException
	             | IllegalBlockSizeException | IOException e) {
		e.printStackTrace();
            }
     }
	
     public static void main(String[] args) throws FileNotFoundException{
	// String key = "This is a secret";
     	String home = System.getProperty("user.home");
	//System.out.println(home);
     	File file = new File(home+"/SPC/AES/aeskey.txt");
     	String key;
     	key = new Scanner(file).useDelimiter("\\A").next();	
     	// key = key.substring(0,Math.min(key.length(),16));
     	key = key.substring(0,16);
     	//System.out.print(key);
		File inputFile = new File(args[0]);
		File encryptedFile = new File(args[0]);
		// File decryptedFile = new File("decrypted-textbynow.jpg");
			
		try {
		     Cryptoe.fileProcessor(Cipher.ENCRYPT_MODE,key,inputFile,encryptedFile);
		     // Crypto.fileProcessor(Cipher.DECRYPT_MODE,key,encryptedFile,decryptedFile);
		     // System.out.println("Susccess");
		 } catch (Exception ex) {
		     // System.out.println(ex.getMessage());
	             ex.printStackTrace();
		 }
	     
	     String encodedBase64 = null;
        try {

            FileInputStream fileInputStreamReader = new FileInputStream(encryptedFile);
            byte[] bytes = new byte[(int)encryptedFile.length()];
            fileInputStreamReader.read(bytes);
            // encodedBase64 = new String(Base64.encodeBase64(bytes));
            encodedBase64 = new String(Base64.getEncoder().encode(bytes));
            fileInputStreamReader.close();
            FileWriter fw = new FileWriter(encryptedFile);
            fw.write(encodedBase64);
            fw.flush();
			fw.close();
            // System.out.println(encodedBase64);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

	
}
}

