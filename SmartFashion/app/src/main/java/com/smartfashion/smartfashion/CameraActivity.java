package com.smartfashion.smartfashion;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import android.net.Uri;
import android.os.Environment;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;


public class CameraActivity extends AppCompatActivity {
    public static final int MEDIA_TYPE_IMAGE = 1;
    public static final int MEDIA_TYPE_VIDEO = 2;
    String imageFilePath;

    private static final int ACTIVITY_START_CAMERA_APP = 0;
    private static final int PICK_IMAGE_REQUEST = 100;
    private ImageView mPhotCapuredImageView;
    private String encodedImage;
    private Bitmap bmp;
    private Bitmap photoCapturedBitmap;
    TextView responseView;
    private ImageView galleryView;

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
        // savedInstanceState is non-null when there is fragment state
        // saved from previous configurations of this activity
        // (e.g. when rotating the screen from portrait to landscape).
        // In this case, the fragment will automatically be re-added
        // to its container so we don't need to manually add it.
        // For more information, see the Fragments API guide at:
        //
        // http://developer.android.com/guide/components/fragments.html
            super.onCreate(savedInstanceState);
            setContentView(R.layout.camera_activity);

            //Button gender_button = (Button)findViewById(R.id.genderButton);
            //nextGender = gender_button.getText().toString();

            mPhotCapuredImageView = (ImageView) findViewById(R.id.capturePhotoImageView);
            responseView = (TextView) findViewById(R.id.responseView);
            progressBar = (ProgressBar) findViewById(R.id.progressBar);

            responseView.setVisibility(View.INVISIBLE);
            progressBar.setVisibility(View.INVISIBLE);

    }

    public void takePhoto(View view){
//        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
//        Uri fileUri = getOutputMediaFileUri(MEDIA_TYPE_IMAGE);
//        intent.putExtra(android.provider.MediaStore.EXTRA_OUTPUT, fileUri);
//        //intent.setAction(MediaStore.ACTION_IMAGE_CAPTURE);
//        startActivityForResult(intent, ACTIVITY_START_CAMERA_APP);
        File photoFile = null;
        try {
            photoFile = createImageFile();
        }
        catch (IOException e) {
            Log.d("createImgFile", "takePhoto: e.toString()");
        }
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        Uri photoUri = FileProvider.getUriForFile(this, "com.smartfashion.fileprovider", photoFile);
        intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
        startActivityForResult(intent, ACTIVITY_START_CAMERA_APP);
    }

    public void pickImage(View view) {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        startActivityForResult(intent, PICK_IMAGE_REQUEST);
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        if(requestCode == ACTIVITY_START_CAMERA_APP && resultCode == RESULT_OK){
//            Bundle extras =data.getExtras();
//            photoCapturedBitmap = (Bitmap) extras.get("data");
//            mPhotCapuredImageView.setImageBitmap(photoCapturedBitmap);
//            img_flag = true;
            //Toast.makeText(this, "Picture Taken", Toast.LENGTH_SHORT).show();

            //super.onActivityResult(requestCode, resultCode, data);
            File file = new File(imageFilePath);
            try {
                photoCapturedBitmap = MediaStore.Images.Media.getBitmap(getBaseContext().getContentResolver(), Uri.fromFile(file));
                int height = photoCapturedBitmap.getHeight();
                int width = photoCapturedBitmap.getWidth();
                float aspectRatio = (float)width/(float)height;
                int newWidth = 500;
                int newHeight = (int) (newWidth/(aspectRatio));
                photoCapturedBitmap = Bitmap.createScaledBitmap(photoCapturedBitmap, newWidth, newHeight, false);
                mPhotCapuredImageView.setImageBitmap(photoCapturedBitmap);
                img_flag = true;
            }
            catch (Exception e) {
                Log.d("onActivityResult", "onActivityResult: " + e.toString());
            }
        }
        else if (requestCode == PICK_IMAGE_REQUEST) {
            Uri selectedImage = data.getData();
            try {
                photoCapturedBitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), selectedImage);
                int height = photoCapturedBitmap.getHeight();
                Log.d("height", "height: " + Integer.toString(height));
                int width = photoCapturedBitmap.getWidth();
                float aspectRatio = (float)width/(float)height;
                int newWidth = 500;
                int newHeight = (int) (newWidth/(aspectRatio));
                Log.d("aspect ratio", "aspect ratio: " + aspectRatio);
                Log.d("new height and width", "width, height: " + newWidth + "  " + newHeight);
                photoCapturedBitmap = Bitmap.createScaledBitmap(photoCapturedBitmap, newWidth, newHeight, false);
                mPhotCapuredImageView.setImageBitmap(photoCapturedBitmap);
                img_flag = true;
            }
            catch (Exception e) {
                Log.d("img gallery", "onActivityResult: could not pick image: " + e.toString());
            }
        }
    }

    /** Called when the user taps the Send button */
    public void sendImage(View view) {
        if (img_flag){
            img_flag = false;
            new StartQuery().execute();
            /*mPhotCapuredImageView.setVisibility(View.INVISIBLE);
            responseView.setVisibility(View.VISIBLE);
            progressBar.setVisibility(View.VISIBLE);*/
        }else{
            Toast.makeText(this, "Please take an image before sending", Toast.LENGTH_SHORT).show();
        }
    }

    /** Called when the user taps the Gender button */
