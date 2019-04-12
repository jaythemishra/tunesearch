DROP TABLE IF EXISTS tf_idf;
DROP TABLE IF EXISTS token;
DROP TABLE IF EXISTS song;
DROP TABLE IF EXISTS artist;


CREATE TABLE artist (
    id          smallint NOT NULL,
    artist_name varchar(50),
    PRIMARY KEY (id)
);

CREATE TABLE song (
    id          integer NOT NULL,
    artist_id   smallint,
    song_name   varchar(100),
    song_url    varchar(150),
    PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artist(id)
);

CREATE TABLE token (
    id          bigserial,
    song_id     integer,
    token       varchar(110),
    frequency   smallint,
    PRIMARY KEY (id),
    FOREIGN KEY (song_id) REFERENCES song(id)
);

CREATE TABLE tf_idf (
    id          bigint NOT NULL,
    score       decimal,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES token(id)
);