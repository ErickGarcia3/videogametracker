CREATE DATABASE videogame;
USE videogame;

CREATE TABLE games (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
platform VARCHAR(50) NOT NULL,
play_status ENUM('Unplayed','Playing','Completed','Abandoned'),
hours_played DECIMAL(5,1),
rating INT(1),
store_url VARCHAR(512)
);

