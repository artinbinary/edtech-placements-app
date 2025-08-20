-- Description of analysis: SQL queries to gain insights on placement ready students 

-- Query 1: Filtering list of students "Ready" for placement with details of mock interview score and internships completed:
    
SELECT 
    s.Student_ID,
    s.Name,
    s.Email,
    p.Mock_Interview_Score,
    p.Internships_Completed,
    p.Placement_Status
FROM 
    Students s
JOIN 
    Placements p ON s.Student_ID = p.Student_ID
WHERE 
    p.Placement_Status = 'Ready';

#________________________________________________________________ #

-- Query 2: Filtering list of students "Ready" for placement with details of columns with all communication based scores, graduation year, city, languages learnt, problems_solved, assessments_completed, mini_projects, certifications_earned, and latest_project_score:

SELECT 
    s.Student_ID,
    s.Name,
    s.Graduation_Year,
    s.City,
    pr.Language,
    pr.Problems_Solved,
    pr.Assessments_Completed,
    pr.Mini_Projects,
    pr.Certifications_Earned,
    pr.Latest_Project_Score,
    ss.Communication_Score,
    ss.Teamwork_Score,
    ss.Presentation_Score,
    ss.Leadership_Score,
    ss.Critical_Thinking,
    ss.Interpersonal_Skills,
    p.Mock_Interview_Score
FROM 
    Students s
JOIN 
    Programming pr ON s.Student_ID = pr.Student_ID
JOIN 
    Soft_Skills ss ON s.Student_ID = ss.Student_ID
JOIN 
    Placements p ON s.Student_ID = p.Student_ID
WHERE 
    p.Placement_Status = 'Ready';

#________________________________________________________________ #

-- Query 3: Filtering list of students "Ready" for placement with highest mock interview scores, also showing all relevant scores and criteria from above two searches combined:

#ready folks with highest mock-interview scores
SELECT 
    s.Student_ID,
    s.Name,
    s.Email,
    s.Graduation_Year,
    s.City,
    pr.Language,
    pr.Problems_Solved,
    pr.Assessments_Completed,
    pr.Mini_Projects,
    pr.Certifications_Earned,
    pr.Latest_Project_Score,
    ss.Communication_Score,
    ss.Teamwork_Score,
    ss.Presentation_Score,
    ss.Leadership_Score,
    ss.Critical_Thinking,
    ss.Interpersonal_Skills,
    p.Mock_Interview_Score,
    p.Internships_Completed,
    p.Placement_Status
FROM 
    Students s
JOIN 
    Programming pr ON s.Student_ID = pr.Student_ID
JOIN 
    Soft_Skills ss ON s.Student_ID = ss.Student_ID
JOIN 
    Placements p ON s.Student_ID = p.Student_ID
WHERE 
    p.Placement_Status = 'Ready'
    # AND pr.Latest_Project_Score > 70
ORDER BY 
    p.Mock_Interview_Score DESC;

#________________________________________________________________ #

-- Context based filters:

-- Query 4: # "Ready" students for AI internship or fresher jobs with python & (pytorch or mistral or llama)
    # Usage of like instead of "group by" or "having" which did not yield any results despite removing language critria 1 by 1 to optional and also checking for any placement_status among students with the languages needed for AI interns

SELECT 
    s.`Student_ID`,
    s.`Name`,
    s.`City`,
    s.`Graduation_Year`,
    pr.`Language`,
    p.`Placement_Status`
    
FROM 
    `Students` s
JOIN 
    `Programming` pr ON s.`Student_ID` = pr.`Student_ID`
JOIN 
    `Placements` p ON s.`Student_ID` = p.`Student_ID`
WHERE 
    p.`Placement_Status` = 'Ready'
    AND (pr.`Language` LIKE '%PyTorch%' 
         OR pr.`Language` LIKE '%Mistral%' 
         OR pr.`Language` LIKE '%Llama%');

#________________________________________________________________ #

-- Query 5: Company wants candidate to take hacker rank or take a live coding test in interview. 

    SELECT 
    s.`Name`,
    s.`Student_ID`,
    s.`Graduation_Year`,
    s.`City`,
    pr.`Certifications_Earned`,
    pr.`Problems_Solved`,
    pr.`Mini_Projects`,
    p.`Placement_Status`
FROM 
    `Students` s
