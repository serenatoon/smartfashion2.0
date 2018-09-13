package com.smartfashion.smartfashion;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.util.Base64;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import java.io.IOException;
import java.net.URL;

/**
 * Created by mini- on 30/07/2017.
 */

public class ResultObject {
    private String name;
    private String price;
    private String url;
    private String image;

    /***protected void onCreate(Bundle savedInstanceState) {
        // savedInstanceState is non-null when there is fragment state
        // saved from previous configurations of this activity
        // (e.g. when rotating the screen from portrait to landscape).
        // In this case, the fragment will automatically be re-added
        // to its container so we don't need to manually add it.
        // For more information, see the Fragments API guide at:
        //
        // http://developer.android.com/guide/components/fragments.html
        onCreate(savedInstanceState);
        setContentView(R.layout.cardviews);

        //Button gender_button = (Button)findViewById(R.id.genderButton);
        //nextGender = gender_button.getText().toString();

        mPhotCapuredImageView = (ImageView) findViewById(R.id.capturePhotoImageView);
        responseView = (TextView) findViewById(R.id.responseView);
        progressBar = (ProgressBar) findViewById(R.id.progressBar);

    }***/


    ResultObject (String name, String price, String url, String image){
        this.name = name;
        this.price = price;
        this.url = url;
        this.image = image;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getImage() {
        return image;
    }

    public Bitmap getImageBmp(){
        byte[] decodedString = Base64.decode(this.image, Base64.DEFAULT);
        //Log.e("getImageBmp: ", decodedString.toString() );
        Bitmap imageBmp = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        return imageBmp;
//
//        Bitmap bmp;
//        try {
//            URL url = new URL(image);
//            bmp = BitmapFactory.decodeStream(url.openConnection().getInputStream());
//            return bmp;
//        } catch(IOException e) {
//            System.out.println(e);
//        }
//
//        Bitmap.Config conf = Bitmap.Config.ARGB_8888;
//        return Bitmap.createBitmap(1, 1, conf); // return some random ass bitmap just so function compiles
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
//
//    public void viewOnAmazon(View view) {
//        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(this.getUrl()));
//        view.getContext().startActivity(intent);
//    }


}
