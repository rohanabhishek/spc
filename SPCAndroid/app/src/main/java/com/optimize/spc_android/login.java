package com.optimize.spc_android;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
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
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class login extends AppCompatActivity {

    EditText username;
    EditText password;
    EditText url;
    EditText schema;
    EditText key;
    Button btn;
    static ArrayList<String> userslist  = new ArrayList<String>();

    class GetUsernames extends AsyncTask<Void, Void, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            userslist.clear();
        }

        @Override
        protected String doInBackground(Void... voids) {
            try {
                String POST_URL = "http://"+url.getText()+"/exist.php";
                String POST_PARAMS = "username="+username.getText()+"&password="+password.getText()+"&submit=True";

                URL obj = new URL(POST_URL);
                HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                con.setRequestMethod("POST");
                con.setDoOutput(true);
                OutputStream os = con.getOutputStream();
                os.write(POST_PARAMS.getBytes());
                os.flush();
                os.close();
                int responseCode = con.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(
                            con.getInputStream()));
                    String inputLine;
                    StringBuffer response = new StringBuffer();

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();
                    String out = response.toString();
                    if(out.indexOf("True")!=-1){
                        return "Yes";
                    }
                    else{
                        return "No";
                    }
                } else {
                    return "POST request not worked";
                }
            }
            catch(Exception e){
                return "";
            }
        }

        @Override
        public void onPostExecute(String s){
            try{
                if(s=="Yes"){
                    Intent intent = new Intent(login.this, mainpage.class);
                    intent.putExtra("username",(username.getText()).toString());
                    intent.putExtra("password",(password.getText()).toString());
                    intent.putExtra("url",(url.getText()).toString());
                    intent.putExtra("schema",(schema.getText()).toString());
                    intent.putExtra("key",(key.getText()).toString());
                    startActivity(intent);
                }
                else{
                    Toast tf = Toast.makeText(login.this,"Wrong credentials",Toast.LENGTH_LONG);
                    tf.show();
                }
            }
            catch (Exception e){
                e.printStackTrace();
                Toast t = Toast.makeText(login.this,"Enter a username",Toast.LENGTH_LONG);
                t.show();
            }
        }
    }
    private View.OnClickListener myListener = new View.OnClickListener() {
        public void onClick(View v) {
            new GetUsernames().execute();

        }
    };
    //    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        username = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        url = (EditText) findViewById(R.id.url);
        schema = (EditText) findViewById(R.id.schema);
        key = (EditText) findViewById(R.id.key);
        btn = (Button) findViewById(R.id.button);
        btn.setOnClickListener(myListener);

    }
}