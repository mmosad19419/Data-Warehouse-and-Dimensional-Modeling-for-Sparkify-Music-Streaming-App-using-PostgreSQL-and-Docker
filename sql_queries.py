# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songsplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

user_table_create = (""" CREATE TABLE IF NOT EXISTS users
                            (user_id INT PRIMARY KEY UNIQUE NOT NULL,
                            first_name VARCHAR,
                            last_name VARCHAR,
                            gender CHAR, level VARCHAR);
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs
                    (song_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
                    title VARCHAR NOT NULL, artist_id VARCHAR NOT NULL,
                    artist_name VARCHAR NOT NULL,
                    year INT NOT NULL,
                    duration FLOAT8 NOT NULL);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists
                      (artist_id VARCHAR PRIMARY KEY UNIQUE NOT NULL,
                      name VARCHAR NOT NULL,
                      location VARCHAR,
                      latitude FLOAT8,
                      longitude FLOAT8);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time
                    (session_id VARCHAR NOT NULL,
                    start_time TIME NOT NULL,
                    hour VARCHAR, day VARCHAR,
                    week VARCHAR, month VARCHAR,
                    year VARCHAR,
                    weekday VARCHAR,
                    PRIMARY KEY (start_time, session_id));
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays
                        (songplay_id SERIAL PRIMARY KEY NOT NULL,
                        start_time TIME NOT NULL,
                        session_id VARCHAR UNIQUE NOT NULL,
                        user_id INT UNIQUE NOT NULL,
                        song_id VARCHAR UNIQUE,
                        artist_id VARCHAR UNIQUE,
                        level VARCHAR,
                        location VARCHAR,
                        user_agent VARCHAR);
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays
                            (start_time, session_id, user_id, song_id, artist_id, level, location, user_agent)
                        VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (user_id)
                        DO UPDATE level = %s;
""")


# user table insertion
user_table_insert = ("""INSERT INTO users
                        (user_id, first_name, last_name, gender, level)
                    VALUES
                        (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id)
                    DO UPDATE level = %s;
""")


# song table insertion
song_table_insert = ("""INSERT INTO songs
                        (song_id, title, artist_id, artist_name, year, duration)
                    VALUES
                        (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (song_id)
                    DO UPDATE duration = %s;
""")


# song table insertion
artist_table_insert = ("""INSERT INTO artists
                          (artist_id, name, location, latitude, longitude)
                    VALUES
                          (%s, %s, %s, %s, %s)
                    ON CONFLICT (artist_id)
                    DO UPDATE name = %s;
""")


# time table insert
time_table_insert = ("""INSERT INTO time
                        (session_id, start_time, hour, day, week, month, year, weekday)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (artist_id)
                    DO UPDATE start_time = %s;
""")

# FIND SONGS

song_select = ("""SELECT song_id, artist_id FROM songs
                  WHERE title LIKE %s
                  AND artist_name LIKE %s
                  AND duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
