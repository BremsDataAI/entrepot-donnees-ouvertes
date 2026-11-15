WITH source AS (
    SELECT * FROM {{ source('raw', 'wb_cpi_annual') }}
    WHERE "Country Name" = 'Senegal'
),

pivote AS (
  UNPIVOT source
  ON COLUMNS(* EXCLUDE (
    "Country Name",
    "Country Code",
    "Indicator Name",
    "Indicator Code"
  ))
  INTO NAME annee VALUE valeur
),

renomme AS (
  SELECT
    "Country Name"           AS pays,
    "Indicator Name"         AS indicateur,
    cast(annee AS integer)   AS annee,
    cast(valeur AS double)   AS valeur
  FROM pivote
  WHERE cast(annee AS integer) >= 2000
)

SELECT * FROM renomme
