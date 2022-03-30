CREATE TABLE room (
    room_id INT PRIMARY KEY,
    room_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    room_desc VARCHAR ( 1024 ) 
);

CREATE TABLE item (
    item_id INT PRIMARY KEY,
    room_id INT REFERENCES room (room_id),
    item_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    item_desc VARCHAR ( 1024 )
);

CREATE TABLE objective (
    objective_id INT PRIMARY KEY,
    room_id INT REFERENCES room (room_id),
    objective_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    objective_desc VARCHAR ( 1024 ),
    difficulty INT,
    objective_url VARCHAR ( 256 ),
    supported_by INT REFERENCES objective (objective_id),
    requires INT REFERENCES item (item_id)
);

CREATE TABLE person (
    person_id INT PRIMARY KEY,
    room_id INT REFERENCES room (room_id),
    person_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    person_desc VARCHAR ( 1024 )
);

CREATE TABLE junction (
    destination INT REFERENCES room (room_id),
    room_id INT REFERENCES room (room_id),
    junction_desc VARCHAR ( 1024 )
);
