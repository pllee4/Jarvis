package com.example.projectjarvis;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.IOException;

public class RecordingActivity extends AppCompatActivity {

    private static final String LOG_TAG = "AudioRecordTest";
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;

    public static final String Age = "value4";
    public static final String Gender = "value5";
    public static final String Native = "value6";

    public String Age_temp = "None";
    public String Gender_temp = "None";
    public String Native_temp = "None";


    public static String [] fileName = { "", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","", "","","","" };
    public static String [] fileName2 = { "/audiorecord1.3gp", "/audiorecord2.3gp","/audiorecord3.3gp", "/audiorecord4.3gp","/audiorecord5.3gp", "/audiorecord6.3gp",
            "/audiorecord7.3gp", "/audiorecord8.3gp","/audiorecord9.3gp", "/audiorecord10.3gp" , "/audiorecord11.3gp", "/audiorecord12.3gp","/audiorecord13.3gp",
            "/audiorecord14.3gp","/audiorecord15.3gp", "/audiorecord16.3gp", "/audiorecord17.3gp", "/audiorecord18.3gp","/audiorecord19.3gp", "/audiorecord20.3gp" ,
            "/audiorecord21.3gp", "/audiorecord22.3gp","/audiorecord23.3gp", "/audiorecord24.3gp","/audiorecord25.3gp", "/audiorecord26.3gp",
            "/audiorecord27.3gp", "/audiorecord28.3gp","/audiorecord29.3gp", "/audiorecord30.3gp","/audiorecord31.3gp", "/audiorecord32.3gp","/audiorecord33.3gp" };

    private int currentfile = 0;

    public Button recordButton = null;
    private MediaRecorder recorder = null;
    boolean mStartRecording = true;

    public Button playButton = null;
    private MediaPlayer player = null;
    boolean mStartPlaying = true;

    public Button next_done_Button = null;
    private TextView textview = null;
    private ImageView image = null;

    // Requesting permission to RECORD_AUDIO
    private boolean permissionToRecordAccepted = false;
    private String [] permissions = {Manifest.permission.RECORD_AUDIO};

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode){
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted  = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
        }
        if (!permissionToRecordAccepted ) finish();

    }

    private void onRecord(boolean start) {
        if (start)
            startRecording();
        else
            stopRecording();
    }

    private void startRecording() {
        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setOutputFile(fileName[currentfile]);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            recorder.prepare();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }

        recorder.start();
    }

    private void stopRecording() {
        recorder.stop();
        recorder.release();
        recorder = null;
    }

    private void onPlay(boolean start) {
        if (start)
            startPlaying();
        else
            stopPlaying();
    }

    private void startPlaying() {
        player = new MediaPlayer();
        try {
            player.setDataSource(fileName[currentfile]);
            player.prepare();
            player.start();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }
    }

    private void stopPlaying() {
        player.release();
        player = null;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recording);

        Intent intent = getIntent();
        Age_temp = intent.getStringExtra(CollectInforActivity.Age);
        Gender_temp = intent.getStringExtra(CollectInforActivity.Gender);
        Native_temp = intent.getStringExtra(CollectInforActivity.Native);

        // Record to the external cache directory for visibility
        //fileName = getExternalCacheDir().getAbsolutePath();
        //fileName += "/audiorecordtest.3gp";
        for(int i = 0; i < 33; i++)
            fileName[i] = getExternalCacheDir().getAbsolutePath() +  fileName2[i];

        ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);
        recordButton = findViewById(R.id.Record);
        recordButton.setText("Start recording");
        recordButton.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                onRecord(mStartRecording);
                if (mStartRecording)
                    recordButton.setText("Stop recording");
                else
                    recordButton.setText("Start recording");
                mStartRecording = !mStartRecording;
            }
        });

        playButton = findViewById(R.id.Play);
        playButton.setText("Start playing");
        playButton.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View view)
            {
                onPlay(mStartPlaying);
                if (mStartPlaying)
                    playButton.setText("Stop playing");
                else
                    playButton.setText("Start playing");
                mStartPlaying = !mStartPlaying;
            }
        });

        next_done_Button = findViewById(R.id.next_done);
        textview = findViewById(R.id.next_done_textview);
        image = findViewById(R.id.imageview);
        next_done_Button.setText("Next");
        image.setImageResource(R.drawable.pic1);
        textview.setText("Press Next to continue");
        next_done_Button.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                if(!mStartPlaying){
                    stopPlaying();
                    playButton.setText("Start playing");
                    mStartPlaying = !mStartPlaying;
                }

                if (!mStartRecording){
                    stopRecording();
                    recordButton.setText("Start recording");
                    mStartRecording = !mStartRecording;
                }
                currentfile++;
                switch (currentfile){
                    case 1: image.setImageResource(R.drawable.pic2);
                        break;
                    case 2: image.setImageResource(R.drawable.pic3);
                        break;
                    case 3: image.setImageResource(R.drawable.pic4);
                        break;
                    case 4: image.setImageResource(R.drawable.pic5);
                        break;
                    case 5: image.setImageResource(R.drawable.pic6);
                        break;
                    case 6: image.setImageResource(R.drawable.pic7);
                        break;
                    case 7: image.setImageResource(R.drawable.pic88);
                        break;
                    case 8: image.setImageResource(R.drawable.pic9);
                        break;
                    case 9: image.setImageResource(R.drawable.pic10);
                        break;
                    case 10: image.setImageResource(R.drawable.pic11);
                        break;
                    case 11: image.setImageResource(R.drawable.pic12);
                        break;
                    case 12: image.setImageResource(R.drawable.pic13);
                        break;
                    case 13: image.setImageResource(R.drawable.pic14);
                        break;
                    case 14: image.setImageResource(R.drawable.pic15);
                        break;
                    case 15: image.setImageResource(R.drawable.pic16);
                        break;
                    case 16: image.setImageResource(R.drawable.pic17);
                        break;
                    case 17: image.setImageResource(R.drawable.pic18);
                        break;
                    case 18: image.setImageResource(R.drawable.pic19);
                        break;
                    case 19: image.setImageResource(R.drawable.pic20);
                        break;
                    case 20: image.setImageResource(R.drawable.pic21);
                        break;
                    case 21: image.setImageResource(R.drawable.pic22);
                        break;
                    case 22: image.setImageResource(R.drawable.pic23);
                        break;
                    case 23: image.setImageResource(R.drawable.pic24);
                        break;
                    case 24: image.setImageResource(R.drawable.pic25);
                        break;
                    case 25: image.setImageResource(R.drawable.pic26);
                        break;
                    case 26: image.setImageResource(R.drawable.pic27);
                        break;
                    case 27: image.setImageResource(R.drawable.pic28);
                        break;
                    case 28: image.setImageResource(R.drawable.pic29);
                        break;
                    case 29: image.setImageResource(R.drawable.pic30);
                        break;
                    case 30: image.setImageResource(R.drawable.pic31);
                        break;
                    case 31: image.setImageResource(R.drawable.pic32);
                        break;
                    case 32: image.setImageResource(R.drawable.pic33);
                        break;
                }

                if (currentfile == 32){
                    next_done_Button.setText("Done");
                    textview.setText("Press Done to continue");
                } else if (currentfile == 33){
                    toFinal(view);
                }

            }
        } );
    }

    public void toFinal(View view) {
        Intent intent = new Intent(this, FinalActivity.class);
        intent.putExtra(Age, Age_temp);
        intent.putExtra(Gender, Gender_temp);
        intent.putExtra(Native, Native_temp);
        startActivity(intent);
    }

}
