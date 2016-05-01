######################################################################
##				Démarche :  										##
##	 Idem que pour le fichier Insee mais au niveau européen         ##
## 	calculer la	population à 10 20 30 100km des centrales			##
## 																	##
######################################################################

# 2 differences avec les données france uniquement :
# - cette fois, les cordonnées des carres sont stockées dans un shapefile, qu'on va lire avec le module fiona. 
# chaque carre est identifie par un "grid ID", et un fichier pop contient l'info sur les populations de chaque pays dans chaque grille "grid ID"
# - il y a deux fichiers populations: les populations de certains pays ont été stockées a part (dont le Luxembourg... grrr)


from operator import itemgetter  # pour trier un tableau a plusieurs colonnes
from math import sqrt
import fiona  # pour lire les shapefile
import dbfread # finalement on ne va pas s'en servir
import pyproj

# écrire toutes les longitudes-latitudes carroyees dans un fichier (pour bien dessiner)
monfichier=open('/Users/analutzky/Desktop/data/nucleaire/densitePop.csv','w') # on ouvre le fichier '/Users/analutzky/Desktop/data/nucleaire/densitePop.csv' en mode ecriture ('w')
monfichier.write('longitude,latitude,x,y,population\n') # on ecrit l'en-tete dans monfichier : \n veut dire retour à la ligne
for i,record in enumerate(DBF('/Users/analutzky/Desktop/data/nucleaire/ECP1KM_09_MET/R_rfl09_LAEA1000.dbf')): # i = nombre de ligne, record = contenu de la ligne, enumerate sert à rajouter pour chaque ligne son numéro (i)
#	print(record) # printer la ligne qu'on lit (desactivé)

# DBF c'est la fonction, c'est comme open (code qui n'a finalement pas servi, c'est juste pour lire la ligne d'un DBF)
# mon_dbf_euro=DBF('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTATReferenceGrid/Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.dbf')
# comment lire un ligne (la 1ère ligne pas déjà lue : si je le fais une 2e fois j'aurai la 2e)
# ligne_1=mon_dbf_euro.load()

#for i,record in enumerate(mon_dbf_euro): # i = nombre de ligne, record = contenu de la ligne, enumerate sert à rajouter pour chaque ligne son numéro (i)
#	print(record) # printer la ligne qu'on lit (desactivé)
#	if i >2 : break
# on se rend compte que le format du dbf est pas le même (et zut !)

######################################################################
##				     Objectif 1: 									##
##	                  exploration des données                		##
## 				      pop et shape               					##
## 																	##
######################################################################

# avant de faire le code final, on explore les données :

popFile=open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTAT_grid_POP_1K_2011_V2_0_1.csv','r')
noms=popFile.readline() # lire une ligne
noms=noms.strip() # enleve les caracteres de retour a la ligne (\n et \r) a la fin de la ligne
noms=noms.split(',') # coupe selon le caractere demandé ici une virgule
print(noms)
popFile.close()

shapeFile=fiona.open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTATReferenceGrid/Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.shp', 'r')
for i,pt in enumerate(shapeFile):
	print(pt) # printer la ligne qu'on lit et là on se rend compte que c'est le bordel. Il faut récupérer les coordonnées du 1er coin du carré et l'identifiant
	x_laea=pt['geometry']['coordinates'][0][0][0]
	y_laea=pt['geometry']['coordinates'][0][0][1]
	id=str(pt['properties']['GRD_ID']) # en jetant un oeil à 'properties' on se rend compte que c'est un dictionnaire Orderdict
	if i >2 : break
# 

######################################################################
##				         Objectif 2: 								##
##	               mettre pop dans des vecteurs	                	##
## 				puis le trier selon la colonne grid					##
## 																	##
######################################################################
# on lit le fichier pop et on extrait la population et l'identifiant de grille de chaque carre
popFile=open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTAT_grid_POP_1K_2011_V2_0_1.csv','r')
pop=[]
grid=[]
for i, line in enumerate(popFile):
	if i>0 :
		lignecsv=line.strip().split(',') # commande-type pour lire une ligne d'un fichier csv et la mettre dans un tableau
		pop.append(int(lignecsv[0]))  # on mets le premier élement du tableau (pop) dans pop
		grid.append(lignecsv[1]) # on mets le 2e élement du tableau (grid Id) dans grid