JOIN 
    `Programming` pr ON s.`Student_ID` = pr.`Student_ID`
JOIN 
    `Placements` p ON s.`Student_ID` = p.`Student_ID`
WHERE 
    p.`Placement_Status` = 'Ready'
    AND pr.`Mini_Projects` > 5
ORDER BY 
    pr.`Problems_Solved` DESC;

#________________________________________________________________ #

-- Query 6: High softskills score to filter students for techno-functional roles

CREATE OR REPLACE VIEW Techno_functional AS
SELECT 
    s.`Name`,
    s.`Student_ID`,
    ss.`Communication_Score`,
    ss.`Teamwork_Score`,
    ss.`Presentation_Score`,
    ss.`Leadership_Score`,
    ss.`Critical_Thinking`,
    ss.`Interpersonal_Skills`,
    (ss.`Communication_Score` + ss.`Teamwork_Score` + ss.`Presentation_Score` + 
     ss.`Leadership_Score` + ss.`Critical_Thinking` + ss.`Interpersonal_Skills`) / 6 AS `Average_Soft_Skills_Score`,
    p.`Placement_Status`,
    p.`Mock_Interview_Score`
FROM 
    `Students` s
JOIN 
    `Programming` pr ON s.`Student_ID` = pr.`Student_ID`
JOIN 
    `Soft_Skills` ss ON s.`Student_ID` = ss.`Student_ID`
JOIN 
    `Placements` p ON s.`Student_ID` = p.`Student_ID`
WHERE
	p.`Placement_Status` = 'Ready';
SELECT * FROM 
	Techno_functional
ORDER BY
	`average_soft_skills_score` DESC;

#________________________________________________________________ #

-- Query 7: Low soft skills scores but high technical scores among "Ready" Students for roles that are not client facing / company does not stress on communication skills 
    
# Include Ready students where Average Soft Skills ∈ [40, 70]

WITH prog AS (
  SELECT
    pr.`Student_ID`,
    AVG(CAST(pr.`Latest_Project_Score` AS DECIMAL(5,2)))           AS `Latest_Project_Score`,
    SUM(COALESCE(pr.`Problems_Solved`, 0))                         AS `Problems_Solved`,
    SUM(COALESCE(pr.`Assessments_Completed`, 0))                   AS `Assessments_Completed`,
    GROUP_CONCAT(DISTINCT pr.`Language` ORDER BY pr.`Language`)    AS `Language`,
    GROUP_CONCAT(DISTINCT pr.`Certifications_Earned` ORDER BY pr.`Certifications_Earned`) AS `Certifications_Earned`
  FROM `Programming` pr
  GROUP BY pr.`Student_ID`
),
soft_avg AS (
  SELECT
    ss.`Student_ID`,
    ROUND((
      ss.`Communication_Score` + ss.`Teamwork_Score` + ss.`Presentation_Score` +
      ss.`Leadership_Score` + ss.`Critical_Thinking` + ss.`Interpersonal_Skills`
    ) / 6.0) AS `Average_Soft_Skills_Score`
  FROM `Soft_Skills` ss
)
SELECT
  s.`Student_ID`,
  s.`Name`,
  sa.`Average_Soft_Skills_Score`,
  p.`Placement_Status`,
  COALESCE(CAST(p.`Mock_Interview_Score` AS DECIMAL(5,2)), 0)     AS `Mock_Interview_Score`,
  COALESCE(pg.`Latest_Project_Score`, 0)                           AS `Latest_Project_Score`,
  COALESCE(pg.`Problems_Solved`, 0)                                AS `Problems_Solved`,
  COALESCE(pg.`Assessments_Completed`, 0)                          AS `Assessments_Completed`,
  pg.`Language`,
  pg.`Certifications_Earned`,
  COALESCE(p.`Internships_Completed`, 0)                           AS `Internships_Completed`
FROM `Students` s
JOIN `Placements`  p  ON p.`Student_ID` = s.`Student_ID`
JOIN soft_avg      sa ON sa.`Student_ID` = s.`Student_ID`
JOIN `Soft_Skills` ss ON ss.`Student_ID` = s.`Student_ID`
LEFT JOIN prog     pg ON pg.`Student_ID` = s.`Student_ID`
WHERE
  (
    p.`Placement_Status` = 'Ready'
    AND sa.`Average_Soft_Skills_Score` BETWEEN 40 AND 70
  )
  
