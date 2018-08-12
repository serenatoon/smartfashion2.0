package com.smartfashion.smartfashion;

import android.content.Context;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.support.v7.widget.RecyclerView;
import android.graphics.Bitmap;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.StringTokenizer;

/**
 * Created by mini- on 30/07/2017.
 */

public class MyRecyclerViewAdapter extends RecyclerView.Adapter<MyRecyclerViewAdapter.DataObjectHolder> {

    private static String LOG_TAG = "MyRecyclerViewAdapter";
    private HashMap mResults;
    private Integer mResultsNumber;
    private Context mContext;
    private ArrayList<DataObject> mDataset;
    private static MyClickListener myClickListener;

    MyRecyclerViewAdapter(DataObjectHolder holder, int position){

    }

    public static class DataObjectHolder extends RecyclerView.ViewHolder
            implements View
            .OnClickListener {
        TextView nameLabel;
        TextView priceLabel;
        ImageView resultImage;
        String url;
        private Context context;

        public DataObjectHolder(View itemView) {
            super(itemView);
            nameLabel = (TextView) itemView.findViewById(R.id.textView);
            priceLabel = (TextView) itemView.findViewById(R.id.textView2);
            resultImage = (ImageView) itemView.findViewById(R.id.imageView);

            Log.i(LOG_TAG, "Adding Listener");
            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            myClickListener.onItemClick(getAdapterPosition(), v);
            Intent i = new Intent(Intent.ACTION_VIEW);
            i.setData(Uri.parse(url));
            //startActivity(i);
        }
    }




    public void setOnItemClickListener(MyClickListener myClickListener) {
        this.myClickListener = myClickListener;
    }

    public MyRecyclerViewAdapter(HashMap results, int numberResults) {
        mResults = results;
        mResultsNumber = numberResults;

    }

    @Override
    public DataObjectHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.card_view_row, parent, false);

        DataObjectHolder dataObjectHolder = new DataObjectHolder(view);
        return dataObjectHolder;
    }

    @Override
    public void onBindViewHolder(DataObjectHolder holder, int position) {
        Log.e("POSITION", Integer.toString(position));
        position = position+1;
        Log.e("POSITION", Integer.toString(position));
        ResultObject resultObject = (ResultObject) mResults.get(position);
        Log.e("RESULT OBJECT", resultObject.toString());
        holder.nameLabel.setText(resultObject.getName());
        holder.priceLabel.setText("$"+resultObject.getPrice());
        holder.resultImage.setImageBitmap(resultObject.getImageBmp());
        holder.url = resultObject.getUrl();
    }


    public void addItem(DataObject dataObj, int index) {
        mDataset.add(index, dataObj);
        notifyItemInserted(index);
    }

    public void deleteItem(int index) {
        mResults.remove(index);
        notifyItemRemoved(index);
    }

    @Override
    public int getItemCount() {
        Log.e("RESULT", Integer.toString(mResults.size()));
        if (mResults.size() == 1){
            Log.e("RESULTS KEYS", mResults.keySet().toString());
            Log.e("RESULT OBJECT HERE", mResults.get(1).toString());
        }
        return mResults.size();
    }

    public interface MyClickListener {
        public void onItemClick(int position, View v);

    }
}
