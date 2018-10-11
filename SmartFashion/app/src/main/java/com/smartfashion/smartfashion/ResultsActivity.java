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
import java.util.HashMap;
import android.net.Uri;

import static com.smartfashion.smartfashion.CameraActivity.status;

public class ResultsActivity extends AppCompatActivity {
    private Context context;


    private final static int NUMBER_RESULTS_LOAD = 20;
    private static int NUMBER_RESULTS_TO_LOAD = NUMBER_RESULTS_LOAD;
    private static int NUMBER_RESULTS_LOADED = 0;

    private HashMap results = new HashMap();
    private boolean getResultDone = true;
    private boolean limit_reached = false;

    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    private static String LOG_TAG = "CardViewActivity";
    private RecyclerView.LayoutManager mLayoutManager;

    public String[] url = new String[10];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.results_activity);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        NUMBER_RESULTS_TO_LOAD = NUMBER_RESULTS_LOAD;
        NUMBER_RESULTS_LOADED = 0;

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                goToMain("Back to Home");
            }
        });


        mRecyclerView = (RecyclerView) findViewById(R.id.my_recycler_view);
        mRecyclerView.setHasFixedSize(true);
        mLayoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(mLayoutManager);

        mAdapter = new MyRecyclerViewAdapter(results, NUMBER_RESULTS_LOADED);
        mRecyclerView.setAdapter(mAdapter);

        new GetResult(NUMBER_RESULTS_LOADED).execute();
        NUMBER_RESULTS_LOADED++;

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
//                String amazonUrl = "https://github.com/";
                Intent i = new Intent(Intent.ACTION_VIEW);
                Log.d("click", "url: " + url[position]);
                i.setData(Uri.parse(url[position+1]));
                startActivity(i);
            }
        });
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
                url[NUMBER_RESULTS_LOADED] = responseUrl;
                Log.d("url", "onPostExecute url: " + url[NUMBER_RESULTS_LOADED]);
                String responseImage = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("img").toString();
                String responseName = object.getJSONObject(Integer.toString(NUMBER_RESULTS_LOADED)).get("title").toString();

                //CREATE RESULT OBJECT
                ResultObject resultObject = new ResultObject(responseName, responsePrice, responseUrl, responseImage);

                //ADD RESULT OBJECT TO THE HASH MAP
                results.put(NUMBER_RESULTS_LOADED, resultObject);

                //Updates
                mAdapter = new MyRecyclerViewAdapter(results, NUMBER_RESULTS_LOADED);
                mRecyclerView.setAdapter(mAdapter);

            } catch (JSONException jsonLit){
                limit_reached = true;
                status = "error";
                //goToMain("An exception has occurred");
            }
            getResultDone = true;
            getMoreResults();
        }
    }
}