ORDER BY `Placement_Status` ASC, sa.`Average_Soft_Skills_Score` DESC, s.`Student_ID`;


#________________________________________________________________ #

-- Query 8: Checking which city has most "Ready" students so placements cell can target companies locally for placements
    
SELECT 
    s.`City`,
    COUNT(*) AS `Ready_Students_Count`
FROM 
    `Students` s
JOIN 
    `Placements` p 
    ON s.`Student_ID` = p.`Student_ID`
WHERE 
    p.`Placement_Status` = 'Ready'
GROUP BY 
    s.`City`
ORDER BY 
    `Ready_Students_Count` DESC
LIMIT 1;

#________________________________________________________________ #

-- Query 9: 2024 & 2025 passouts ready for placement ordered by mock interview scores

SELECT
    s.`Name`,
    s.`Student_ID`,
    s.`City` AS `Location`,
    s.`Graduation_Year`,
    p.`Placement_Status`,
    p.`Mock_Interview_Score`
FROM `Students` s
JOIN `Placements` p 
    ON s.`Student_ID` = p.`Student_ID`
JOIN `Programming` pr 
    ON s.`Student_ID` = pr.`Student_ID`
WHERE s.`Graduation_Year` in (2024, 2025)
  AND p.`Placement_Status` = 'Ready'
  
ORDER BY p.`Mock_Interview_Score` DESC;
    
#________________________________________________________________ #

-- Query 10: Analysing the success factors for placed students 

-- 1. Drop existing temporary tables to avoid conflicts
DROP TEMPORARY TABLE IF EXISTS `Score_Brackets`;
DROP TEMPORARY TABLE IF EXISTS `Certification_Counts`;
DROP TEMPORARY TABLE IF EXISTS `Internships_Count`;
DROP TEMPORARY TABLE IF EXISTS `Mock_Interview_Score_Brackets`;
DROP TEMPORARY TABLE IF EXISTS `Latest_Project_Score_Brackets`;

-- 2. Create a view for placed students' base data
CREATE OR REPLACE VIEW `Placed_Students_View` AS
SELECT 
    s.`Student_ID`,
    s.`Name`,
    ss.`Communication_Score`,
    ss.`Teamwork_Score`,
    ss.`Presentation_Score`,
    ss.`Leadership_Score`,
    ss.`Critical_Thinking`,
    ss.`Interpersonal_Skills`,
    ROUND(
        COALESCE(
            (ss.`Communication_Score` + ss.`Teamwork_Score` + ss.`Presentation_Score` + 
             ss.`Leadership_Score` + ss.`Critical_Thinking` + ss.`Interpersonal_Skills`) / 6.0, 
            0
        )
    ) AS `Average_Soft_Skills_Score`,
    p.`Placement_Status`,
    COALESCE(CAST(p.`Mock_Interview_Score` AS DECIMAL(5,2)), 0) AS `Mock_Interview_Score`,
    p.`Internships_Completed`,
    pr.`Certifications_Earned`,
    COALESCE(CAST(pr.`Latest_Project_Score` AS DECIMAL(5,2)), 0) AS `Latest_Project_Score`
FROM 
    `Students` s
JOIN 
    `Programming` pr ON s.`Student_ID` = pr.`Student_ID`
JOIN 
    `Soft_Skills` ss ON s.`Student_ID` = ss.`Student_ID`
JOIN 
    `Placements` p ON s.`Student_ID` = p.`Student_ID`
WHERE 
    p.`Placement_Status` = 'Placed';

-- 3. Create a reference table for score brackets
CREATE TEMPORARY TABLE `Score_Brackets` (
    `Bracket` VARCHAR(10),
    `Lower_Bound` INT,
    `Upper_Bound` INT
);
INSERT INTO `Score_Brackets` (`Bracket`, `Lower_Bound`, `Upper_Bound`)
VALUES 
    ('50-60', 50, 60),
    ('60-70', 61, 70),
    ('70-80', 71, 80),
    ('80-90', 81, 90),
    ('90-100', 91, 100);

-- 4. Most common certifications earned
CREATE TEMPORARY TABLE `Certification_Counts` AS
SELECT 
    TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(pr.`Certifications_Earned`, ',', numbers.n), ',', -1)) AS `Certification`,
    COUNT(*) AS `Certification_Count`
FROM 
    `Placements` p
