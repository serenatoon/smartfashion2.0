package com.smartfashion.smartfashion;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class CameraActivity extends AppCompatActivity {

    private static final int ACTIVITY_START_CAMERA_APP = 0;
    private ImageView mPhotCapuredImageView;
    private String encodedImage;
    private Bitmap bmp;
    private Bitmap photoCapturedBitmap;
    TextView responseView;

    ProgressBar progressBar;

    public static String status = "";

    //Class local variables
    private boolean img_flag = false;
    private String nextGender;

    //Device Variables
    final static String DEVICE_ID = android.os.Build.MODEL;
    final static String SERVER_PASSWORD = "nadeem";

    //API CALLS
    final static String API_URL = "http://irasyamira.pythonanywhere.com/";
    final static String PING = "ping";
    final static String PASSWORD = "passwordTest";
    final static String JSON = "randomJson";
    final static String QUERY = "startQuery";
    final static String CLOSE = "closeQuery";
    final static String STATUS = "getStatusUpdate";
    final static String SET_IMAGE = "setImage";
    final static String GET_RESULT = "getResult";
    final static String GET_IMAGE = "getImage";

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);

        Button gender_button = (Button)findViewById(R.id.genderButton);
        nextGender = gender_button.getText().toString();

        mPhotCapuredImageView = (ImageView) findViewById(R.id.capturePhotoImageView);
        responseView = (TextView) findViewById(R.id.responseView);
        progressBar = (ProgressBar) findViewById(R.id.progressBar);

        responseView.setVisibility(View.INVISIBLE);
        progressBar.setVisibility(View.INVISIBLE);

    }

    public void takePhoto(View view){
        Intent callCameraApplicationIntent = new Intent();
        callCameraApplicationIntent.setAction(MediaStore.ACTION_IMAGE_CAPTURE);
        startActivityForResult(callCameraApplicationIntent, ACTIVITY_START_CAMERA_APP);
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        if(requestCode == ACTIVITY_START_CAMERA_APP && resultCode == RESULT_OK){
            Bundle extras =data.getExtras();
            photoCapturedBitmap = (Bitmap) extras.get("data");
            mPhotCapuredImageView.setImageBitmap(photoCapturedBitmap);
            img_flag = true;
            //Toast.makeText(this, "Picture Taken", Toast.LENGTH_SHORT).show();
        }
    }

    /** Called when the user taps the Send button */
    public void sendImage(View view) {
        if (img_flag ){
            new StartQuery().execute();
            /*mPhotCapuredImageView.setVisibility(View.INVISIBLE);
            responseView.setVisibility(View.VISIBLE);
            progressBar.setVisibility(View.VISIBLE);*/

            Intent intent =  new Intent(this, LoadingActivity.class);
            startActivity(intent);
        }else{
            Toast.makeText(this, "Please take an image before sending", Toast.LENGTH_SHORT).show();
        }
    }

    /** Called when the user taps the Gender button */
    public void cycleGender(View view) {
        Button gender_button = (Button)findViewById(R.id.genderButton);
        String currentGender = gender_button.getText().toString();
        nextGender = getNextGender(currentGender);
        gender_button.setText(nextGender);
    }

    private String getNextGender(String gender){
        switch (gender){
            case "Male"     : return "Female";
            case "Female"   : return "Male";
            default         : return "Female";
        }
    }

    class StartQuery extends AsyncTask<Void, Void, String> {
        private Exception exception;
        protected void onPreExecute() {
            bmp = photoCapturedBitmap;
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            bmp.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArrayImage = stream.toByteArray();
            encodedImage = Base64.encodeToString(byteArrayImage, Base64.DEFAULT);
            Log.d("IMG Array", encodedImage);
        }
        public String doInBackground(Void... urls) {
            try {
                JSONObject json = new JSONObject();

                json.put("device_ID", DEVICE_ID);
                json.put("password", SERVER_PASSWORD);
                json.put("image_array", encodedImage);
                json.put("gender", nextGender );
                URL url = new URL(API_URL + QUERY);
                Log.d("url", url.toString());
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                Log.d("urlConnection", urlConnection.toString());
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
                    //responseView.setText("i cry");
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
            }
            //progressBar.setVisibility(View.GONE);
            Log.i("INFO", response);
            try{
                JSONObject object = new JSONObject(response);
                String responseText = object.get("status").toString();
                status = responseText;
                responseView.setText(responseText);
            } catch (JSONException jsonLit){
                status = "error";
                responseView.setText("EXCEPTION DUN DUN DUN: " + response);
            }
        }
    }


}
