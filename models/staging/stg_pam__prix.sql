WITH source AS (
    SELECT * FROM {{ source('raw', 'pam_prix') }}
    WHERE date <> '#date'           -- ligne de balises HXL
),

renomme AS (
  SELECT
    cast(date as date)    AS date_releve,
    admin1                AS region,
    admin2                AS departement,
    market                AS marche,
    category              AS categorie,
    commodity             AS produit,
    unit                  AS unite,
    pricetype             AS type_prix,
    currency              AS devise,
    cast(price as double) AS prix
  FROM source
)

SELECT * FROM renomme