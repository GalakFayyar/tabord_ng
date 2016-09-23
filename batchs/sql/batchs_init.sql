CREATE TABLE batchs_laboratoires(
	id SERIAL NOT NULL,
	libelle VARCHAR(50) NOT NULL,
	CONSTRAINT prk_constraint_batchs_laboratoires PRIMARY KEY (id)
);

CREATE TABLE batchs_produits(
	id SERIAL NOT NULL,
	code07 VARCHAR(50) NOT NULL,
	code13 VARCHAR(50) NOT NULL,
	libelle VARCHAR(50) NOT NULL,
	codeLaboratoire VARCHAR(50) NOT NULL,
	txTVA VARCHAR(50) NOT NULL,
	CONSTRAINT prk_constraint_batchs_produits PRIMARY KEY (id)
);

CREATE TABLE batchs_ventes(
	id SERIAL NOT NULL,
	periode VARCHAR(50) NOT NULL,
	codeCIP VARCHAR(50) NOT NULL,
	idArticle VARCHAR(50) NOT NULL,
	quantite VARCHAR(50) NOT NULL,
	prixAchatHT VARCHAR(50) NOT NULL,
	CAHT VARCHAR(50) NOT NULL,
	CATTC VARCHAR(50) NOT NULL,
	CONSTRAINT prk_constraint_batchs_ventes PRIMARY KEY (id)
);