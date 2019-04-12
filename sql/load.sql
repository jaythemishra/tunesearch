\copy artist FROM '/home/cs143/data/artist.csv' WITH DELIMITER ',' QUOTE '"' CSV;
\copy song FROM '/home/cs143/data/song.csv' WITH DELIMITER ',' QUOTE '"' CSV;
\copy token (song_id, token, frequency) FROM '/home/cs143/data/token.csv' WITH DELIMITER ',' QUOTE '"' CSV;