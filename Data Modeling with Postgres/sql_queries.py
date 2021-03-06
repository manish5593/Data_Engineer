# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"     
user_table_drop = "DROP TABLE IF EXISTS users;" 
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"



# CREATE TABLES
# each table requires a primary key. when it does not have such a column, create a automatically increment one like (songplay_id # serial primary key and id serial primary key )
# A primary key is required to be NOT NUL
# foreign keys must reference a unique key in the parent table: pay attention to who references whom
# which means, a foreign key must reference columns that either are a primary key or form a unique constrain

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays (songplay_id serial, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar, song_id varchar , artist_id varchar, session_id int, location varchar, user_agent varchar,  
primary key(songplay_id), 
foreign key (user_id) references users(user_id),
foreign key(song_id) references songs(song_id),
foreign key(artist_id) references artists(artist_id),
foreign key(start_time) references time(start_time))""" )

user_table_create = (""" CREATE TABLE IF NOT EXISTS users (user_id int primary key, first_name varchar, last_name varchar, gender varchar, level varchar) """)

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (song_id varchar primary key, title varchar, artist_id varchar, year int, duration float) """)

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists (artist_id varchar primary key, artist_name varchar, artist_location varchar, artist_lattitude float, artist_longitude float ) """)

# start_time time without time zone 
time_table_create = (""" CREATE TABLE IF NOT EXISTS time ( start_time timestamp primary key, hour int NOT NULL, day int NOT NULL, week int NOT NULL, month int NOT NULL, year int NOT NULL, weekday int NOT NULL ) """)



# INSERT RECORDS
# primary key (user_id,song_id,artist_id), so they are unique. But in reality, there will be some conflicts. So you need handle conflicts

# pay attention to three tables which requires to handle confliction because we set them as primary key (user_id,song_id,artist_id), user table has a special part, coz the level(status) can be changed from free to paid 

# songplay_id will increase automatically, it should not be treated as a separate column 
songplay_table_insert = (""" INSERT INTO songplays ( start_time, user_id, level, song_id, artist_id, session_id, location , user_agent) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s) """)   

user_table_insert = (""" INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET level= EXCLUDED.level """)

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING """)

artist_table_insert = (""" INSERT INTO artists (artist_id, artist_name, artist_location, artist_lattitude, artist_longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING """)

time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING """)


# FIND SONGS
# this is required in etl.ipynb 
# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, 
# and duration of a song.
#should be left join , some songs may not have artist in record
song_select = (""" SELECT s.song_id, a.artist_id
                   FROM songs s 
                   LEFT JOIN artists a     
                   ON s.artist_id = a.artist_id
                   WHERE title = (%s) AND artist_name = (%s) AND duration = (%s) """)    
# this where statement is based on what is required in etl.ipynb


# QUERY LISTS
# the order is important, you should execute the dimension tables first, then fact table. Because there are fks in fact table pointing to dimension tables. So dimension tables must exist first
# dimension tables in the front 
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