popFile.close()

# à la recherche du Luxembourg perdu (on se demandait s'il était dans le fichier, la population étant trop faible autour de Cattenom)
# on va faire la liste des identifiants de pays qui sont present dans popFile
# les données étaient triées par pays : dès que je vois un nouveau nom de pays, je le stocke
popFile=open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTAT_grid_POP_1K_2011_V2_0_1.csv','r')
cntry=['test'] #cntry c'est le nom du pays
j=0 #j c'est le nombre de pays
for i, line in enumerate(popFile):
	if i>0 :
		lignecsv=line.strip().split(',') # commande-type pour lire une ligne d'un fichier csv et la mettre dans un tableau
		if lignecsv[2]!=cntry[j] :   # si on trouve un nouveau pays
			cntry.append(lignecsv[2])  # on mets le 3e élement du tableau (country) dans cntry
			j=j+1

popFile.close()
# on a vu qu'il manquait effectivement le Luxembourg

# on lit le 2eme fichier pop et on extrait la population et l'identifiant de grille de chaque carre
popFile=open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/JRC-GHSL_AIT-grid-POP_1K_2011.csv','r')
for i, line in enumerate(popFile):
	if i>0 :
		lignecsv=line.strip().split(',')
		pop.append(int(lignecsv[0]))  # on mets le premier élement du tableau (pop) dans pop 
		grid.append(lignecsv[1]) # on mets le 2e élement du tableau (grid Id) dans grid
		# on n'a pas redéfini pop et grid parce qu'on les rajoute au même vecteur

popFile.close()

# on trie pop selon l'identifiant grid pour pouvoir merger ensuite avec la géolocalisation du carré
combined=[(pop[i],grid[i]) for i in range(len(pop))] # on crée une liste qui contient tous les couples (pop, grid) : on combine grid et pop
combined.sort(key=itemgetter(1))  # on trie la combinaison, par son 2e element (grid)
sorted_pop=[x for (x,y) in combined]  # on extrait pop de la combinaison triée
sorted_gridpop=[y for (x,y) in combined] # on extrait grid de la combinaison triée

[sorted_pop[i] for i in range(10)]
[sorted_gridpop[i] for i in range(10)] # on a bien trié par grid

######################################################################
##				         Objectif 3: 								##
##	               mettre shape dans des vecteurs	             	##
## 				puis le trier selon la colonne grid					##
## 																	##
######################################################################
# on stocke le contenu du fichier shape dans 3 vecteurs
x_laea=[]
y_laea=[]
grid_shape=[]
shapeFile=fiona.open('/Users/analutzky/Desktop/data/nucleaire/geostat_donnees_carroyees/GEOSTATReferenceGrid/Grid_ETRS89_LAEA_1K-ref_GEOSTAT_POP_2011_V2_0_1.shp', 'r')
for i,pt in enumerate(shapeFile):
# 	print(pt) # printer la ligne qu'on lit (desactivé)
 	x_laea.append(pt['geometry']['coordinates'][0][0][0])
 	y_laea.append(pt['geometry']['coordinates'][0][0][1])
	grid_shape.append(str(pt['properties']['GRD_ID']))

shapeFile.close()

# on trie shape selon l'identifiant grid pour pouvoir merger ensuite avec la pop
combined=[(x_laea[i],y_laea[i],grid_shape[i]) for i in range(len(grid_shape))] # on combine 
combined.sort(key=itemgetter(2))  # on trie la combinaison, par son 3e element (grid_shape)
sorted_xshape=[x for (x,y,z) in combined]  # on extrait x de la combinaison triée
sorted_yshape=[y for (x,y,z) in combined]  # on extrait y de la combinaison triée
sorted_gridshape=[z for (x,y,z) in combined] # on extrait grid_shape de la combinaison triée

######################################################################
##				Objectif 4 : 										##
##	 			compter le nombre d'invididus à						##
## 				10 20 30km et 100km des centrales					##
## 																	##
######################################################################

