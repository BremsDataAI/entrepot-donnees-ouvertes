-- Créer les objets
use role sysadmin;

create warehouse if not exists wh_entrepot
    warehouse_size = 'XSMALL'
    auto_suspend = 60          -- secondes sans requête avant l'arrêt
    auto_resume = true
    initially_suspended = true -- ne démarre pas à la création
    comment = 'Entrepôt de données ouvertes du Sénégal';

create database if not exists entrepot;
create schema if not exists entrepot.raw;      -- données brutes, chargées par tes scripts
create schema if not exists entrepot.staging;  -- modèles stg_ de dbt
create schema if not exists entrepot.marts;    -- dimensions et faits