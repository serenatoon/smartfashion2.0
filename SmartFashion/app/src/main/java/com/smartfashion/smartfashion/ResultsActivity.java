package com.smartfashion.smartfashion;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import android.net.Uri;

import static com.smartfashion.smartfashion.CameraActivity.status;

public class ResultsActivity extends AppCompatActivity {
    private Context context;


    private final static int NUMBER_RESULTS_MAX = 50;
    private final static int NUMBER_RESULTS_LOAD = 10;
    private static int NUMBER_RESULTS_TO_LOAD = NUMBER_RESULTS_LOAD;
    private static int NUMBER_RESULTS_LOADED = 0;

    private HashMap results = new HashMap();
    private boolean getResultDone = true;
    private boolean limit_reached = false;

    private FloatingActionButton loadMoreButton;
    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    private static String LOG_TAG = "CardViewActivity";
    private RecyclerView.LayoutManager mLayoutManager;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.results_activity);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        NUMBER_RESULTS_TO_LOAD = NUMBER_RESULTS_LOAD;
        NUMBER_RESULTS_LOADED = 0;

//        loadMoreButton = (FloatingActionButton) findViewById(R.id.loadMoreButton);
//        loadMoreButton.setVisibility(View.INVISIBLE);
//        loadMoreButton.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                loadMore();
//            }
//        });

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
            goToMain("Back to Home");
            }
        });



//        resultName = (TextView) findViewById(R.id.resultName);
//        resultPrice = (TextView) findViewById(R.id.resultPrice);
//        resultImage = (ImageView) findViewById(R.id.resultImage);

        mRecyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);
        mRecyclerView.setHasFixedSize(true);
        mLayoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(mLayoutManager);



        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        //mRecyclerView.setHasFixedSize(true);

        // use a linear layout manager
//        mLayoutManager = new LinearLayoutManager(this);
//        mRecyclerView.setLayoutManager(mLayoutManager);

        //new GetResult().execute();

        mAdapter = new MyRecyclerViewAdapter(results, NUMBER_RESULTS_LOADED);
        mRecyclerView.setAdapter(mAdapter);


        new GetResult(NUMBER_RESULTS_LOADED).execute();
        NUMBER_RESULTS_LOADED++;


       /* int i = 0;
        while (i < NUMBER_RESULTS_LOAD){
            if (getResultDone){
                getResultDone = false;

                i++;
            }
        }*/
    }

    private void loadMore(){
        NUMBER_RESULTS_TO_LOAD = NUMBER_RESULTS_TO_LOAD + NUMBER_RESULTS_LOAD;
        getMoreResults();
        loadMoreButton.setVisibility(View.INVISIBLE);
    }

    private void getMoreResults(){
        if (getResultDone){
            if (NUMBER_RESULTS_LOADED < NUMBER_RESULTS_TO_LOAD){
                getResultDone = false;
                if (!limit_reached){
                    new GetResult(NUMBER_RESULTS_LOADED).execute();
                    NUMBER_RESULTS_LOADED++;
                }else{
                    Toast.makeText(this, "All Results Returned", Toast.LENGTH_SHORT).show();
                }
            }else{
                //loadMoreButton.setVisibility(View.VISIBLE);
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        ((MyRecyclerViewAdapter) mAdapter).setOnItemClickListener(new MyRecyclerViewAdapter.MyClickListener() {
            @Override
            public void onItemClick(int position, View v) {
                Log.i(LOG_TAG, " Clicked on Item " + position);
                //viewOnAmazon(v, position);
                //TODO: need to figure out how to get the url from object using the position
                String amazonUrl = "https://github.com/";
                Intent i = new Intent(Intent.ACTION_VIEW);
                i.setData(Uri.parse(amazonUrl));
                startActivity(i);
            }
        });
    }

    /** Called when the user taps the result panel */
    public void viewOnAmazon(View view, Integer position) {
         String amazonUrl = "https://github.com/";
         Intent i = new Intent(Intent.ACTION_VIEW);
         i.setData(Uri.parse(amazonUrl));
         startActivity(i);
     }


    private ArrayList<DataObject> getDataSet() {
        ArrayList results = new ArrayList<DataObject>();
        for (int index = 0; index < 20; index++) {
            DataObject obj = new DataObject("Some Primary Text " + index,
                    "Secondary " + index);
            results.add(index, obj);
        }
        return results;
    }

    public void goToMain(String errorMessage){
        Toast.makeText(this, errorMessage, Toast.LENGTH_SHORT).show();
        Intent intent =  new Intent(this, CameraActivity.class);
        startActivity(intent);
    }



    class GetResult extends AsyncTask<Void, Void, String> {
        private int resultNumber;

        GetResult(int resultNumber){
            this.resultNumber = resultNumber;
        }

        private Exception exception;

        protected void onPreExecute() {

        }

        public String doInBackground(Void... urls) {
            try {

                JSONObject json = new JSONObject();
                json.put("device_ID", CameraActivity.DEVICE_ID);
                json.put("password", CameraActivity.SERVER_PASSWORD);
                json.put("result_no", this.resultNumber);
                URL url = new URL(CameraActivity.API_URL + CameraActivity.GET_RESULT);
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

                }/*catch (Exception e){
                    limit_reached = true;
                }*/
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
            Log.d("RESULT POST EXECUTE", "onPostExecute: ");
            if(response == null) {
                response = "THERE WAS AN ERROR";
            }
            //progressBar.setVisibility(View.GONE);
            Log.i("INFO", response);
            try{
                JSONObject object = new JSONObject(response);
                Log.d("JSON", "onPostExecute: " + object.toString());

                //GET RESULT
                //String responseStatus = object.get("0").get("toString();

                String responsePrice = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("price").toString();
                //Log.d("price", "price: " + responsePrice);
                String responseUrl = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("url").toString();
                String responseImage = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("img").toString();
                String responseName = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("title").toString();
                //String responsePrice = object

                //CREATE RESULT OBJECT
                ResultObject resultObject = new ResultObject(responseName, responsePrice, responseUrl, responseImage);

                //ADD RESULT OBJECT TO THE HASH MAP
                results.put(NUMBER_RESULTS_LOADED, resultObject);

                //Updates
                mAdapter = new MyRecyclerViewAdapter(results, NUMBER_RESULTS_LOADED);
                mRecyclerView.setAdapter(mAdapter);

                //myDataset[0] = object.get("price").toString();


               /* resultPrice.setText(responsePrice);
                resultName.setText(responseName);
                resultImage.setImageBitmap(returnedBmp);*/
                //status = responseText;

                //responseView.setText(responseText);
            } catch (JSONException jsonLit){
                limit_reached = true;
                status = "error";
                // responseView.setText("EXCEPTION DUN DUN DUN: " + response);
            }

            getResultDone = true;
            getMoreResults();
        }
    }
}

