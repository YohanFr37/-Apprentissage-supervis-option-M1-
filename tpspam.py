import numpy as np
import os
import math
import re


def lireMail(fichier, dictionnaire):
	#""" 
	#Lire un fichier et retourner un vecteur de booléens en fonctions du dictionnaire
	#"""
	f = open(fichier, "r", encoding="ascii", errors="surrogateescape")
	motsTempo = f.read().split(" ")

	mots = []
	"""
	Sépare les mots des caractères qui ne sont pas des lettres
	Exemple : "https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings" 
	devient une liste : ["https", "stackoverflow", "com", "questions", "remove", "empty", "strings", "from","a","list","of","string" 
	"""
	for i in range(len(motsTempo)): 
		#print(mots[i].encode('utf8','replace'))
		tempo = re.split('[^a-zA-Z]',motsTempo[i])
		#print(motss)
		for j in range(len(tempo)):
			mots.append(tempo[j])
		#print()
	mots = list(filter(lambda x: len(x) >=3, mots))
	#print(mots)
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
	for path in range(len(dictionnaire)):
		b.append((np.sum(dossier[:,path])+e)/((len(fichiers))+2*e))
	return np.array(b)


def prediction(x, Pspam, Pham, bspam, bham):
	"""
		Prédit si un mail représenté par un vecteur booléen x est un spam
		à partir du modèle de paramètres Pspam, Pham, bspam, bham.
		Retourne True ou False.
		
	"""
	isSpam = [len(x)]
	Pspam_x = [len(x)]
	Pham_x = [len(x)]
	for i in range(len(x)):
		spam = np.log(1/np.sum(x[i]))+np.log(Pspam)+np.sum(np.log((bspam**x[i])*((1-bspam)**(1-x[i]))))
		ham = np.log(1/np.sum(x[i]))+np.log(Pham)+np.sum(np.log((bham**x[i])*((1-bham)**(1-x[i]))))
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
	nbErreur = 0
	for i in range(len(isSpam)):
		print(i)
		if(dossier == "spam/basetest/spam"):
			print('SPAM Numéro ' + str(i) + ' P(Y=SPAM | X=x) = ' + str(Pspam[i]) + ', P(Y=HAM | X=x) = ' + str(Pham[i]))
			if(Pspam[i]>Pham[i]):
				print('=> identifié comme un SPAM')
			else:
				print('=> identifié comme un HAM *** erreur ***')
				nbErreur = nbErreur+1
		else:
			print('HAM Numéro ' + str(i) + ' P(Y=SPAM | X=x) = ' + str(Pspam[i]) + ', P(Y=HAM | X=x) = ' + str(Pham[i]))
			if(Pspam[i]<Pham[i]):
				print('=> identifié comme un HAM')
			else:
				print('=> identifié comme un SPAM *** erreur ***')
				nbErreur = nbErreur+1

	#for fichier in fichiers:
		#print("Mail " + dossier+"/"+fichier)

		# à compléter...
	return nbErreur/len(Pspam)*100


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
mSpam = 500
mHam = 500

# Chargement du dictionnaire:
dictionnaire = charge_dico("spam/dictionnaire1000en.txt")

xbasespam = [int(len(fichiersspams))]
xbaseham = [int(len(fichiershams))]
xspam = [mSpam]
xham = [mHam]

print('baseapp/spam')
for i in range(int(len(fichiersspams))):
	xbasespam.append(lireMail(dossier_spams+"/"+str(i)+".txt",dictionnaire))
print('baseapp/ham')
for i in range(int(len(fichiershams))):
	xbaseham.append(lireMail(dossier_hams+"/"+str(i)+".txt",dictionnaire))
print('basetest/spam')
for i in range(mSpam):
	xspam.append(lireMail(dossier_test_spams+"/"+str(i)+".txt",dictionnaire))
print('basetest/ham')
for i in range(mHam):
	xham.append(lireMail(dossier_test_hams+"/"+str(i)+".txt",dictionnaire))

xspam = np.asarray(xspam[1:])
xham = np.asarray(xham[1:])
xbasespam = np.asarray(xbasespam[1:])
xbaseham = np.asarray(xbaseham[1:])
# Apprentissage des bspam et bham:
print("apprentissage de bspam...")
bspam = apprendBinomial(xbasespam, fichiersspams, dictionnaire)
print("apprentissage de bham...")
bham = apprendBinomial(xbaseham, fichiershams, dictionnaire)

# Calcul des probabilités a priori Pspam et Pham:
isSpam, Pspam_x, Pham_x = prediction(xspam, Pspam, Pham, bspam, bham)

# Calcul des erreurs avec la fonction test():
erreurSpam = test(dossier_test_spams, isSpam, Pspam_x, Pham_x, bspam, bham)
isSpam, Pspam_x, Pham_x = prediction(xham, Pspam, Pham, bspam, bham)
erreurHam = test(dossier_test_hams, isSpam, Pspam_x, Pham_x, bspam, bham)
print("Pourcentage d'erreur dans les mails SPAM :" + str(erreurSpam))
print("Pourcentage d'erreur dans les mails HAM :" + str(erreurHam))
print("Pourcentage moyen d'erreur :" +str((erreurSpam+erreurHam)/2))