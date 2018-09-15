--DROP VIEW v_games;
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
INNER JOIN amount_type ON amount_type.id_amount_type = meal_ingradients.fk_amount_type
