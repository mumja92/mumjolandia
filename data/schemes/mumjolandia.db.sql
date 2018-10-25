BEGIN TRANSACTION;
DROP TABLE IF EXISTS "game";
CREATE TABLE IF NOT EXISTS "game" (
	"id_game"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "game_instance";
CREATE TABLE IF NOT EXISTS "game_instance" (
	"id_game_instance"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"fk_game"	INTEGER NOT NULL,
	"year"	INTEGER,
	"fk_platform"	INTEGER NOT NULL,
	"fk_drm"	INTEGER NOT NULL,
	FOREIGN KEY("fk_platform") REFERENCES "platform"("id_platform"),
	FOREIGN KEY("fk_game") REFERENCES "game"("id_game"),
	FOREIGN KEY("fk_drm") REFERENCES "drm"("id_drm")
);
DROP TABLE IF EXISTS "drm";
CREATE TABLE IF NOT EXISTS "drm" (
	"id_drm"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "game_tags";
CREATE TABLE IF NOT EXISTS "game_tags" (
	"id_game_tags"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"fk_game"	INTEGER NOT NULL,
	"fk_tag"	INTEGER NOT NULL,
	FOREIGN KEY("fk_tag") REFERENCES "tag"("id_tag"),
	FOREIGN KEY("fk_game") REFERENCES "game"("id_game")
);
DROP TABLE IF EXISTS "tag";
CREATE TABLE IF NOT EXISTS "tag" (
	"id_tag"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "platform";
CREATE TABLE IF NOT EXISTS "platform" (
	"id_platform"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL UNIQUE
);
DROP INDEX IF EXISTS "ix_game_instance";
CREATE UNIQUE INDEX IF NOT EXISTS "ix_game_instance" ON "game_instance" (
	"fk_game",
	"fk_platform",
	"fk_drm"
);
DROP INDEX IF EXISTS "ix_game_tag";
CREATE UNIQUE INDEX IF NOT EXISTS "ix_game_tag" ON "game_tags" (
	"fk_game"	ASC,
	"fk_tag"	ASC
);
DROP VIEW IF EXISTS "v_tags";
CREATE VIEW v_tags AS 
SELECT
 game.name as game,
 tag.name as tag
FROM
 game_tags
INNER JOIN game ON game.id_game = game_tags.fk_game
INNER JOIN tag ON tag.id_tag = game_tags.fk_tag;
DROP VIEW IF EXISTS "v_games";
CREATE VIEW v_games AS 
SELECT
 game.name as name,
 year as year,
 platform.name as platform,
 drm.name as drm
FROM
 game_instance
INNER JOIN platform ON platform.id_platform = game_instance.fk_platform
INNER JOIN game ON game.id_game = game_instance.fk_game
INNER JOIN drm ON drm.id_drm = game_instance.fk_drm;
COMMIT;
