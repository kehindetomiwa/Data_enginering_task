
CREATE TABLE IF NOT EXISTS app(
            pk INT NOT NULL PRIMARY KEY,
            id VARCHAR(256) UNIQUE,
            title VARCHAR(256),
            decription VARCHAR(2000),
            published_timestamp TIMESTAMP,
            last_update TIMESTAMP
); 