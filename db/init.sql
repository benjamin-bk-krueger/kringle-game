CREATE TABLE creator (
    creator_id SERIAL PRIMARY KEY,
    creator_name VARCHAR ( 100 ) UNIQUE NOT NULL
);

CREATE TABLE world (
    world_id SERIAL PRIMARY KEY,
    creator_id INT REFERENCES creator ( creator_id ),
    world_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    world_desc VARCHAR ( 1024 ),
    world_url VARCHAR ( 256 )
);

CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    world_id INT REFERENCES world ( world_id ),
    room_name VARCHAR ( 100 ),
    room_desc VARCHAR ( 1024 ) 
);

CREATE UNIQUE INDEX idx_room_name
ON room ( room_id, world_id );

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES room ( room_id ),
    world_id INT REFERENCES world ( world_id ),
    item_name VARCHAR ( 100 ),
    item_desc VARCHAR ( 1024 )
);

CREATE UNIQUE INDEX idx_item_name
ON item ( item_id, world_id );

CREATE TABLE objective (
    objective_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES room ( room_id ),
    world_id INT REFERENCES world ( world_id ),
    objective_name VARCHAR ( 100 ),
    objective_desc VARCHAR ( 1024 ),
    difficulty INT,
    objective_url VARCHAR ( 256 ),
    supported_by VARCHAR ( 100 ),
    requires VARCHAR ( 100 )
);

CREATE UNIQUE INDEX idx_objective_name
ON objective ( objective_id, world_id );

CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES room ( room_id ),
    world_id INT REFERENCES world ( world_id),
    person_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    person_desc VARCHAR ( 1024 )
);

CREATE UNIQUE INDEX idx_person_name
ON person ( person_id, room_id );

CREATE TABLE junction (
    junction_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES room ( room_id ),
    world_id INT REFERENCES world ( world_id ),
    dest_id INT REFERENCES room ( room_id ),
    junction_desc VARCHAR ( 1024 )
);

CREATE UNIQUE INDEX idx_junction_dest
ON junction ( room_id, dest_id, world_id );

CREATE TABLE quest (
    quest_id SERIAL PRIMARY KEY,
    objective_id INT REFERENCES objective ( objective_id ),
    creator_id INT REFERENCES creator ( creator_id ),
    quest_text TEXT
);

CREATE UNIQUE INDEX idx_quest_creator
ON quest ( objective_id, creator_id );

CREATE TABLE solution (
    solution_id SERIAL PRIMARY KEY,
    objective_id INT REFERENCES objective ( objective_id ),
    creator_id INT REFERENCES creator ( creator_id ),
    solution_text TEXT
);

CREATE UNIQUE INDEX idx_solution_creator
ON solution ( objective_id, creator_id );
