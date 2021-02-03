BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `recipe_day` (
	`id_recipe_day`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`fk_breakfast`	INTEGER NOT NULL,
	`fk_second_breakfast`	INTEGER NOT NULL,
	`fk_dinner`	INTEGER NOT NULL,
	`fk_tea`	INTEGER NOT NULL,
	`fk_supper`	INTEGER NOT NULL,
	FOREIGN KEY(`fk_supper`) REFERENCES `meal_ingradients`(`id_meal_ingradients`),
	FOREIGN KEY(`fk_second_breakfast`) REFERENCES `meal_ingradients`(`id_meal_ingradients`),
	FOREIGN KEY(`fk_dinner`) REFERENCES `meal_ingradients`(`id_meal_ingradients`),
	FOREIGN KEY(`fk_breakfast`) REFERENCES `meal_ingradients`(`id_meal_ingradients`),
	FOREIGN KEY(`fk_tea`) REFERENCES `meal_ingradients`(`id_meal_ingradients`)
);
CREATE TABLE IF NOT EXISTS `meal_type` (
	`id_meal_type`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `meal_ingradients` (
	`id_meal_ingradients`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`fk_meal_id`	INTEGER NOT NULL,
	`fk_ingradient_id`	INTEGER NOT NULL,
	`fk_amount_type`	INTEGER NOT NULL,
	`amount`	INTEGER NOT NULL,
	FOREIGN KEY(`fk_amount_type`) REFERENCES `amount_type`(`id_amount_type`),
	FOREIGN KEY(`fk_meal_id`) REFERENCES `meal`(`id_meal`),
	FOREIGN KEY(`fk_ingradient_id`) REFERENCES `ingradient`(`id_ingradient`)
);
CREATE TABLE IF NOT EXISTS `meal` (
	`id_meal`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`fk_meal_type`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL UNIQUE,
	`recipe`	TEXT,
	FOREIGN KEY(`fk_meal_type`) REFERENCES `meal_type`(`id_meal_type`)
);
CREATE TABLE IF NOT EXISTS `ingradient` (
	`id_ingradient`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS `amount_type` (
	`id_amount_type`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE
);
INSERT INTO `amount_type` VALUES (1,'g');
INSERT INTO `amount_type` VALUES (2,'number');
INSERT INTO `amount_type` VALUES (3,'a_little');
INSERT INTO `amount_type` VALUES (4,'ml');
INSERT INTO `amount_type` VALUES (5,'handful');
INSERT INTO `amount_type` VALUES (6,'slice');
INSERT INTO `amount_type` VALUES (7,'spoon');
CREATE UNIQUE INDEX IF NOT EXISTS `ix_meal_ingradients` ON `meal_ingradients` (
	`fk_meal_id`,
	`fk_ingradient_id`
);
CREATE VIEW v_meal AS 
SELECT
 meal.name as name,
 ingradient.name as 'ingradient',
 amount_type.name as 'amount type',
 amount as 'amount' 
FROM
 meal_ingradients
INNER JOIN meal ON meal.id_meal = meal_ingradients.fk_meal_id
INNER JOIN ingradient ON ingradient.id_ingradient = meal_ingradients.fk_ingradient_id
INNER JOIN amount_type ON amount_type.id_amount_type = meal_ingradients.fk_amount_type;
COMMIT;
