\copy artist FROM '/home/cs143/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
\copy song   FROM '/home/cs143/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
\copy token  FROM '/home/cs143/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;
INSERT INTO tfidf SELECT
  tf_data.song_id,
  tf_data.token,
  LOG((SELECT COUNT(*) FROM song) / df_data.df) * tf_data.count AS score
FROM token tf_data
LEFT JOIN (
  SELECT
    token,
    COUNT(song_id) AS df
  FROM token
  GROUP BY token
) df_data
ON df_data.token = tf_data.token;