# Analyse de la table des prix du PAM
---

Méthodologie : choisir une mesure, déclarer le grain, identifier les dimensions, identifier les faits. 

## 1. Choisir une mesure
---
La mesure est le prix relevé d'un produit

## 2. Déclarer le grain 
---
Le grain représente ce qu'est une ligne de la table de fait. 
Nous définissons ici le grain comme : *le prix d'un produit, dans une unité, pour un type (détail ou gros), dans un marché, sur un mois.*

La requête sql permettant de vérifier que le grain choisi est correct, c'est à dire qu'il ne contient pas de doublons et ne mélange pas plusieurs grain est la suivante : 
```sql
SELECT price, commodity, unit, pricetype, market, date, count(*) AS n
FROM pam_prices
GROUP BY all
HAVING count(*) > 1;
```

## 3. Identification des faits, des dimensions et de leurs attributs
---
Cette partie concerne l'identification des tables de faits, des tables de dimensions ainsi que leurs attributs.
- Identification des faits
  * fct_prix (le prix d'un produit) : price, usdprice
- Identification des dimensions 
  * dim_product (produit) : commodity, commodity_id, category, unit
  * dim_market (marche) : market, market_id, admin1, admin2, latitude, longitude
  * dim_date (date) : date
- *Cas particulier* : attributs du relevé
Les attributs 'priceflag', 'pricetype', et 'currency' sont des attributs du relevé. Ils peuvent être rattachés à la table de faits. 
