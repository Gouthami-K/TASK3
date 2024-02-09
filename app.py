from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    # Load your data and perform the analysis
    df = pd.read_excel('rawdata.xlsx')

    df.head()

    ## 1. Datewise total duration for each inside and outside:

    # Convert the 'date' and 'time' columns to a datetime format and combine them into a new 'datetime' column
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
    df['datetime']

    # Sort the DataFrame by 'date', 'location', and 'datetime' to ensure chronological order
    df = df.sort_values(by=['date', 'location', 'datetime'])
    df.head()

    # Calculate the duration for each activity based on the difference between consecutive timestamps
    df['duration'] = df.groupby(['date', 'location'])['datetime'].diff().dt.total_seconds().fillna(0)
    df['duration']

    # Group by 'date' and 'location', then sum the durations to get the total duration for each inside and outside on each date
    datewise_duration = df.groupby(['date', 'location'])['duration'].sum().reset_index()
    datewise_duration

    # 2. Datewise number of picking and placing activity done:

    # Group by 'date' and 'activity', then count the number of occurrences of each activity for each date
    datewise_activity_count = df.groupby(['date', 'activity'])['number'].count().reset_index()

    # Display the datewise counts of picking and placing activities
    print(datewise_activity_count)

    # Pass the results to the template
    return render_template('index.html', datewise_duration=datewise_duration, datewise_activity_count=datewise_activity_count)

if __name__ == '__main__':
    app.run(debug=True)
