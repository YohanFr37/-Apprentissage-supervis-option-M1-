import numpy as np
import os
import math

def lireMail(fichier, dictionnaire):
	""" 
	Lire un fichier et retourner un vecteur de booléens en fonctions du dictionnaire
	"""
	f = open(fichier, "r",encoding="ascii", errors="surrogateescape")
	mots = f.read().split(" ")
	
	x = [False] * len(dictionnaire) 
	
	# à modifier...	
	"""
	for i in range(0,len(mots)-1):

		for j in range(0,len(dictionnaire)-1):
			if(mots[i].upper() == dictionnaire[j]):
				print(dictionnaire[j])
				x[i] = True
				a+=1
				#print(str(a) + " "+ str(i))
				#print("coucou")
				break
			#print("mots " + str(mots[i]) + " dico " + str(dictionnaire[j]))
	print(a)
	
	for i in range(0,len(mots)-1):
		if(mots[i].upper() in dictionnaire):

			x[i] = True
			b += 1
			#print(str(b) + " "+ str(i))
	"""
	for i in range(len(dictionnaire)):
		if(dictionnaire[i] in list(map(str.upper,mots))):
			x[i] = True
	f.close()
	return x

def charge_dico(fichier):
	f = open(fichier, "r")
	motstempo = f.read().split("\n")

	indiceMot = 0
	mots = []
	for i in range (len(motstempo)):
		#Si le mot fait 3 lettres ou plus, on le garde
		if(len(motstempo[i]) >= 3): 
			mots.append(motstempo[i])

	print("Chargé " + str(len(mots)) + " mots dans le dictionnaire")
	f.close()

	return mots[:-1]

def apprendBinomial(dossier, fichiers, dictionnaire):
	"""
	Fonction d'apprentissage d'une loi binomiale a partir des fichiers d'un dossier
	Retourne un vecteur b de paramètres 
		
	"""
	b = 0	# à modifier...
	return b


def prediction(x, Pspam, Pham, bspam, bham):
	"""
		Prédit si un mail représenté par un vecteur booléen x est un spam
		à partir du modèle de paramètres Pspam, Pham, bspam, bham.
		Retourne True ou False.
		
	"""
	
	return False  # à modifier...
	
def test(dossier, isSpam, Pspam, Pham, bspam, bham):
	"""
		Test le classifieur de paramètres Pspam, Pham, bspam, bham 
		sur tous les fichiers d'un dossier étiquetés 
		comme SPAM si isSpam et HAM sinon
		
		Retourne le taux d'erreur 
	"""
	fichiers = os.listdir(dossier)
	for fichier in fichiers:
		print("Mail " + dossier+"/"+fichier)		

		
		# à compléter...

	return 0  # à modifier...


############ programme principal ############

dossier_spams = "spam/baseapp/spam"	# à vérifier
dossier_hams = "spam/baseapp/ham"

fichiersspams = os.listdir(dossier_spams)
fichiershams = os.listdir(dossier_hams)

mSpam = len(fichiersspams)
mHam = len(fichiershams)

# Chargement du dictionnaire:
dictionnaire = charge_dico("spam/dictionnaire1000en.txt")
#print(dictionnaire)

# Apprentissage des bspam et bham:
print("apprentissage de bspam...")
bspam = apprendBinomial(dossier_spams, fichiersspams, dictionnaire)
print("apprentissage de bham...")
bham = apprendBinomial(dossier_hams, fichiershams, dictionnaire)

initial_count=0
# Calcul des probabilités a priori Pspam et Pham:

yspam = []
Pspam = []

for path in range(len(fichiersspams)):
	yspam.append(lireMail(dossier_spams+"/"+str(path)+".txt", dictionnaire))
	#Calcul des probas
	Pspam.append(np.sum(yspam,1)[path]/len(fichiersspams))
print(Pspam)

yham = []
Pham = []

for path in range(len(fichiershams)):
	yham.append(lireMail(dossier_hams+"/"+str(path)+".txt", dictionnaire))
	#Calcul des probas
	Pham.append(np.sum(yham,1)[path]/len(fichiershams))
print(Pham)

# Calcul des erreurs avec la fonction test():


