import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

vegetable = ["Salad", "Radish", "Lunar Soil 1", "Lunar Soil 2"]
shelfColor = ["plum", "bisque", "greenyellow", "cornflowerblue"]

defaultPotState = [["red","orange","green","red","orange","green","red","orange"],["red","red","red","red","red","red","red","red"],["red","red","red","red","red","red","red","red"],["red","red","red","red","red","red","red","red"]]

def makePlantStateImg(potState, show=False) :
	imgFileName = "plantState.png"
	fig, ax = plt.subplots()

	nbrPotPerRow = 4
	nbrPotPerCol = 2

	shelfLenX = 0.3
	shelfLenY = shelfLenX/(nbrPotPerRow-1)

	constY = 0.55
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


makePlantStateImg(defaultPotState)