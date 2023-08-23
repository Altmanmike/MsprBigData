-- 1) 
-- Attribution des poids selon la gravité ou degré de violence des classes de crime
--
ALTER TABLE Criminalité
ADD poids INT;

UPDATE Criminalité
SET poids = 
  CASE
    WHEN classe IN ('Violences sexuelles', 'Vols avec armes') THEN 5
    WHEN classe IN ('Vols violents sans arme', 'Autres coups et blessures volontaires', 'Coups et blessures volontaires intrafamiliaux', 'Coups et blessures volontaires') THEN 4
    WHEN classe IN ('Vols de véhicules', 'Cambriolages de logement', 'Destructions et dégradations volontaires') THEN 3
    WHEN classe IN ('Vols sans violence contre des personnes', 'Vols d''accessoires sur véhicules', 'Vols dans les véhicules') THEN 2
    ELSE 0
  END;


-- 2) 
-- Ajout du champ "indice_crim" à la table Criminalité2 (FLOAT ou DECIMAL ?)
--
ALTER TABLE Criminalité
ADD indice_crim FLOAT;

-- Calcule de l'indice de criminalité pour chaque crime i.e. ici Taux de criminalité normalisé si on ne met pas * 1000
UPDATE Criminalité
SET indice_crim = (CAST(poids AS FLOAT) / 5) * (CAST(faits AS FLOAT) / POP);


-- 3) 
-- Créer une vue pour obtenir l'indice de criminalité final en classant les départements i.e. ici la moyenne du taux de criminalité normalisé pour toutes les années disponibles pour chaque département
--
CREATE VIEW Indice_Criminalité_Final AS
SELECT Code_département, indice_crim_final
FROM (
    SELECT Code_département, SUM(indice_crim) AS indice_crim_final,
           ROW_NUMBER() OVER (ORDER BY SUM(indice_crim) ASC) AS classement
    FROM Criminalité2
    GROUP BY Code_département
) AS ClassementDepartements;