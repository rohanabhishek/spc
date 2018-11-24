import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.Key;
import java.util.Scanner;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.util.Base64;

public class Blowd {
	
	private static final String ALGORITHM = "Blowfish";
	private static String keyString;

	// public static void encrypt(File inputFile, File outputFile)
	// 		throws Exception {
	// 	doCrypto(Cipher.ENCRYPT_MODE, inputFile, outputFile);
	// 	System.out.println("File encrypted successfully!");
	// }

	public static void decrypt(File inputFile, File outputFile)
			throws Exception {
		doCrypto(Cipher.DECRYPT_MODE, inputFile, outputFile);
		// System.out.println("File decrypted successfully!");
	}

	private static void doCrypto(int cipherMode, File inputFile,
			File outputFile) throws Exception {

		Key secretKey = new SecretKeySpec(keyString.getBytes(), ALGORITHM);
		Cipher cipher = Cipher.getInstance(ALGORITHM);
		cipher.init(cipherMode, secretKey);

		FileInputStream inputStream = new FileInputStream(inputFile);
		byte[] inputBytes = new byte[(int) inputFile.length()];
		inputStream.read(inputBytes);

		byte[] outputBytes = cipher.doFinal(inputBytes);

		FileOutputStream outputStream = new FileOutputStream(outputFile);
		outputStream.write(outputBytes);

		inputStream.close();
		outputStream.close();

	}

	public static void main(String[] args) throws Exception{
		// File decryptedFile = new File("test.decrypted");
		// File file = new File("bkey.txt");
		// String home = System.getProperty("user.home");
		//System.out.println(home);
     	File file = new File("bkey.txt");
		     	// String key;
		keyString = new Scanner(file).useDelimiter("\\A").next();
		keyString = keyString.substring(0,keyString.length()-1);
		String filename = new String();
		filename = args[0];
		File inputFile = new File(filename);
		// File inputFile = new File("test.encrypted");
		
		File decryptedFile = new File(filename + ".tmp");

		try {
			// TestFileEncryption.encrypt(inputFile, inputFile);
			

            FileInputStream fileInputStreamReader = new FileInputStream(inputFile);
            byte[] bytes = new byte[(int)inputFile.length()];
            fileInputStreamReader.read(bytes);
            // encodedBase64 = new String(Base64.encodeBase64(bytes));
            byte [] encodedBase64 = Base64.getDecoder().decode(new String(bytes));
            fileInputStreamReader.close();
            FileOutputStream stream = new FileOutputStream(inputFile);
		
		    stream.write(encodedBase64);
		
		    stream.close();
			
			Blowd.decrypt(inputFile, decryptedFile);
			inputFile.delete();
			File file2 = new File(filename+".tmp");
	        file2.renameTo(inputFile);

		} catch (Exception e) {
			e.printStackTrace();
		}
		
		
	}
}
