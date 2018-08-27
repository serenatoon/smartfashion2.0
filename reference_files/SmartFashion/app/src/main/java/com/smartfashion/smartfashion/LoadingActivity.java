package com.smartfashion.smartfashion;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;

import static com.smartfashion.smartfashion.CameraActivity.status;

public class LoadingActivity extends AppCompatActivity {

    private Timer autoUpdate;
    TextView textView;

    @Override
    public void onResume() {
        super.onResume();
        autoUpdate = new Timer();
        autoUpdate.schedule(new TimerTask() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    public void run() {
                        textView.setText(status);
                        //goToResults();
                        if (status.equals("accepted")){
                            status = "finished";
                            goToResults();
                        }else if(status.equals("error")){
                            status = "clean";
                            goToMain();
                        }
                    }
                });
            }
        }, 0, 1000); // updates each 40 secs
    }

    @Override
    public void onPause() {
        autoUpdate.cancel();
        super.onPause();
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);
        textView = (TextView) findViewById(R.id.textView);
        textView.setText(status);
    }

    public  void goToResults(){
        onPause();
        Intent intent =  new Intent(this, ResultsActivity.class);
        startActivity(intent);
    }

    public void cancelQuery(View view){
        onPause();
        Toast.makeText(this, "Cancel Clicked", Toast.LENGTH_SHORT).show();
        new CanelQuery().execute();
        Intent intent =  new Intent(this, CameraActivity.class);
        startActivity(intent);
    }

    public void goToMain(){
        Toast.makeText(this, "oops something went wrong", Toast.LENGTH_SHORT).show();
        Intent intent =  new Intent(this, CameraActivity.class);
        startActivity(intent);
    }

    class CanelQuery extends AsyncTask<Void, Void, String> {

        private Exception exception;

        protected void onPreExecute() {

        }

        public String doInBackground(Void... urls) {
            try {

                JSONObject json = new JSONObject();
                json.put("device_ID", CameraActivity.DEVICE_ID);
                json.put("password", CameraActivity.SERVER_PASSWORD);
                URL url = new URL(CameraActivity.API_URL + CameraActivity.CLOSE);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setDoOutput(true);
                urlConnection.setRequestProperty("Content-Type", "application/json");
                urlConnection.setRequestProperty("Accept", "application/json");
                urlConnection.setRequestMethod("POST");
                urlConnection.connect();
                try {
                    String data = json.toString();

                    //Write
                    OutputStream outputStream = urlConnection.getOutputStream();
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));
                    writer.write(data);
                    writer.close();
                    outputStream.close();

                    //Read
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;
                    while ((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line);
                    }
                    bufferedReader.close();
                    return stringBuilder.toString();

                }
                finally{
                    urlConnection.disconnect();
                }
            }
            catch(Exception e) {
                Log.e("ERROR", e.getMessage(), e);
                return null;
            }
        }

        protected void onPostExecute(String response)  {
            if(response == null) {
                response = "THERE WAS AN ERROR";
                goToMain();
            }
            //progressBar.setVisibility(View.GONE);
            Log.i("INFO", response);
            try{
                JSONObject object = new JSONObject(response);
                String responseText = object.get("status").toString();
                status = responseText;
                //responseView.setText(responseText);
            } catch (JSONException jsonLit){
                status = "error";
                goToMain();
                // responseView.setText("EXCEPTION DUN DUN DUN: " + response);
            }
        }
    }
}
