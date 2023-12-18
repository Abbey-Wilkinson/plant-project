DROP TABLE IF EXISTS plant_condition;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS origin;

CREATE TABLE origin (
    origin_id INT GENERATED ALWAYS AS IDENTITY,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    town VARCHAR(50) NOT NULL,
    country VARCHAR(25) NOT NULL,
    continent VARCHAR(25) NOT NULL,
    PRIMARY KEY (origin_id)
);

CREATE TABLE botanist (
    botanist_id INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(25) NOT NULL,
    surname VARCHAR(25) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    phone_number INT UNIQUE NOT NULL,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE plant (
    plant_id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) UNIQUE NOT NULL,
    scientific_name VARCHAR(50) UNIQUE NOT NULL,
    botanist_id INT NOT NULL,
    origin_id INT NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id)
        REFERENCES botanist(botanist_id),
    FOREIGN KEY (origin_id)
        REFERENCES origin(origin_id)
);

CREATE TABLE plant_condition (
    plant_condition_id INT GENERATED ALWAYS AS IDENTITY,
    at TIMESTAMPTZ NOT NULL,
    soil_moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    last_watered TIMESTAMPTZ NOT NULL,
    plant_id INT NOT NULL,
    PRIMARY KEY (plant_condition_id),
    FOREIGN KEY (plant_id)
        REFERENCES plant(plant_id)
);