USE plants;
GO

DROP TABLE IF EXISTS s_epsilon.plant_condition;
GO
DROP TABLE IF EXISTS s_epsilon.plant;
GO
DROP TABLE IF EXISTS s_epsilon.botanist;
GO
DROP TABLE IF EXISTS s_epsilon.origin;
GO
DROP TABLE IF EXISTS s_epsilon.country;
GO
DROP TABLE IF EXISTS s_epsilon.continent;
GO

CREATE TABLE s_epsilon.continent (
    continent_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    continent_name VARCHAR(25) NOT NULL,
);

CREATE TABLE s_epsilon.country (
    country_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    country_name VARCHAR(30) UNIQUE NOT NULL,
    continent_id INT NOT NULL
    FOREIGN KEY (continent_id)
        REFERENCES s_epsilon.continent(continent_id)
);

CREATE TABLE s_epsilon.origin (
    origin_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    region VARCHAR(50) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id)
        REFERENCES s_epsilon.country(country_id)
);

CREATE TABLE s_epsilon.botanist (
    botanist_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(25) NOT NULL,
    surname VARCHAR(25) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
);

CREATE TABLE s_epsilon.plant (
    plant_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(50) NOT NULL,
    scientific_name VARCHAR(50) NOT NULL,
    botanist_id INT NOT NULL,
    origin_id INT NOT NULL,
    FOREIGN KEY (botanist_id)
        REFERENCES s_epsilon.botanist(botanist_id),
    FOREIGN KEY (origin_id)
        REFERENCES s_epsilon.origin(origin_id)
);

CREATE TABLE s_epsilon.plant_condition (
    plant_condition_id INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    at TIMESTAMP NOT NULL,
    soil_moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    plant_id INT NOT NULL,
    FOREIGN KEY (plant_id)
        REFERENCES s_epsilon.plant(plant_id)
);

GO

INSERT INTO s_epsilon.continent (continent_name)
        VALUES
    ('America'),
    ('Africa'),
    ('Asia'),
    ('Europe');
GO

INSERT INTO s_epsilon.country (country_name, continent_id)
        VALUES
    ('Brazil', 1),
    ('USA', 1),
    ('Nigeria', 2),
    ('El Salvador', 1),
    ('Indonesia', 3),
    ('Canada', 1),
    ('Ivory Coast', 2),
    ('Germany', 4),
    ('Croatia', 4),
    ('Tunisia', 2),
    ('Botswana', 2),
    ('Spain', 4),
    ('Japan', 3),
    ('Sudan', 2),
    ('Algeria', 2),
    ('Ukraine', 4),
    ('Libya', 2),
    ('China', 3),
    ('Chile', 1),
    ('Tanzania', 2),
    ('France', 4),
    ('Bulgaria', 4),
    ('Mexico', 1),
    ('Malawi', 2),
    ('Italy', 4),
    ('Philippines', 3);
GO


INSERT INTO s_epsilon.botanist(first_name, surname, email, phone_number)
        VALUES
    ('Gertrude', 'Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
    ('Carl', 'Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
    ('Eliza', 'Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');
GO

INSERT INTO s_epsilon.origin(latitude, longitude, region, country_id)
        VALUES
    (-19.32556, -41.25528, 'Resplendor', 1),
    (33.95015, -118.03917, 'South Whittier', 2),
    (7.65649, 4.92235, 'Efon-Alaaye', 3),
    (13.70167, -89.10944, 'Ilopango', 4),
    (22.88783, 84.13864, 'Jashpurnagar', 5),
    (43.86682, -79.2663, 'Markham', 6),
    (5.27247, -3.59625, 'Bonoua', 7),
    (50.9803, 11.32903, 'Weimar', 8),
    (43.50891, 16.43915, 'Split', 9),
    (20.88953, -156.47432, 'Kanului', 2),
    (32.5007, -94.74049, 'Longview', 2),
    (49.68369, 8.61839, 'Bensheim', 8),
    (29.65163, -82.32483, 'Gainesville', 2),
    (36.08497, 9.37082, 'Siliana', 10),
    (40.93121, -73.89875, 'Yonkers', 2),
    (-7.51611, 109.05389, 'Wangon', 5),
    (51.30001, 13.10984, 'Oschatz', 8),
    (-21.44236, 27.46153, 'Tonota', 11),
    (41.15612, 1.10687, 'Reus', 12),
    (-29.2975, -51.50361, 'Carlos Barbosa', 1),
    (48.35693, 10.98461, 'Friedberg', 8),
    (52.53048, 13.29371, 'Charlottenburg-Nord', 8),
    (43.82634, 144.09638, 'Motomachi', 13),
    (11.8659, 34.3869, 'Ar Ruseris', 14),
    (36.06386, 4.62744, 'El Achir', 15),
    (51.67822, 33.9162, 'Hlukhiv', 16),
    (43.91452, -69.96533, 'Brunswick', 2),
    (34.75856, 136.13108, 'Ueno-ebisumachi', 13),
    (30.75545, 20.22625, 'Ajdabiya', 17),
    (23.29549, 113.82465, 'Licheng', 18),
    (52.47774, 10.5511, 'Gifhorn', 8),
    (28.92694, 78.23456, 'Bachhraon', 5),
    (-32.45242, -71.23106, 'La Ligua', 19),
    (32.54044, -82.90375, 'Dublin', 2),
    (30.21121, 74.4818, 'Malaut', 5),
    (-6.8, 39.25, 'Magomeni', 20), 
    (36.24624, 139.07204, 'Fujioka', 13),
    (44.92801, 4.8951, 'Valence', 21),
    (22.4711, 88.1453, 'Pujali', 5),
    (41.57439, 24.71204, 'Smolyan', 22),
    (20.22816, -103.5687, 'Zacoalco de Torres', 23),
    (-13.7804, 34.4587, 'Salima', 24),
    (37.49223, 15.07041, 'Catania', 25),
    (14.14989, 121.3152, 'Calauan', 26),
    (17.94979, -94.91386, 'Acayucan', 23);

INSERT INTO s_epsilon.plant(plant_name, scientific_name, botanist_id, origin_id)
        VALUES
    ('Epipremnum Aureum', 'Epipremnum aureum', 2, 1),
    ('Venus flytrap', 'N/A', 1, 2),
    ('Corpse flower', 'N/A', 2, 3),
    ('Rafflesia arnoldii', 'N/A', 3, 1),
    ('Black bat flower', 'N/A', 2, 4),
    ('Pitcher plant', 'Sarracenia catesbaei', 2, 5),
    ('Wollemi pine', 'Wollemia nobilis', 3, 6),
    ('Not Found' , 'Not Found', 1, 1),
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
    ('On Loan', 'On Loan', 1, 1),
    ('Araucaria Heterophylla', 'Araucaria heterophylla', 1, 41),
    ('Begonia ''Art Hodes''', 'N/A', 1, 2),
    ('Medinilla Magnifica', 'Medinilla magnifica', 3, 42),
    ('Calliandra Haematocephala', 'Calliandra haematocephala', 3, 43),
    ('Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 2, 44),
    ('Crassula Ovata', 'Crassula ovata', 3, 45),
    ('Epipremnum Aureum', 'Epipremnum aureum', 2, 1);
GO