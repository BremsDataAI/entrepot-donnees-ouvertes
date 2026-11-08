import duckdb

con = duckdb.connect("entrepot.duckdb")
con.sql("CREATE SCHEMA IF NOT EXISTS raw")
con.sql("""
    CREATE OR REPLACE TABLE raw.pam_prix AS
    SELECT * FROM read_csv('data/raw/pam/wfp_food_prices_sen.csv', all_varchar=true)
""")
con.close()
