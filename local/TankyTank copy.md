# Projet Développement logiciel : TANKY TANK

## Présentation :

Ce projet consiste à créer un jeu de Tank sur PC où 2 joueur jouent en 1 VS 1 sur un même PC.

## Fonctionnalités :
**Le programme comporte 4 écrans :**
 - Un **écran d'accueil** avec 3 boutons pour accéder à l'écran du jeu et l'écran du tableau de scores.
 - Un **écran avec le tableau des meilleurs scores**, avec possibilité de retour vers menu principal.
 - Un **écran de jeu** qui permet à l'utilisateur de se connecter au réseau, le jeu se lance lorsqu’un autre joueur est connecté sur le réseau, avec possibilité de retour vers menu principal.
 - Un **écran d'instructions** avec possibilité de retour vers menu principal.

**Modèle de données **
Les deux joueurs possèdent :
 - une différentiation joueur1/joueur2 (J1/J2, couleurs des tanks)
 - une vitesse de déplacement
 - des points de vie
 - une puissance de tir
 - une vitesse de tir 
 - un délai de tir 

**Des scores composés de :**
 - le score du joueur 1
 - le score du joueur 2
 - le temps enregistré à la fin du jeu

**Contrôleurs :**
Clavier -> boutons :
Joueur 1 : UP,DOWN,RIGHT,LEFT,SPACE
Joueur 2 : Z(up),Q(left),S(down),D(right),A(shoot)

**Déroulement d’une partie :**  
 - les deux joueurs apparaissent de part et d’autre de l’écran.
 - l’espace de jeu se limite à l’écran, pas de physique, la vue caméra est dite “top-down”.
 - le tank est capable de pivoter à 90° et d'avancer en haut, bas, gauche, droite.
 - un des boutons permet au joueur de tirer un projectile. 
 - un Joueur perd un point de vie quand un projectile le touche.


**Fin de partie :**
 - la partie se termine quand un joueur n’a plus de points de vie.
 - le logiciel bascule alors sur l’écran de fin de partie, où le score du gagnant s’affiche ainsi que sa position dans les meilleurs scores et le timer.
