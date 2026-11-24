use role useradmin;
create role if not exists transformer;
create user if not exists dbt_entrepot
    type = service
    default_role = transformer
    default_warehouse = wh_entrepot
    rsa_public_key = 'MIIBIjANBgkqh...';   -- ta clé publique, sans les lignes BEGIN et END
grant role transformer to user dbt_entrepot;
grant role transformer to user <TON_UTILISATEUR>;  -- pour tester toi-même avec ce rôle
grant role transformer to role sysadmin;           -- l'administrateur garde la main

use role sysadmin;
grant usage on warehouse wh_entrepot to role transformer;
grant usage on database entrepot to role transformer;
grant usage on schema entrepot.raw to role transformer;
grant select on all tables in schema entrepot.raw to role transformer;
grant select on future tables in schema entrepot.raw to role transformer;
grant usage, create table, create view on schema entrepot.staging to role transformer;
grant usage, create table, create view on schema entrepot.marts to role transformer;