lambert=pyproj.Proj("+init=EPSG:3035")
# compter les habitants autour des centrales
longitudes=[2.875,-0.69083,5.27083,6.21806,0.17028,4.79056,0.6528,4.75667,2.51667,7.563036,-1.88167,0.84528,2.135,3.51778,0.63528,1.21194,4.75528,1.58349,4.72249]
latitudes=[47.50972,45.25611,45.79833,49.41583,47.2306,50.09,46.45667,44.63306,47.73306,47.903108,49.53639,44.10667,51.01444,48.51528,49.85778,49.97611,45.40444,47.723982,44.335698]

# conversion des coordonnées GPS des 19 centrales en Lambert
xCentrales=[]
yCentrales=[]
for j in range(19):
	print str(longitudes[j])+ '   ' + str(latitudes[j])
	xCentrale,yCentrale= lambert(longitudes[j],latitudes[j])
	xCentrales.append(xCentrale)
	yCentrales.append(yCentrale)
		
# initialiser le vecteur popCentrale avec 19 éléments "0"
popCentrale_10=[]
popCentrale_20=[]
popCentrale_30=[]
popCentrale_100=[]
for j in range(19):
	popCentrale_10.append(0)
	popCentrale_20.append(0)
	popCentrale_30.append(0)
	popCentrale_100.append(0)

# tiens, y'a moins de shape que de pop... => chasse aux doublons, car pour un même carré il peut y avoir plusieurs pays
numPop=0
for numShape in range(len(sorted_gridshape)):
	popCarre=sorted_pop[numPop]
	xCarre=sorted_xshape[numShape]+500
	yCarre=sorted_yshape[numShape]+500	
	# tant que le grid ID de numPop est le même que celui de numShape, on ajoute la pop à la pop du carré
	while(numPop<len(sorted_gridpop) and sorted_gridpop[numPop+1]==sorted_gridshape[numShape]):
 		numPop=numPop+1	
 		popCarre=popCarre+sorted_pop[numPop]				
	numPop=numPop+1	
	if numShape-10000*(numShape/10000)==0: print numShape # écrire numShape tous les 10000 carrés pour verifier que ca tourne
	# on s'arrête de calculer quand on arrive trop à l'Est du fichier d'Eurostat 
	if xCarre < 4250000 :	
		for j in range(19):
			dist=sqrt((xCarre-xCentrales[j])**2+(yCarre-yCentrales[j])**2)
	#		print(dist)  # printer les distances (desactivé)
			if dist<=10000 :
				popCentrale_10[j]=popCentrale_10[j]+popCarre	
			if dist<=20000 :
				popCentrale_20[j]=popCentrale_20[j]+popCarre
			if dist<=30000 :
				popCentrale_30[j]=popCentrale_30[j]+popCarre
			if dist<=100000 :
				popCentrale_100[j]=popCentrale_100[j]+popCarre

# on printe les résultats à 20 km pour comparer avec Mentrek et voir si c'est cohérent avec les siens
mypops=popCentrale_20		
sorted(popCentrale_20)
[sorted(popCentrale_20)[i]-mypops[i] for i in range(19)]

# http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/

nomsCentrales=['Belleville','Blayais','Bugey','Cattenom','Chinon-B','Chooz-B','Civaux','Cruas','Dampierre','Fessenheim','Flamanville','Golfech','Gravelines','Nogent','Paluel','Penly','Saint-Alban','St. Laurent','Tricastin']

monfichier=open('/Users/analutzky/Desktop/data/nucleaire/popCentrales_euro.csv','w') # on ouvre le fichier '/Users/analutzky/Desktop/data/nucleaire/densitePop.csv' en mode ecriture ('w')
monfichier.write('numCentrale,nomsCentrale,latitude,longitude,population10,population20,population30,population100\n') # on ecrit l'en-tete dans monfichier : \n veut dire retour à la ligne
for j in range(19):
	monfichier.write(str(j)+','+str(nomsCentrales[j])+','+str(latitudes[j])+','+str(longitudes[j])+','+str(popCentrale_10[j])+','+str(popCentrale_20[j])+','+str(popCentrale_30[j])+','+str(popCentrale_100[j])+'\n')

monfichier.close()
