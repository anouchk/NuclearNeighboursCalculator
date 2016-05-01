# mon script
# j'importe le package qui permet de gérer les projections, pyproj
# j'importe la fonction racine carrée
# j'importe de quoi lire un fichier au format dbf (format du fichier des données carroyées de l'Insee)
import pyproj
from math import sqrt
from dbfread import DBF

# le site qui explique comment utiliser pyproj pour passer de cordonnées GPS à lambert (et vice-versa)
# http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
# j'appelle lambert la projection qui correspond à EPSG:3035
lambert=pyproj.Proj("+init=EPSG:3035")

#Essayons avec des villes que je connais
xParis, yParis = lambert(2.333333, 48.866667)
xIteville, yIteville = lambert(2.333333,48.516667)
xClermont, yClermont= lambert(3.083333, 45.783333)
xGravelines,yGravelines= lambert (2.125,50.98333)

#Donc, en utilisant le magnifique théorème de Pythagore, voyons voir les distances entre Paris et Itteville/Clermont/Gravelines
sqrt((xParis-xIteville)**2+(yParis-yIteville)**2)

sqrt((xParis-xClermont)**2+(yParis-yClermont)**2)

sqrt((xParis-xGravelines)**2+(yParis-yGravelines)**2)


##########################################
##				Objectif 1 : 			##
##	 calculer la distance entre une 	##
## 	centrale et plusieurs points x,y 	##
##########################################

# premier test
y,x = lambert(48.514297,0)

### comment stocker les distances pour le premier element de x,y
#je crée l'Array dist de longueur 1
dist=sqrt((x[0]-xGravelines)**2+(y[0]-yGravelines)**2)

# je rajoute un élément à mon Array
dist.append(sqrt((x[0]-xGravelines)**2+(y[0]-yGravelines)**2))

# on teste en mettant n'importe quoi pour x et y et on calcule les distances
x=range(10) # x = 0 1 .. 10 (pour faire les chiffres de 0 à 10)
y=range(10) # y = 0 1 .. 10
dist=[] # dist est une liste (colonne), un array
for i in range(len(x)) :
	dist.append(sqrt((x[i]-xGravelines)**2+(y[i]-yGravelines)**2))  # on rajoute des elements (les distances) a la liste


### comment printer tous les éléments des Arrays x et y (de même longueur)
for i in range(len(x)) :
	print(x[i],y[i])

### On applique : pour 2 arrays x et y, on va calculer la distance de gravelines a chaque couple x[i],y[i], la printer, et la stocker dans dist
dist=[]
length_x=len(x)
for i in range(len(x)) :
	dist_i=sqrt((x[i]-xGravelines)**2+(y[i]-yGravelines)**2)
	print(dist_i)
	dist.append(dist_i)


######################################################################
##				Objectif 2 : 										##
##	 lire le fichier DBF et ecrire toutes les longitudes-latitudes 	##
## 			carroyees dans un fichier (densitePop.csv) 				##
######################################################################
# ecrire toutes les longitudes-latitudes carroyees dans un fichier (densitePop.csv)
# (pour bien dessiner, et vérifier que le fichier de l'Insee correspond bien à la France)


# Test: comment marche enumerate : on cree une liste de lettres, puis on print les 10 premiers elements (avec leur numero)
liste = ["a","d","m","k","l","t","y","u","i","o","p","u","g","h"]
for i,lettre in enumerate(liste): # enumerate ajoute un nombre devant chaque element pour compter les elements.
	if i==10: break
 	print lettre, i
 	
 	

