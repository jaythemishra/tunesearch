\copy artist FROM '/home/cs143/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
\copy song   FROM '/home/cs143/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
\copy token  FROM '/home/cs143/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;
\copy tfidf  FROM '/home/cs143/data/tfidf.csv'  DELIMITER ',' QUOTE '"' CSV;
