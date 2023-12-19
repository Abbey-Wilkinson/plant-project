DROP TABLE IF EXISTS plant_condition;
GO
DROP TABLE IF EXISTS plant;
GO
DROP TABLE IF EXISTS botanist;
GO
DROP TABLE IF EXISTS origin;
GO

CREATE TABLE epsilon.continent (
    continent_id INT GENERATED ALWAYS AS IDENTITY,
    continent_name VARCHAR(25)
);

CREATE TABLE epsilon.origin (
    origin_id INT GENERATED ALWAYS AS IDENTITY,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(25) NOT NULL,
    continent_id INT NOT NULL,
    PRIMARY KEY (origin_id),
    FOREIGN KEY (continent_id)
        REFERENCES continent(continent_id)
);

CREATE TABLE epsilon.botanist (
    botanist_id INT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(25) NOT NULL,
    surname VARCHAR(25) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE epsilon.plant (
    plant_id INT GENERATED ALWAYS AS IDENTITY,
    plant_name VARCHAR(50) UNIQUE NOT NULL,
    scientific_name VARCHAR(50) UNIQUE NOT NULL,
    botanist_id INT NOT NULL,
    origin_id INT NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id)
        REFERENCES botanist(botanist_id),
    FOREIGN KEY (origin_id)
        REFERENCES origin(origin_id)
);

