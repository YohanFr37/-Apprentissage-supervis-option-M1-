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
	#Retire les mots 'outils' de la langue anglaise
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
	b = []
	for path in range(int(len(dictionnaire))):
		b.append((np.sum(dossier[:,path])+e)/((len(fichiers))+2*e))
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
	isSpam = [len(x)]
	print(len(x[0]))
	print(len(x))
	Pspam_x = [len(x)]
	Pham_x = [len(x)]
	for i in range(len(x)):
		spam = 1/np.sum(x[i])*Pspam*np.sum((bspam**x[i])*(1-bspam**(1-x[i])))
		ham = 1/np.sum(x[i])*Pham*np.sum((bham**x[i])*(1-bham**(1-x[i])))
		Pspam_x.append(spam)
		Pham_x.append(ham)
		isSpam.append(spam>ham)
	return isSpam[1:], Pspam_x[1:], Pham_x[1:]


def test(dossier, isSpam, Pspam, Pham, bspam, bham):
	"""
		Test le classifieur de paramètres Pspam, Pham, bspam, bham 
		sur tous les fichiers d'un dossier étiquetés 
		comme SPAM si isSpam et HAM sinon
		
		Retourne le taux d'erreur 
	"""
	fichiers = os.listdir(dossier)
	print(len(isSpam))
	print(len(Pspam))
	for i in range(len(isSpam)):
		print(i)
		print('SPAM Numéro ' + str(i) + ' P(Y=SPAM | X=x) = ' + str(Pspam[i]) + ', P(Y=HAM | X=x) = ' + str(Pham[i]))
		if(Pspam>Pham):
			print('=> identifié comme un SPAM')
		else:
			print('=> identifié comme un HAM *** erreur ***')
	#for fichier in fichiers:
		#print("Mail " + dossier+"/"+fichier)

		# à compléter...
	return 0  # à modifier...


############ programme principal ############

e = 1 # Epsilon

dossier_spams = "spam/baseapp/spam"  # à vérifier
dossier_hams = "spam/baseapp/ham"

dossier_test_spams = "spam/basetest/spam" 
dossier_test_hams = "spam/basetest/ham"

fichiersspams = os.listdir(dossier_spams)
fichiershams = os.listdir(dossier_hams)
print(len(fichiersspams))
print(len(fichiershams))
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
xbasespam = [int(len(fichiersspams)/10)]
xbaseham = [int(len(fichiershams)/10)]
xspam = [mSpam]
xham = [mHam]
print('baseapp/spam')
for i in range(int(len(fichiersspams)/10)):
	xbasespam.append(lireMail(dossier_spams+"/"+str(i)+".txt",dictionnaire))
print('baseapp/ham')
for i in range(int(len(fichiershams)/10)):
	xbaseham.append(lireMail(dossier_hams+"/"+str(i)+".txt",dictionnaire))
print('basetest/spam')
for i in range(mSpam):
	xspam.append(lireMail(dossier_test_spams+"/"+str(i)+".txt",dictionnaire))
print('basetest/ham')
for i in range(mHam):
	xham.append(lireMail(dossier_test_hams+"/"+str(i)+".txt",dictionnaire))
# Apprentissage des bspam et bham:

# Calcul des probabilités a priori Pspam et Pham:
yham = []
xspam = np.asarray(xspam[1:])
xham = np.asarray(xham[1:])
xbasespam = np.asarray(xbasespam[1:])
xbaseham = np.asarray(xbaseham[1:])
print("apprentissage de bspam...")
#print(xbasespam[1])
bspam = apprendBinomial(xbasespam, fichiersspams, dictionnaire)
#print(len(bspam))
print("apprentissage de bham...")
bham = apprendBinomial(xbaseham, fichiershams, dictionnaire)
isSpam, Pspam_x, Pham_x = prediction(xspam, Pspam, Pham, bspam, bham)
print(len(Pham_x))
print(len(isSpam))
print()
test(dossier_test_spams, isSpam, Pspam_x, Pham_x, bspam, bham)
#print(isSpam)
#print(Pspam_x)
#print(Pham_x)
isSpam, Pspam_x, Pham_x = prediction(xham, Pspam, Pham, bspam, bham)
test(dossier_test_hams, isSpam, Pspam_x, Pham_x, bspam, bham)

"""

# Calcul des erreurs avec la fonction test():
"""