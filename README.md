# OffreSolaire V2

Ce dépôt contient une application Next.js permettant de comparer des kits solaires plug & play.
L'objectif est d'afficher les offres provenant de différentes boutiques spécialisées et de les classer selon le prix et la puissance du kit.

## Contenu du dépôt

- **package.json** : liste des dépendances (Next.js, React, Supabase) et scripts de démarrage/build.
- **tsconfig.json** : configuration TypeScript pour le projet.
- **next.config.js** : configuration basique de Next.js.
- **tailwind.config.js** et **postcss.config.js** : configuration de Tailwind CSS.
- **src/pages/** : pages de l'application. `index.tsx` récupère les offres depuis Supabase et les affiche.
- **src/lib/supabase.ts** : initialisation du client Supabase en utilisant des variables d'environnement.
- **styles/** : fichiers CSS globaux avec Tailwind.
- **schema.sql** : script SQL pour créer les tables nécessaires (`merchants`, `offers`, `price_history`, `subscribers`, `clicks`).
- **scraper.py** : exemple de script Python pour récupérer des offres depuis des sites marchands.

## Utilisation

1. **Base de données** : créez un projet Supabase et exécutez `schema.sql` pour créer les tables.
2. **Variables d'environnement** :
   - Dans Vercel ou en local, créez `NEXT_PUBLIC_SUPABASE_URL` et `NEXT_PUBLIC_SUPABASE_ANON_KEY` avec les valeurs de votre projet Supabase.
3. **Installation** :
   ```bash
   npm install
   npm run dev
   ```
4. **Déploiement** :
   - Importez ce dépôt dans Vercel comme un projet Next.js (racine du dépôt).
   - Configurez les variables d'environnement.
   - Vercel exécutera `npm run build` et déploiera votre site automatiquement.

## Scraping

Le fichier `scraper.py` contient un exemple de fonctions de scraping pour deux marchands. Vous pouvez l'adapter et l'exécuter pour remplir la table `offers` de Supabase.
