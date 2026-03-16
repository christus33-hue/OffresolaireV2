# OffreSolaire

OffreSolaire est un comparateur de kits solaires plug‑and‑play. L’objectif est
de référencer des marchands spécialisés dans le solaire, de collecter
automatiquement leurs offres et de classer les kits selon la puissance
recommandée et le prix au kWc. Ce projet se veut transparent (affichage des
prix publics) et monétisé via des liens affiliés.

## Contenu du dépôt

* **`schema.sql`** : script SQL pour créer les tables nécessaires (`merchants`,
  `offers`, `price_history`, `subscribers`, `clicks`) dans une base de données
  PostgreSQL (par exemple via Supabase).
* **`scraper.py`** : script Python de démonstration utilisant `requests` et
  `BeautifulSoup` pour récupérer les offres sur des sites de marchands. Deux
  fonctions sont fournies à titre d’exemple pour Mater France et Mon Kit
  Solaire. Vous pouvez ajouter vos propres scrapers en suivant le même schéma.

## Utilisation

1. **Base de données** : créez un projet Supabase ou toute autre base
   PostgreSQL et exécutez `schema.sql` pour initialiser les tables.
2. **Scraping** : installez les dépendances Python (`pip install requests
   beautifulsoup4`) puis lancez le script :

   ```bash
   python scraper.py
   ```

   Les fonctions `fetch_materfrance()` et `fetch_monkitsolaire()` renvoient
   des listes d’offres. Pour chaque marchand, adaptez le sélecteur HTML aux
   pages concernées et appelez `_parse_price()` pour convertir les montants.
3. **Intégration** : insérez les résultats dans la table `offers` en
   associant les identifiants de marchands. Les prix peuvent aussi être
   historisés dans `price_history`.

## Déploiement

* **Next.js** : créez une application Next.js (TypeScript + Tailwind CSS) et
  connectez‑vous à la base Supabase via les variables d’environnement. Le
  front‑end affichera les kits classés selon la puissance et le prix.
* **Vercel** : déployez le dépôt sur Vercel et configurez un cron job
  quotidien pour exécuter le script de scraping et rafraîchir les offres.

## Contribuer

Les contributions sont les bienvenues ! Ajoutez de nouveaux marchands, des
scripts de scraping robustes ou des composants front‑end pour améliorer
l’expérience utilisateur. Assurez‑vous que les marchands sélectionnés
publient leurs prix sans formulaire de devis et offrent des produits de
qualité.