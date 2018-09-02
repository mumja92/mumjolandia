--DROP VIEW v_games;
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
INNER JOIN drm ON drm.id_drm = game_instance.fk_drm