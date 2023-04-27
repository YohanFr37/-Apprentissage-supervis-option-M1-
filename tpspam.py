import numpy as np
import os
import math


def lireMail(fichier, dictionnaire):
	""" 
	Lire un fichier et retourner un vecteur de booléens en fonctions du dictionnaire
	"""
	f = open(fichier, "r", encoding="ascii", errors="surrogateescape")
	mots = f.read().split(" ")

	x = [False] * len(dictionnaire)

	for i in range(len(dictionnaire)):
		if (dictionnaire[i] in list(map(str.upper, mots))):
			x[i] = True
	f.close()
	return x


def charge_dico(fichier):
	f = open(fichier, "r")
	motstempo = f.read().split("\n")
	mots = []
	for i in range(len(motstempo)):
		# Filtre les mots de moins de 3 lettres
		if (len(motstempo[i]) >= 3):
			mots.append(motstempo[i])
	motsOutil = ['YOU','YES','FOR','WHILE','ALSO','TOO','BECAUSE','THEN','YET','NEVER','THIS','THAT','THE','THESE','THUS','SINCE','THEREFORE','ACTUALLY','BUT','INDEED','FROM']
	for i in motsOutil:
		mots.remove(i)
	print("Chargé " + str(len(mots)) + " mots dans le dictionnaire")
	f.close()
	return mots[:-1]


def apprendBinomial(dossier, fichiers, dictionnaire):
	"""
	Fonction d'apprentissage d'une loi binomiale a partir des fichiers d'un dossier
	Retourne un vecteur b de paramètres 
		
	"""


	#y = []
	#b = []
	#e = 1 #Epsilon
	#for path in range(int(len(fichiers)/5)):
	#	y.append(lireMail(dossier+"/"+str(path)+".txt", dictionnaire))
	#	# Calcul des probas
	#y = np.array(y)
	#print(y)
	#for path in range(int(len(dictionnaire))):
	#	b.append((np.sum(y[:,path])+e)/((len(fichiers)/5)+2*e))
	#print(len(b))
	#b = 0  # à modifier...
	#return np.array(y),np.array(b)


	y = []
	b = []
	e = 1 #Epsilon
	for path in range(int(len(fichiers)/4)):
		y.append(lireMail(dossier+"/"+str(path)+".txt", dictionnaire))
		# Calcul des probas
	y = np.array(y)
	for path in range(int(len(dictionnaire))):
		b.append((np.sum(y[:,path])+e)/((len(fichiers)/4)+2*e))
	return np.array(b)


def prediction(x, Pspam, Pham, bspam, bham):
	"""
		Prédit si un mail représenté par un vecteur booléen x est un spam
		à partir du modèle de paramètres Pspam, Pham, bspam, bham.
		Retourne True ou False.
		
	"""
	#isSpam = [len(x)]
	#for i in range(len(x)):
		#print(x[i])
	#print(np.sum(x))
	spam = (1/np.sum(x))*Pspam*np.sum((bspam**x)*(1-bspam**(1-x)))
	ham = (1/np.sum(x))*Pham*np.sum((bham**x)*(1-bham**(1-x)))
	print(spam)
	print(ham)
	print
	#isSpam.append(spam>ham)
	#print(spam>ham)
	return spam>ham


def test(dossier, isSpam, Pspam, Pham, bspam, bham):
	"""
		Test le classifieur de paramètres Pspam, Pham, bspam, bham 
		sur tous les fichiers d'un dossier étiquetés 
		comme SPAM si isSpam et HAM sinon
		
		Retourne le taux d'erreur 
	"""
	fichiers = os.listdir(dossier)
	#for fichier in fichiers:
		#print("Mail " + dossier+"/"+fichier)

		# à compléter...
	return 0  # à modifier...


############ programme principal ############

e = 1 # Epsilon

dossier_spams = "spam/baseapp/spam"  # à vérifier
dossier_hams = "spam/baseapp/ham"

dossier_test_spams = "spam/basetest/spam/" 
dossier_test_hams = "spam/basetest/ham/"

fichiersspams = os.listdir(dossier_spams)
fichiershams = os.listdir(dossier_hams)

P = (len(fichiersspams)+len(fichiershams))
Pspam = len(fichiersspams)/P
Pham = len(fichiershams)/P

mSpam = len(fichiersspams)
mHam = len(fichiershams)
mSpam = 200
mHam = 200
# Chargement du dictionnaire:
dictionnaire = charge_dico("spam/dictionnaire1000en.txt")
# print(dictionnaire)
xspam = [mSpam]
xham = [mHam]
for i in range(mSpam):
	xspam.append(lireMail(dossier_test_spams+"/"+str(i)+".txt",dictionnaire))
	#print(xspam[i])
for i in range(mHam):
	xham.append(lireMail(dossier_test_hams+"/"+str(i)+".txt",dictionnaire))
#xspam=lireMail(dossier_test_spams,dictionnaire)
#xham=lireMail(dossier_test_hams,dictionnaire)
# Apprentissage des bspam et bham:
print("apprentissage de bspam...")
bspam = apprendBinomial(dossier_spams, fichiersspams, dictionnaire)
print("apprentissage de bham...")
bham = apprendBinomial(dossier_hams, fichiershams, dictionnaire)
# Calcul des probabilités a priori Pspam et Pham:
#Pspam = len(bspam)/(len(bspam)+len(bham))
#Pham = 1 - Pspam
yham = []

#prediction(xspam, Pspam, Pham, bspam, bham)
#prediction(xham, Pspam, Pham, bspam, bham)
xspam = np.asarray(xspam[1:])
xham = np.asarray(xham[1:])
isSpam = [mSpam]
for i in range(mSpam):
	isSpam.append(prediction(xspam[i], Pspam, Pham, bspam, bham))
isSpamB = [mHam]
for i in range(mHam):
	isSpamB.append(prediction(xham[i], Pspam, Pham, bspam, bham))
print(np.sum(isSpam))
print(np.sum(isSpamB))
#print(xspam[1])
#print(len(isSpam))
#print(prediction(xham, Pspam, Pham, bspam, bham))
#print(x)
#test(dossier_test_spams, 0, Pspam, Pham, bspam, bham)
#test(dossier_test_hams, 0, Pspam, Pham, bspam, bham)

"""

# Calcul des erreurs avec la fonction test():
"""