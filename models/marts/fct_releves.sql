{{ config(
     materialized='incremental',
     unique_key=['date_releve', 'marche', 'produit', 'unite', 'type_prix']
) }}

SELECT * FROM {{ ref('stg_pam__prix') }}
{% if  is_incremental() %}
WHERE date_releve > (SELECT max(date_releve) FROM {{ this }})
{% endif %}