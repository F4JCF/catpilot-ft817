# CAT Pilot FT-817 — consignes de maintenance

- Logiciel distinct de CAT Pilot (FT-991A, dépôt F4JCF/catpilot) : ne jamais modifier l'autre dépôt depuis ici.
- L'utilisateur n'installe pas Python : toute livraison passe par GitHub Actions (exécutables Windows et Linux,
  publication automatique quand `catpilot/__init__.py` change de version).
- À CHAQUE modification visible par l'utilisateur :
  1. augmenter la version dans `catpilot/__init__.py` ;
  2. écrire les nouveautés dans `NOTES.md` (notes de la publication GitHub) ;
  3. ajouter une entrée en tête de `assets/nouveautes.html` (historique affiché dans le mode d'emploi) ;
  4. mettre à jour `assets/manuel.html` (mode d'emploi intégré, menu Aide > Mode d'emploi, F1)
     et `README.md` si la fonction y est décrite.
- Textes de l'interface et du manuel en français ; les traductions anglaises sont dans `catpilot/i18n_en.py`.
