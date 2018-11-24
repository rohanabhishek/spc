package com.optimize.spc_android;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;

import android.support.v7.app.AppCompatActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDate;
import java.time.Month;
import java.time.Period;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import static java.lang.Integer.parseInt;

public class mainpage extends AppCompatActivity {
    String username;
    String password;
    String url1;
    String schema;
    String key;

    static ArrayList<String> filenames  = new ArrayList<String>();
    static ArrayList<String> filemimes  = new ArrayList<String>();
    static ArrayList<String> fileids  = new ArrayList<String>();

    class GetInfo extends AsyncTask<Void, Void, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            filenames.clear();
            fileids.clear();
        }

        @Override
        protected String doInBackground(Void... voids) {
            HttpURLConnection urlConnection = null;
            try {
                URL url = new URL("http://"+url1+"/list_file_android.php?username=" + username + "&password="+ password);
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                urlConnection.connect();

                InputStream is = urlConnection.getInputStream();
                if(is == null){
                    return "Rohan from ret 1";
                }
                BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    sb.append(line + "\n");
                }
                br.close();
                return sb.toString();
            }
            catch (ProtocolException e) {
                e.printStackTrace();
                return "h1";
            }
            catch (MalformedURLException e) {
                e.printStackTrace();
                return "h2";
            }
            catch (IOException e) {
                e.printStackTrace();
                return "http://"+url1+"/list_file_android.php?username=" + username + "&password="+ password;
            }
        }

        @Override
        public void onPostExecute(String s){
            try{
                String[] arrOfStr = s.split(" ");
                String msg = new String();
                for(int x=1;x<arrOfStr.length;x+=2){
                    filenames.add(arrOfStr[x]+" "+arrOfStr[x-1]);
                }
                ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(mainpage.this, R.layout.preview,R.id.text1,filenames);
                ListView listView = (ListView) findViewById(R.id.list);
                listView.setAdapter(itemsAdapter);
                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        String val = ((TextView)view).getText().toString().split(" ")[1];
                        try {
                            URL url = new URL("http://"+url1+"/get_content_android.php?username=" + username + "&password=" + password + "&id=" + val + "&schema=" + schema +"&key=" +key);
                            Intent intent = new Intent(Intent.ACTION_VIEW);
                            intent.setData(Uri.parse(url.toString()));
                            startActivity(intent);
                        }
                        catch(Exception e){
                            e.printStackTrace();
                        }
                    }
                });
            }
            catch (Exception e){
                e.printStackTrace();
                Toast t = Toast.makeText(mainpage.this,"Rohan from last tut",Toast.LENGTH_LONG);
                t.show();
            }
        }
    }
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_mainpage);
        Bundle extras = getIntent().getExtras();
        username=extras.getString("username");
        password=extras.getString("password");
        url1=extras.getString("url");
        schema=extras.getString("schema");
        key=extras.getString("key");
        new GetInfo().execute();
    }
}