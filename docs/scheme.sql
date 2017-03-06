create database flaskr;

use flaskr;

CREATE TABLE user (
	id INTEGER NOT NULL,
	username VARCHAR(80),
	password VARCHAR(20),
	email VARCHAR(120),
	PRIMARY KEY (id),
	UNIQUE (username),
	UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE category (
	id INTEGER NOT NULL,
	name VARCHAR(50),
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE post (
	id INTEGER NOT NULL,
	title VARCHAR(80),
	body TEXT,
	pub_date DATETIME,
	category_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(category_id) REFERENCES category (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

