--DROP VIEW v_tags;
CREATE VIEW v_tags AS 
SELECT
 game.name as game,
 tag.name as tag
FROM
 game_tags
INNER JOIN game ON game.id_game = game_tags.fk_game
INNER JOIN tag ON tag.id_tag = game_tags.fk_tag