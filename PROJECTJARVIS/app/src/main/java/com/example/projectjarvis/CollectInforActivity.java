package com.example.projectjarvis;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;

public class CollectInforActivity extends AppCompatActivity {

    public static final String Age = "value1";
    public static final String Gender = "value2";
    public static final String Native = "value3";

    private String Gender_temp = "None";
    private String Native_temp = "None";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_collect_infor);
    }

    public void StartRecordingActivity(View view){
        Intent intent = new Intent(this, RecordingActivity.class);
        EditText editText = (EditText) findViewById(R.id.editText);
        String message =  editText.getText().toString();
        intent.putExtra(Age, message);
        intent.putExtra(Gender, Gender_temp);
        intent.putExtra(Native, Native_temp);
        startActivity(intent);
    }

    public void onRadioButtonClicked(View view) {
        // Is the button now checked?
        boolean checked = ((RadioButton) view).isChecked();

        // Check which radio button was clicked
        switch(view.getId()) {
            case R.id.radioButton7: // Male
                if (checked)
                    Gender_temp = "Male";
                    break;
            case R.id.radioButton6: // Female
                if (checked)
                    Gender_temp = "Female";
                    break;

            case R.id.radioButton8: // Yes
                if (checked)
                    Native_temp = "Yes";
                    break;
            case R.id.radioButton9: // No
                if (checked)
                    Native_temp = "No";
                    break;
        }
    }

}
