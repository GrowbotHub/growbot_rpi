import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import constants as cst
import random

vegetable = ["Salad", "Radish", "Lunar Soil 1", "Lunar Soil 2"]
shelfColor = ["plum", "bisque", "greenyellow", "cornflowerblue"]

#defaultPotState = [["black","orange","green","red","orange","green","red","orange", "black","orange","green","red","orange","green","red","orange"],["red","orange","green","red","orange","green","red","orange", "red","red","red","red","red","red","red","red"],["red","orange","green","red","orange","green","red","orange", "red","red","red","red","red","red","red","red"],["red","orange","green","red","orange","green","red","orange", "red","red","red","red","red","red","red","red"]]

potColor = ["red", "orange", "greenyellow", "green"]

def generateRandomPotColors():
	potList = []
	for shelf in range(0,4)	:
		temp = []
		for pot in range(0,16) :
			temp.append(random.choice(potColor))
		temp[0] = "black"
		temp[7] = "black"
		temp[8] = "black"
		temp[15] = "black"
		potList.append(temp)
	return potList


def makePlantStateImg(potState=None, show=False) :
	if potState == None :
		potState = generateRandomPotColors()
	imgFileName = cst._RESOURCE_FOLDER + "plantState.png"
	fig, ax = plt.subplots()

	nbrPotPerRow = 8
	nbrPotPerCol = 2

	shelfLenX = 0.40
	shelfLenY = shelfLenX/(nbrPotPerRow-1)

	constY = 0.35
	constX = 1.1 
	shelfPosY = [0.5 - shelfLenY/constY, 0.5 + shelfLenY/constY]
	shelfPosX = [0.5 - shelfLenX/constX, 0.5 + shelfLenX/constX]

	potRad = shelfLenX/(nbrPotPerRow*2)

	potX = np.linspace(-shelfLenX/2, shelfLenX/2, num=nbrPotPerRow)
	potY = np.linspace(-shelfLenY/2, shelfLenY/2, num=nbrPotPerCol)

	patches = []
	#rectPatches = []

	constX = 1.5
	constY = 2
	for isY, sY in enumerate(shelfPosY) :
		for isX, sX in enumerate(shelfPosX) :
			rect = mpatches.Rectangle([sX - shelfLenX/2 - 2*potRad, sY - shelfLenY/2 - 2*potRad], shelfLenX + 4*potRad, shelfLenY + 4*potRad, ec="black", fc=shelfColor[shelfPosY.index(sY)*2 + shelfPosX.index(sX)], fill=True, lw=3, alpha=0.4)
			ax.add_patch(rect)
			for ipY, pY in enumerate(potY) :
				for ipX, pX in enumerate(potX) :
					circle = mpatches.Circle([pX + sX, pY + sY], potRad, fill=True, ec="black", fc=potState[isY*2 + isX][ipY*nbrPotPerRow + ipX], alpha=0.9, lw=1.7)
					ax.add_patch(circle)
			rect = mpatches.Rectangle([sX - shelfLenX/2 - 2*potRad, sY - shelfLenY/2 - 2*potRad], shelfLenX + 4*potRad, shelfLenY + 4*potRad, ec="black", fc=shelfColor[shelfPosY.index(sY)*2 + shelfPosX.index(sX)], fill=False, lw=3)
			ax.add_patch(rect)
			plt.text(sX, sY + potRad*4.2, vegetable[shelfPosY.index(sY)*2 + shelfPosX.index(sX)], va="center", ha="center", family='sans-serif', size=14, color="black")

	plt.axis('equal')
	plt.axis('off')
	plt.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	return imgFileName


#makePlantStateImg(defaultPotState)