CREATE TABLE room (
    room_id INT PRIMARY KEY,
    room_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    room_desc VARCHAR ( 1024 ) 
);

CREATE TABLE item (
    item_id INT PRIMARY KEY,
    room_name VARCHAR ( 100 ),
    item_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    item_desc VARCHAR ( 1024 )
);

CREATE TABLE objective (
    objective_id INT PRIMARY KEY,
    room_name VARCHAR ( 100 ),
    objective_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    objective_desc VARCHAR ( 1024 ),
    difficulty INT,
    objective_url VARCHAR ( 256 ),
    supported_by VARCHAR ( 100 ),
    requires VARCHAR ( 100 )
);

CREATE TABLE person (
    person_id INT PRIMARY KEY,
    room_name VARCHAR ( 100 ),
    person_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    person_desc VARCHAR ( 1024 )
);

CREATE TABLE junction (
    destination VARCHAR ( 100 ),
    room_name VARCHAR ( 100 ),
    junction_desc VARCHAR ( 1024 )
);
