-- creaing ComputeAverageWeightedScoreForUser

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_score FLOAT;

    SELECT SUM(weight) INTO total_weight FROM projects 
    INNER JOIN corrections ON projects.id = corrections.project_id 
    WHERE corrections.user_id = user_id;

    SELECT SUM(score * weight) / total_weight INTO weighted_score FROM corrections 
    INNER JOIN projects ON corrections.project_id = projects.id 
    WHERE corrections.user_id = user_id;

    UPDATE users SET average_score = weighted_score WHERE id = user_id;
END;//
DELIMITER ;
