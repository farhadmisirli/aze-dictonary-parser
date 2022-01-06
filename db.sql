CREATE DATABASE aze_dictonary CHARACTER SET utf8 COLLATE utf8_general_ci;

use aze_dictonary;

CREATE TABLE words(
    id int primary key auto_increment,
    text varchar(32) not null,
    description text default null
);