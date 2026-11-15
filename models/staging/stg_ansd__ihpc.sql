WITH source AS (
    SELECT * FROM {{ source('raw', 'ansd_ihpc') }}
),

renomme AS (
  SELECT 
    indicateurs                              AS indice,
    Unit                                     AS unite,
    cast(
        strptime(replace("Date", 'M', '-'), '%Y-%m')
        AS date
    )                                        AS date,
    cast(Value AS double)                    AS valeur
   FROM source
)

SELECT * FROM renomme