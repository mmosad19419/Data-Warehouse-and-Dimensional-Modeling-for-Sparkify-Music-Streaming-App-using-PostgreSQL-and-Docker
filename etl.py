import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    
    return all_files


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_id = df.iloc[0]["song_id"]
    title = df.iloc[0]["title"]
    artist_id = df.iloc[0]["artist_id"]
    artist_name = df.iloc[0]["artist_name"]
    year = int(df.iloc[0]["year"])
    duration = float(df.iloc[0]["duration"])
    
    song_data = list((song_id, title, artist_id, artist_name, year, duration))

    cur.execute(song_table_insert, song_data)

        
    # insert artist record
    artist_id = df.iloc[0]["artist_id"]
    artist_name = df.iloc[0]["artist_name"]
    artist_location = df.iloc[0]["artist_location"]
    artist_latitude = df.iloc[0]["artist_latitude"]
    artist_longitude = df.iloc[0]["artist_longitude"]
    
    artist_data = list((artist_id, artist_name, artist_location, artist_latitude, artist_longitude))
    
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = df.iloc[0]['ts']
    
    # insert time data records
    time_data = pd.Series(pd.to_datetime(t, unit = "ms"), dtype = "datetime64[ns]")
    
    df_dict = {"session_id" : df.iloc[0]["sessionId"],
               "start_time" : time_data.dt.time,
               "hour" : time_data.dt.hour,
               "day" : time_data.dt.day,
               "week" : time_data.dt.week,
               "month" : time_data.dt.week, 
               "year" : time_data.dt.year, 
               "weekday" : time_data.dt.weekday}
    
    time_df = pd.DataFrame(df_dict)
    
    for i, row in time_df.iterrows():
        
        cur.execute(time_table_insert, list(row))
    

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
    
        start_time = time_data.dt.time[0]
        
        # insert songplay record
        songplay_data = tuple([start_time, row.sessionId, row.userId, songid, artistid, row.level, row.location, row.userAgent])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.rollback()
    conn.autocommit=True
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()