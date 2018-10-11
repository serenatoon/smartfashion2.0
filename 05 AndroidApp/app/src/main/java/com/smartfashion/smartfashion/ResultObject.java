package com.smartfashion.smartfashion;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;

public class ResultObject {
    private String name;
    private String price;
    private String url;
    private String image;

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

    public String getImage() {
        return image;
    }

    public Bitmap getImageBmp(){
        byte[] decodedString = Base64.decode(this.image, Base64.DEFAULT);
        Bitmap imageBmp = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
        return imageBmp;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getUrl() {
        return url;
    }
}
