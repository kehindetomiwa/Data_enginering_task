CREATE TABLE IF NOT EXISTS app(
	pk BIGSERIAL NOT NULL PRIMARY KEY, 
	id VARCHAR(50) NOT NULL,
	title VARCHAR(50) NOT NULL,
	rating NUMERIC (2,1) ,
	last_update DATE NOT NULL
);

INSERT INTO app (id, title, rating, last_update) values ('com.facebook.katana', 'Facebook', 4.0, '2016-09-12');
INSERT INTO app (id, title, rating, last_update) values ('com.whatsapp', 'WhatsApp', 4.5, '2016-09-11');
INSERT INTO app (id, title, rating, last_update) values ('com.whatsapp', 'WhatsApp', 4.4, '2016-09-12');
INSERT INTO app (id, title, rating, last_update) values ('com.nianticlabs.pokemongo', 'Pokémon GO', 4.6, '2016-09-05');
INSERT INTO app (id, title, rating, last_update) values ('com.nianticlabs.pokemongo', 'Pokémon GO', 4.3, '2016-09-06');
INSERT INTO app (id, title, rating, last_update) values ('com.nianticlabs.pokemongo', 'Pokémon GO', 4.1, '2016-09-07');