monfichier=open('/Users/analutzky/Desktop/data/nucleaire/densitePop.csv','w') # on cree et on ouvre le fichier '/Users/analutzky/Desktop/data/nucleaire/densitePop.csv' en mode ecriture ('w')
monfichier.write('longitude,latitude,x,y,population\n') # on ecrit l'en-tete dans monfichier : \n veut dire retour à la ligne
# on va écrire à la fois les coordonnées GPS (latitude et longitude) et lambert (x et y) pour chaque carré
for i,record in enumerate(DBF('/Users/analutzky/Desktop/data/nucleaire/ECP1KM_09_MET/R_rfl09_LAEA1000.dbf')): # i = nombre de ligne, record = contenu de la ligne, enumerate sert à rajouter pour chaque ligne son numéro (i)
#	print(record) # printer la ligne qu'on lit : i c'est le numéro de la ligne, record c'est son contenu
	if i>0:
		if i-10000*(i/10000)==0: print i # écrire i tous les 10000 lignes pour verifier que ca tourne (façon de faire un modulo se servant du fait qu'une division par un entier avec Python renvoie un entier)
		x=record['x_laea']+500 # on rajoute 500 pour être au milieu du carré d'1km, car l'Insee géolocalise le coin sud-ouest du carré
		y=record['y_laea']+500 # précision : x_laea et y_laea sont les en-têtes dans le fichier de l'Insee des coordonnées lambert
		pop=record['ind'] # ind est l'entête de la colonne du fichier de l'Insee affichant les populations
		long, lat =lambert(x,y, inverse=True) #là on fait le module pyproj à l'envers, pour passer de lambert à GPS
		monfichier.write(str(long)+','+str(lat)+','+str(x)+','+str(y)+','+str(pop)+'\n') # on ecrit i dans monfichier
#	if i==10: break #là c'est pour tester pour 10

monfichier.close() # on ferme le ficher et on arrête d'écrire dedans.




######################################################################
##				SCRIPT FINAL: 										##
##	 lire le fichier DBF, et compter le nombre d'invididus a 		##
## 				10 20 30km des centrales							##
## 																	##
######################################################################
import pyproj
from math import sqrt
from dbfread import DBF

# http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
lambert=pyproj.Proj("+init=EPSG:3035")
# coordonnées GPS des 19 centrales (source : wikipédia)
longitudes=[2.875,-0.69083,5.27083,6.21806,0.17028,4.79056,0.6528,4.75667,2.51667,7.563036,-1.88167,0.84528,2.135,3.51778,0.63528,1.21194,4.75528,1.58349,4.72249]
latitudes=[47.50972,45.25611,45.79833,49.41583,47.2306,50.09,46.45667,44.63306,47.73306,47.903108,49.53639,44.10667,51.01444,48.51528,49.85778,49.97611,45.40444,47.723982,44.335698]

popCentrales_10=[]
popCentrales_20=[]
popCentrales_30=[]

# j sera le numéro de la centrale, i le numéro du carré
for j in range(19):
	print str(longitudes[j])+ '   ' + str(latitudes[j])
	xCentrale,yCentrale= lambert(longitudes[j],latitudes[j])
	popCentrale_j_10=0
	popCentrale_j_20=0
	popCentrale_j_30=0
	for i,record in enumerate(DBF('/Users/analutzky/Desktop/data/nucleaire/ECP1KM_09_MET/R_rfl09_LAEA1000.dbf')): # i = nombre de ligne, record = contenu de la ligne
	#	print(record) # printer la ligne qu'on lit (desactivé)
		if i>0:
			if i-10000*(i/10000)==0: print i # écrire i tous les 10000 lignes pour verifier que ca tourne
			x=record['x_laea']+500
			y=record['y_laea']+500
			pop=record['ind']
			dist=sqrt((x-xCentrale)**2+(y-yCentrale)**2)
	#		print(dist)  # printer les distances (desactivé)
			if dist<10000 :
				popCentrale_j_10=popCentrale_j_10+pop
			if dist<20000 :
				popCentrale_j_20=popCentrale_j_20+pop
			if dist<30000 :
				popCentrale_j_30=popCentrale_j_30+pop
	#	if i==10: break #là c'est pour tester pour 10
	popCentrales_10.append(popCentrale_j_10)
	popCentrales_20.append(popCentrale_j_20)
	popCentrales_30.append(popCentrale_j_30)
	print popCentrales_10
	print popCentrales_20
	print popCentrales_30
	
monfichier=open('/Users/analutzky/Desktop/data/nucleaire/popCentrales.csv','w') # on ouvre le fichier '/Users/analutzky/Desktop/data/nucleaire/densitePop.csv' en mode ecriture ('w')
monfichier.write('numCentrale,latitude,longitude,population10,population20,population30\n') # on ecrit l'en-tete dans monfichier : \n veut dire retour à la ligne
for j in range(19):
	monfichier.write(str(j)+','+str(latitudes[j])+','+str(longitudes[j])+','+str(popCentrales_10[j])+','+str(popCentrales_20[j])+','+str(popCentrales_30[j])+'\n')

monfichier.close()


