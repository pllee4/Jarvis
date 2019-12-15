package com.example.projectjarvis;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.TextView;

import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageMetadata;
import com.google.firebase.storage.StorageReference;

import java.io.File;

public class FinalActivity extends AppCompatActivity {

    private StorageReference mStorageRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_final);

        mStorageRef = FirebaseStorage.getInstance().getReference();
        Intent intent = getIntent();

        TextView textView = findViewById(R.id.textView9);
        textView.setText("Please Wait........");

        for(int j = 0; j < 33; j++ ){
            Uri file = Uri.fromFile(new File(RecordingActivity.fileName[j]));
            StorageReference riversRef = mStorageRef.child("/voices/" + RecordingActivity.fileName2[j]);
            StorageMetadata metadata = new StorageMetadata.Builder()
                    .setCustomMetadata("Word", Integer.toString((j + 1)) )
                    .setCustomMetadata("Age", intent.getStringExtra(RecordingActivity.Age))
                    .setCustomMetadata("Gender", intent.getStringExtra(RecordingActivity.Gender))
                    .setCustomMetadata("Native", intent.getStringExtra(RecordingActivity.Native))
                    .build();
            riversRef.updateMetadata(metadata);
            riversRef.putFile(file,metadata);
        }

        textView.setText("Thank You For Your Cooperation!");

    }


}
