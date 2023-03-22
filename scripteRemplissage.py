import csv
import unidecode

# MATHEO VALLEE - 22/03/2023
# Scripte de remplissage de table SQL
# En donnant un fichier csv avec les données et le nom de la table en premiere ligne
# Le scripte va creer un fichier SQL avec les requetes d'insertion des données 
# (Fait pour Oracle et exeption gerer pour les apostrophes et les virgules dans les valeurs)
# Gere aussi les dates (format dd-mm-yyyy) et les accents (avec la librairie unidecode) 
# Ainsi que les VARCHAR


# Ouverture du fichier CSV
x = 0
T=[] # Tableau qui contiendra les données du fichier CSV
with open('Jour.csv', newline='') as csv_file: # Fichier source ||a modifier||
    reader = csv.reader(csv_file)
    for row in reader:
        if (len(row) > 1): # Si la ligne contient plus d'une valeur
            tmp = row[0] + "," + row[1] # On concatène les deux valeurs avec une virgule
        else :
            tmp = row[0] # Sinon on prend la valeur seule
        tmp = tmp.split(";") # On sépare les valeurs avec un point-virgule
        T.append(tmp) # On ajoute la ligne au tableau
        if (x == 1000000000): # Pour test on peux mettre que quelque lignes
            break
        x = x + 1 

   
'''   
# Affichage du tableau  
for i in T:
    print(i)
'''

#Creation du squellette de la requete SQL
insertionSQL = 'INSERT INTO '
insertionSQL += str(input("Nom de la table : ")) + ' VALUES ('

# On demande le type de données de chaque colonne pour pouvoir l'adapté dans l'inssertion SQL
typeValeur = []
for i in range(len(T[0])):
    typeValeur.append(str(input('\nSi type de ==> ' + T[0][i] +' :\n•VARCHAR -> 1\n•DATE -> 2\n•AUTRE -> 3\n')))

# On supprime la première ligne du tableau qui contient les noms des colonnes
T.remove(T[0])

# On crée le fichier SQL
fichier = open('Remplissage_Quartier.sql', 'w') # Fichier de destination ||a modifier||
for i in T:
    tmpInsertionSQL = insertionSQL # On crée une copie de la requete SQL
    tmp = ''
    x = 0
    for j in i: # Pour chaque ligne dde la table
        if (',' in j): # Si la valeur contient une virgule on la remplace par un point
            jBis = j.replace(',','.')
        else:
            jBis = j
        if (typeValeur[x] == '1'): # Si le type de la valeur est VARCHAR
            if ('\'' in jBis): # Si la valeur contient une apostrophe on la remplace par deux apostrophes
                jBis = jBis.replace('\'','\'\'')
            tmp +=str('\'' + unidecode.unidecode(jBis) + '\'')  # On ajoute la valeur à la requete SQL
        elif (typeValeur[x] == '2'): # Si le type de la valeur est DATE
            tmp += str('to_date(' + jBis + ',\'dd-mm-yyyy\')') # On ajoute la valeur à la requete SQL
        else:
            tmp +=str(jBis)  # Sinon on ajoute la valeur à la requete SQL
        if (i.index(j) != len(i) - 1): # Si on est pas à la dernière valeur de la ligne on ajoute une virgule
            tmp += ', '
        x = x + 1
    tmpInsertionSQL += tmp 
    tmpInsertionSQL += ');\n'
    fichier.write(tmpInsertionSQL) # On écrit la requete SQL dans le fichier en ajoutant un retour à la ligne
fichier.close()






