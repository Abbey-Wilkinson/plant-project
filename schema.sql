DROP TABLE IF EXISTS plant_condition;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS origin;

CREATE TABLE plant_condition (
    plant_condition_id INT GENERATED ALWAYS AS IDENTITY,
    at TIMESTAMPTZ NOT NULL,
    soil_moisture FLOAT NULL NULL,
    
)