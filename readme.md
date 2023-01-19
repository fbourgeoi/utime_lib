# utime_lib
## Instancier la classe
```python
import utime_lib
utime = utime_lib.utime_web('user','passwd')
```

## Se logger sur le site
```python
utime.login()
```
A noter que si le paramètre autologin est à True dans les autres fonctions, il n'y a pas besoin d'appeler cette fonction

## Pointer
```python
utime.pointer(autologin=True)
```
Un seul appel à cette fonction suffit pour enregistrer un pointage
Autologin permet de ne pas devoir appeler la fonction login()


## Récupérer les pointages
```python
utime.récupérer_pointages(fromdate, todate, autologin=True)
```
Autologin permet de ne pas devoir appeler la fonction login()
fromdate et todate sont les dates de début et de fin de récupération est pointages (inclues)
Elles doivent:
- Etre dans la même année
- Etre au format datetime.date

Si la lecture échoue, la fonction renvoie None
Si la lecture réussi, la fonction renvoie une liste de liste.
Chaque élément représente un jour et contient:
- La date
- L'heure de début de pointage
- L'heure de fin de pointage
- Un booléen qui indique une erreur éventuelle (différence entre le delta des pointages et le temps de prestation indiqué, c'est qu'il y a eu plusieurs pointages dans la journée, ce qui n'est pas inclus dans le rapport utilisé pour récupérer les pointages)

## Récupérer les effectifs
```python
utime.utime.récupérer_effectifs(autologin=True)
```
Autologin permet de ne pas devoir appeler la fonction login()
La fonction renvoie un dictionnaire avec comme clés les services et comme valeur la liste des personnes de ce service


# Tests
Un fichier de test 'test.py' peut être créé à la racine, il  est déjà inclu dans le fichier .gitignore pour éviter de publier un mot de passe