CREATE TABLE epsilon.plant_condition (
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

INSERT INTO epsilon.continent(continent_name)
        VALUES
    ('America'),
    ('Africa'),
    ('Asia'),
    ('Europe'),
    ('Pacific')

INSERT INTO epsilon.botanist(first_name, surname, email, phone_number)
        VALUES
    ('Gertrude', 'Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
    ('Carl', 'Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
    ('Eliza', 'Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');
GO

INSERT INTO epsilon.origin(longitude, latitude, region, country, continent_id)
        VALUES
    (-19.32556, -41.25528, 'Resplendor', 'Brazil', 1),
    (33.95015, -118.03917, 'South Whittier', 'USA', 1),
    (7.65649, 4.92235, 'Efon-Alaaye', 'Nigeria', 2),
    (13.70167, -89.10944, 'Ilopango', 'El Salvador', 1),
    (22.88783, 84.13864, 'Jashpurnagar', 'Indonesia', 3),
    (43.86682, -79.2663, 'Markham', 'Canada', 1),
    (5.27247, -3.59625, 'Bonoua', 'Ivory Coast', 1),
    (50.9803, 11.32903, 'Weimar', 'Germany', 4),
    (43.50891, 16.43915, 'Split', 'Croatia', 4),
    (20.88953, -156.47432, 'Kanului', 'USA', 5),
    (32.5007, -94.74049, 'Longview', 'USA', 1),
    (49.68369, 8.61839, 'Bensheim', 'Germany', 4),
    (29.65163, -82.32483, 'Gainesville', 'USA', 1),
    (36.08497, 9.37082, 'Siliana', 'Tunisia', 2),
    (40.93121, -73.89875, "Yonkers", "USA", 1),
    (-7.51611, 109.05389, "Wangon", "Indonesia", 3),
    (51.30001, 13.10984, "Oschatz", "Germany", 4),
    (-21.44236, 27.46153, 'Tonota', 'Botswana', 2),
    (41.15612, 1.10687, 'Reus', 'Spain', 4),
    (-29.2975, -51.50361, 'Carlos Barbosa', 'Brazil', 1),
    (48.35693, 10.98461, 'Friedberg', 'Germany', 4),
    (52.53048, 13.29371, 'Charlottenburg-Nord', 'Germany', 4),
    (43.82634, 144.09638, 'Motomachi', 'Japan', 3),
    (11.8659, 34.3869, 'Ar Ruseris', 'Sudan', 2),
    (36.06386, 4.62744, 'El Achir', 'Algeria', 2),
    (51.67822, 33.9162, 'Hlukhiv', 'Ukraine', 4),
    (43.91452, -69.96533, 'Brunswick', 'USA', 1),
    (34.75856, 136.13108, 'Ueno-ebisumachi', 'Japan', 3),
    (30.75545, 20.22625, 'Ajdabiya', 'Libya', 2),
    (23.29549, 113.82465, 'Licheng', 'China', 3),
    (52.47774, 10.5511, 'Gifhorn', 'Germany', 4),
    (28.92694, 78.23456, 'Bachhraon', 'Indonesia', 3),
    (-32.45242, -71.23106, 'La Ligua', 'Chile', 1),
    (32.54044, -82.90375, 'Dublin', 'USA', 1),
    (30.21121, 74.4818, 'Malaut', 'Indonesia', 3),
    (-6.8, 39.25, 'Magomeni', 'Tanzania', 2), 
    (36.24624, 139.07204, 'Fujioka', 'Japan', 3),
    (44.92801, 4.8951, 'Valence', 'France', 4),
    (22.4711, 88.1453, 'Pujali', 'Indonesia', 3),
    (41.57439, 24.71204, 'Smolyan', 'Bulgaria', 4),
    (20.22816, -103.5687, 'Zacoalco de Torres', 'Mexico', 1),
    (-13.7804, 34.4587, 'Salima', 'Malawi', 2),
    (37.49223, 15.07041, 'Catania', 'Italy', 4),
    (14.14989, 121.3152, 'Calauan', 'Philippines', 3),
    (17.94979, -94.91386, 'Acayucan', 'Mexico', 1);

INSERT INTO epsilon.plant(plant_name, scientific_name, botanist_id, origin_id)
        VALUES
    ('Epipremnum Aureum', 'Epipremnum aureum', 2, 1),
    ('Venus flytrap', 'N/A', 1, 2),
    ('Corpse flower', 'N/A', 2, 3),
    ('Rafflesia arnoldii', 'N/A', 3, 1),
    ('Black bat flower', 'N/A', 2, 4),
    ('Pitcher plant', 'Sarracenia catesbaei', 2, 5),
    ('Wollemi pine', 'Wollemia nobilis', 3, 6),
    ('Not Found'),
    ('Bird of paradise', 'Heliconia schiedeana ''Fire and Ice''', 3, 7),
    ('Cactus', 'Pereskia grandifolia', 1, 8),
    ('Dragon tree', 'N/A', 1, 9),
    ('Asclepias Curassavica', 'Asclepias curassavica', 1, 10),
    ('Brugmansia X Candida', 'N/A', 3, 11),
    ('Canna ‘Striata’', 'N/A', 3, 12),
    ('Colocasia Esculenta', 'Colocasia esculenta', 1, 13),
    ('Cuphea ‘David Verity’', 'N/A', 1, 14),
    ('Euphorbia Cotinifolia', 'Euphorbia cotinifolia', 1, 15),
    ('Ipomoea Batatas', 'Ipomoea batatas', 2, 16),
    ('Manihot Esculenta ‘Variegata’', 'N/A', 2, 17),
    ('Musa Basjoo', 'Musa basjoo', 1, 18),
    ('Salvia Splendens', 'Salvia splendens', 2, 19),
    ('Anthurium', 'Anthurium andraeanum', 3, 20),
    ('Bird of Paradise', 'Heliconia schiedeana ''Fire and Ice''', 1, 21),
    ('Cordyline Fruticosa', 'Cordyline fruticosa', 3, 22),
    ('Ficus', 'Ficus carica', 2, 23),
    ('Palm Trees', 'N/A', 1, 24),
    ('Dieffenbachia Seguine', 'Dieffenbachia seguine', 2, 25),
    ('Spathiphyllum', 'Spathiphyllum (group)', 2, 26),
    ('Croton', 'Codiaeum variegatum', 2, 27),
    ('Aloe Vera', 'Aloe vera', 1, 28),
    ('Ficus Elastica', 'icus elastica', 2, 29),
    ('Sansevieria Trifasciata', 'Sansevieria trifasciata', 1, 30),
    ('Philodendron Hederaceum', 'Philodendron hederaceum', 1, 31),
    ('Schefflera Arboricola', 'Schefflera arboricola', 2, 32),
    ('Aglaonema Commutatum', 'Aglaonema commutatum', 1, 19),
    ('Monstera Deliciosa', 'Monstera deliciosa', 2, 33),
    ('Tacca Integrifolia', 'Tacca integrifolia', 1, 34),
    ('Psychopsis Papilio', 'N/A', 3, 35),
    ('Saintpaulia Ionantha', 'Saintpaulia ionantha', 1, 36),
    ('Gaillardia', 'Gaillardia aestivalis', 2, 37),
    ('Amaryllis', 'Hippeastrum (group)', 3, 38),
    ('Caladium Bicolor', 'Caladium bicolor', 2, 39),
    ('Chlorophytum Comosum', 'Chlorophytum comosum ''Vittatum''', 2, 40),
    ('Loan'),
    ('Araucaria Heterophylla', 'Araucaria heterophylla', 1, 41),
    ('Begonia ''Art Hodes''', 'N/A', 1, 2),
    ('Medinilla Magnifica', 'Medinilla magnifica', 3, 42),
    ('Calliandra Haematocephala', 'Calliandra haematocephala', 3, 43),
    ('Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 2, 44),
    ('Crassula Ovata', 'Crassula ovata', 3, 45),
    ('Epipremnum Aureum', 'Epipremnum aureum', 2, 1);