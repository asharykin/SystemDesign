DROP TABLE IF EXISTS deliveries CASCADE;

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL ,
    email TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE deliveries (
    id SERIAL PRIMARY KEY,
    sender_id INT NOT NULL REFERENCES users (id),
    receiver_id INT NOT NULL REFERENCES users (id)
);

-- Для users.username индекс будет создан автоматически, так как это поле уникальное

CREATE INDEX ON users (first_name);

CREATE INDEX ON users (last_name);

CREATE INDEX ON deliveries (sender_id);

CREATE INDEX ON deliveries (receiver_id);

INSERT INTO users (username, password, first_name, last_name, email, address) -- password: secret
VALUES ('admin', '$2a$12$sA1yYUegaqJ8psTJFOBQbOcH5DW4RBZeJZuxqZiBkIvVZ4ZlrHAX2', 'Admin', 'Adminov', 'admin@gmail.com', '10 Arbat Street Moscow');

INSERT INTO users (username, password, first_name, last_name, email, address) -- password: ivan1234
VALUES ('iivanov', '$2a$12$sA1yYUegaqJ8psTJFOBQbOcH5DW4RBZeJZuxqZiBkIvVZ4ZlrHAX2', 'Ivan', 'Ivanov', 'iivanov@gmail.com', '6 Tverskaya Street Moscow');

INSERT INTO deliveries (sender_id, receiver_id)
VALUES (1, 2);

INSERT INTO deliveries (sender_id, receiver_id)
VALUES (2, 1);