JOIN 
    `Programming` pr ON p.`Student_ID` = pr.`Student_ID`
JOIN 
    (
        SELECT n
        FROM (
            SELECT a.N + b.N * 10 + 1 AS n
            FROM 
                (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
                 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
                (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
                 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
        ) AS nums
    ) numbers
WHERE 
    p.`Placement_Status` = 'Placed'
    AND numbers.n <= (
        LENGTH(COALESCE(pr.`Certifications_Earned`, '')) 
        - LENGTH(REPLACE(COALESCE(pr.`Certifications_Earned`, ''), ',', '')) 
        + 1
    )
GROUP BY 
    `Certification`
ORDER BY 
    `Certification_Count` DESC;

-- 5. Count of internships completed
CREATE TEMPORARY TABLE `Internships_Count` AS
SELECT 
    p.`Internships_Completed`,
    COUNT(*) AS `Student_Count`
FROM 
    `Placements` p
WHERE 
    p.`Placement_Status` = 'Placed'
    AND p.`Internships_Completed` >= 1
GROUP BY 
    p.`Internships_Completed`
ORDER BY 
    p.`Internships_Completed` ASC;

-- 6. Count of students by Mock_Interview_Score brackets
CREATE TEMPORARY TABLE `Mock_Interview_Score_Brackets` AS
SELECT 
    sb.`Bracket` AS `Mock_Interview_Score_Bracket`,
    COUNT(p.`Student_ID`) AS `Student_Count`
FROM 
    `Score_Brackets` sb
LEFT JOIN 
    `Placements` p 
    ON p.`Placement_Status` = 'Placed'
    AND COALESCE(CAST(p.`Mock_Interview_Score` AS DECIMAL(5,2)), 0) 
        BETWEEN sb.`Lower_Bound` AND sb.`Upper_Bound`
GROUP BY 
    sb.`Bracket`
ORDER BY 
    sb.`Bracket`;

-- 7. Count of students by Latest_Project_Score brackets
CREATE TEMPORARY TABLE `Latest_Project_Score_Brackets` AS
SELECT 
    sb.`Bracket` AS `Latest_Project_Score_Bracket`,
    COUNT(DISTINCT ps.`Student_ID`) AS `Student_Count`
FROM `Score_Brackets` sb
LEFT JOIN (
    SELECT 
        p.`Student_ID`,
        CAST(pr.`Latest_Project_Score` AS DECIMAL(5,2)) AS `Latest_Project_Score`
    FROM `Placements` p
    JOIN `Programming` pr 
      ON pr.`Student_ID` = p.`Student_ID`
    WHERE p.`Placement_Status` = 'Placed'
) AS ps
  ON ps.`Latest_Project_Score` BETWEEN sb.`Lower_Bound` AND sb.`Upper_Bound`
GROUP BY sb.`Bracket`
ORDER BY sb.`Bracket`;

-- 8. Display results
SELECT 'Certification Counts' AS `Result_Type`, `Certification`, `Certification_Count` AS `Value` 
FROM `Certification_Counts`
UNION ALL
SELECT 'Internships Completed' AS `Result_Type`, CAST(`Internships_Completed` AS CHAR), `Student_Count` 
FROM `Internships_Count`
UNION ALL
SELECT 'Mock Interview Score Brackets' AS `Result_Type`, `Mock_Interview_Score_Bracket`, `Student_Count` 
FROM `Mock_Interview_Score_Brackets`
UNION ALL
SELECT 'Latest Project Score Brackets' AS `Result_Type`, `Latest_Project_Score_Bracket`, `Student_Count` 
FROM `Latest_Project_Score_Brackets`
UNION ALL
SELECT 'Per Student Soft Skills Average' AS `Result_Type`, CONCAT(`Student_ID`, ' - ', `Name`), `Average_Soft_Skills_Score` 
FROM `Placed_Students_View`;

-- 9. Drop temporary tables
DROP TEMPORARY TABLE IF EXISTS `Score_Brackets`;
DROP TEMPORARY TABLE IF EXISTS `Certification_Counts`;
DROP TEMPORARY TABLE IF EXISTS `Internships_Count`;
DROP TEMPORARY TABLE IF EXISTS `Mock_Interview_Score_Brackets`;
DROP TEMPORARY TABLE IF EXISTS `Latest_Project_Score_Brackets`;









