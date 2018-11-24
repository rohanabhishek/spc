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

public class Blowe {
	
	private static final String ALGORITHM = "Blowfish";
	private static String keyString;


	public static void encrypt(File inputFile, File outputFile)
			throws Exception {
		doCrypto(Cipher.ENCRYPT_MODE, inputFile, outputFile);
		// System.out.println("File encrypted successfully!");
	}

	// public static void decrypt(File inputFile, File outputFile)
	// 		throws Exception {
	// 	doCrypto(Cipher.DECRYPT_MODE, inputFile, outputFile);
	// 	// System.out.println("File decrypted successfully!");
	// }

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
		
		// File inputFile = new File("test.txt");
		// File encryptedFile = new File("test.encrypted");
		
		// File decryptedFile = new File("test.decrypted");
		String home = System.getProperty("user.home");
		//System.out.println(home);
     	File file = new File(home+"/SPC/Blowfish/bkey.txt");
		// File file = new File("bkey.txt");
		     	// String key;
		keyString = new Scanner(file).useDelimiter("\\A").next();
		keyString = keyString.substring(0,keyString.length()-1);
		String filename = new String();
		filename = args[0];
		File inputFile = new File(filename);
		File encryptedFile = new File(filename + ".tmp");
		try {
			Blowe.encrypt(inputFile, encryptedFile);
			// TestFileEncryption.decrypt(encryptedFile, decryptedFile);
			inputFile.delete();
			String encodedBase64 = null;
	   

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
	   
			File file2 = new File(filename+".tmp");
	        file2.renameTo(inputFile);

		} catch (Exception e) {
			e.printStackTrace();
		}
		
		
	}
}