//    public void cycleGender(View view) {
//        Button gender_button = (Button)findViewById(R.id.genderButton);
//        String currentGender = gender_button.getText().toString();
//        nextGender = getNextGender(currentGender);
//        gender_button.setText(nextGender);
//    }
//
//    private String getNextGender(String gender){
//        switch (gender){
//            case "Male"     : return "Female";
//            case "Female"   : return "Male";
//            default         : return "Female";
//        }
//    }


    class StartQuery extends AsyncTask<Void, Void, String> {
        private Exception exception;
        protected void onPreExecute() {
            bmp = photoCapturedBitmap;
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            bmp.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArrayImage = stream.toByteArray();
            encodedImage = Base64.encodeToString(byteArrayImage, Base64.DEFAULT);
            //Log.d("IMG Array", encodedImage);
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
                    //i try put here but idk la
                    Intent intent =  new Intent(getBaseContext(), LoadingActivity.class);
                    startActivity(intent);
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
                status = "accepted";
                responseView.setText("EXCEPTION DUN DUN DUN: " + response);
            }
        }
    }

    /** Create a file Uri for saving an image or video */
    private static Uri getOutputMediaFileUri(int type){
        Log.d("test", "getOutputMediaFileUri: " + (Uri.fromFile(getOutputMediaFile(type))).toString());
        return Uri.fromFile(getOutputMediaFile(type));
    }

    /** Create a File for saving an image or video */
    private static File getOutputMediaFile(int type){
        // To be safe, you should check that the SDCard is mounted
        // using Environment.getExternalStorageState() before doing this.

        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "MyCameraApp");
        // This location works best if you want the created images to be shared
        // between applications and persist after your app has been uninstalled.

        // Create the storage directory if it does not exist
        if (! mediaStorageDir.exists()){
            if (! mediaStorageDir.mkdirs()){
                Log.d("MyCameraApp", "failed to create directory");
                return null;
            }
        }

        // Create a media file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File mediaFile;
        if (type == MEDIA_TYPE_IMAGE){
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "IMG_"+ timeStamp + ".jpg");
        } else if(type == MEDIA_TYPE_VIDEO) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".mp4");
        } else {
            return null;
        }

        return mediaFile;
    }

    private File createImageFile() throws IOException {
        String timeStamp =
                new SimpleDateFormat("yyyyMMdd_HHmmss",
                        Locale.getDefault()).format(new Date());
        String imageFileName = "IMG_" + timeStamp + "_";
        File storageDir =
                getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        imageFilePath = image.getAbsolutePath();
        return image;
    }
}
