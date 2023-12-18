DROP TABLE IF EXISTS plant_condition;
GO
DROP TABLE IF EXISTS plant;
GO
DROP TABLE IF EXISTS botanist;
GO
DROP TABLE IF EXISTS origin;
GO

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
    phone_number VARCHAR(20) UNIQUE NOT NULL,
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

GO

INSERT INTO botanist(first_name, surname, email, phone_number)
        VALUES
    ('Gertrude', 'Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
    ('Carl', 'Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
    ('Eliza', 'Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');
GO
