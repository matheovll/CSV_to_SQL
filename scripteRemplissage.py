import csv
import unidecode

# MATHEO - 22/03/2023
# Create SQL table filling script from a CSV file
# By giving a CSV file with the data and the table name in the first line
# The script will create an SQL file with data insertion requests
# Exception such as comma or apostrophe are managed
# Also manage dates (DD-MM-Yyyy format) and accents (with the Unidecode bookstore) as well as the Varchar


# CSV file opening
x = 0
T=[] # Table that will contain CSV file data
with open('Jour.csv', newline='') as csv_file: # Source file || To modify ||
    reader = csv.reader(csv_file)
    for row in reader:
        if (len(row) > 1): # If the line contains more than one value
            tmp = row[0] + "," + row[1] # We concaten the two values with a comma
        else :
            tmp = row[0] # Otherwise we take the value alone
        tmp = tmp.split(";") # We separate values with a semicolon
        T.append(tmp) # We add the line to the board
        if (x == 1000000000): # For test we can put only some lines
            break
        x = x + 1 

   
'''   
# Affichage du tableau  
for i in T:
    print(i)
'''

#Creation of the skeleton of the SQL request
insertionSQL = 'INSERT INTO '
insertionSQL += str(input("Nom de la table : ")) + ' VALUES ('

# We ask for the type of data of each column to be able to adapt it in the SQL inssertion
typeValeur = []
for i in range(len(T[0])):
    typeValeur.append(str(input('\nSi type de ==> ' + T[0][i] +' :\n•VARCHAR -> 1\n•DATE -> 2\n•AUTRE -> 3\n')))

# We delete the first line of the table which contains the names of the columns
T.remove(T[0])

# We create the SQL file
fichier = open('Remplissage_Quartier.sql', 'w')# Destination file || To modify ||
for i in T:
    tmpInsertionSQL = insertionSQL # We create a copy of the SQL request
    tmp = ''
    x = 0
    for j in i: # For each line of the table
        if (',' in j):# If the value contains a point we replace it with a point
            jBis = j.replace(',','.')
        else:
            jBis = j
        if (typeValeur[x] == '1'):# If the type of value is Varchar
            if ('\'' in jBis):# If the value contains an apostrophe we replace it with two apostrophes
                jBis = jBis.replace('\'','\'\'')
            tmp +=str('\'' + unidecode.unidecode(jBis) + '\'') # We add the value to the SQL request
        elif (typeValeur[x] == '2'): # If the value type is date
            tmp += str('to_date(' + jBis + ',\'dd-mm-yyyy\')')# We add the value to the SQL request
        else:
            tmp +=str(jBis) # Otherwise we add the value to the SQL request
        if (i.index(j) != len(i) - 1):# If we are not at the last value of the line we add a comma
            tmp += ', '
        x = x + 1
    tmpInsertionSQL += tmp 
    tmpInsertionSQL += ');\n'
    fichier.write(tmpInsertionSQL) # We write the SQL request in the file by adding a return to the line
fichier.close()






