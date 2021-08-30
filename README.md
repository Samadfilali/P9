# P9

# Réalisez une application mobile de recommandation de contenu

Un système de recommandation est une application destinée à proposer à un utilisateur des items susceptibles de l’intéresser en fonction de son profil. 
Dans ce projet, j'ai utilisé trois approches : 
• Content-Based Filtering (Filtrage par contenu) 
• Collaborative Filtering (Filtrage collaboratif) 
• Knowledge-based systems

En utilisant une logique severless, Le DataModel s’appuie sur 3 piliers :
•	Les Users modélisant les utilisateurs ayant consulté ou acheté via le site
•	Les Items qui correspondent aux différents produits du catalogue
•	Les Ratings qui peuvent être des notations, des visualisations de page produit, des achats concrets, …

En conclusion, aucun algorithme n’est performant dans 100% des cas et qu’il faut par conséquent envisager de les combiner. Par exemple en utilisant des algorithmes de catégorisation des utilisateurs en amont du calcul des similarités comme profilage, ou géolocalisation, ….
Il est également envisageable de rajouter des critères métiers pour favoriser différents items par rapport à d’autres, par exemple en privilégiant la mise en avant de produits récents, …
