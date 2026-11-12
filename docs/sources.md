# Sources de données : prix alimentaires et inflation au Sénégal

Ce document recense les trois sources de données utilisées pour analyser l'évolution des prix des denrées alimentaires et de l'inflation au Sénégal. Elles combinent des prix de marché relevés par le PAM (via HDX), l'inflation annuelle des prix à la consommation de la Banque mondiale depuis 2000, et l'indice harmonisé des prix à la consommation (IHPC, base 100 : 2023) de l'ANSD, filtré sur les produits alimentaires, de 2016 à 2025.

| Source | Jeu de données | Page de téléchargement | Accès API | Licence |
|---|---|---|---|---|
| HDX | Prix alimentaires du PAM, 2000-2026| [Page HDX](https://data.humdata.org/dataset/wfp-food-prices-for-senegal/resource/04ffc070-6d05-4653-a9f6-9f3f893a229e) | [Téléchargement CSV](https://data.humdata.org/dataset/77b76bc7-1edd-43f6-a5e4-784498ff6aca/resource/04ffc070-6d05-4653-a9f6-9f3f893a229e/download/wfp_food_prices_sen.csv) | [Licences HDX](https://docs.humdata.org/about/data-licenses) |
| World Bank | Inflation annuelle des prix à la consommation (FP.CPI.TOTL), 2000-2025 | [Page World Bank](https://data.worldbank.org/indicator/FP.CPI.TOTL?end=2025&locations=SN&start=2000&view=chart) | [API CSV](https://api.worldbank.org/v2/country/sn/indicator/FP.CPI.TOTL?date=2000:2025&downloadformat=csv) | [CC-BY 4.0](https://datacatalog.worldbank.org/public-licenses#cc-by) |
| ANSD | IHPC (base 100 : 2023), filtre : produits alimentaires, 2016-2025 | [Page ANSD](https://senegal.opendataforafrica.org/tsghpfc/indice-harmonis%C3%A9-des-prix-%C3%A0-la-consommation-ihpc-base-100-2023) | Package Python `knoema` : `knoema.get('tsghpfc', timerange='2016M1-2026M12', Indicateurs='011')` | [Licence ANSD](https://nso-senegal.opendataforafrica.org/hiwidxb) |
