import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import constants as cst

import numpy as np


def makeWheelImg(angle, show=False):
	center = np.array([0.5, 0.5])
	radius = 0.22
	shlefsize = np.array([0.2, 0.06])
	imgFileName= cst._RESOURCE_FOLDER + "wheel.png"
	#imgFileName = "img/wheel0.png"

	def pol2cart(rho, phi):
	    phi = phi/360.0*2*3.1415
	    x = rho * np.cos(phi)
	    y = rho * np.sin(phi)
	    return np.array([x, y])


	fig, ax = plt.subplots(figsize=[6.4,4.8], dpi=100)

	#plt.text(0.5, 0.75, "Wheel Status", va="top", ha="center", family='sans-serif', size=20, color="black")
	frame = mpatches.Rectangle([0.15,0.25], 0.01, 0.01, ec="white", fill=False, alpha=1, lw=0.2)
	ax.add_patch(frame)
	frame = mpatches.Rectangle([0.85,0.75], 0.01, 0.01, ec="white", fill=False, alpha=1, lw=0.2)
	ax.add_patch(frame)


	def drawShelf(name, color, angle, active=False):
		if active :
			edgecolor = "red"
			linewidth = 4
		else : 
			edgecolor = "black"
			linewidth = 2
		pos = center + pol2cart(radius, angle)
		shelf = mpatches.Rectangle(pos - shlefsize/2, shlefsize[0], shlefsize[1], ec=edgecolor, fc=color, alpha=1, lw=linewidth)
		plt.text(pos[0], pos[1], name, va="center", ha="center", family='sans-serif', size=14, color=edgecolor)
		ax.add_patch(shelf)

	circle = mpatches.Circle(center, radius, fill=False, ec="black", lw=2)
	ax.add_patch(circle)

	circle = mpatches.Circle(center, radius/10, fill=True, ec="black", fc="black")
	ax.add_patch(circle)

	plt.text(0.15, 0.8, "Angle :\n" + str(angle) + " [deg]", va="top", ha="left", family='sans-serif', size=14)

	def isactive(position):
		position = position%360
		if position > cst._ACTIVE_LOWER_TRESH and position < cst._ACTIVE_UPPER_TRESH :
			return True
		else :
			return False

	drawShelf("Salad", "plum", angle, isactive(angle))
	drawShelf("Lunar Soil 1", "greenyellow", angle + 90, isactive(angle + 90))
	drawShelf("Radish", "bisque", angle + 180, isactive(angle + 180))
	drawShelf("Lunar Soil 2", "cornflowerblue", angle + 270, isactive(angle + 270))



	#plt.autoscale(False, tight=False)
	plt.axis('equal')
	#plt.axis('scaled')
	plt.axis('off')
	#plt.axis('square')
	plt.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	return imgFileName


#file = open('img/lastWheel.txt', 'r')
#last = int(file.read())
#print(type(last), last)
#makeWheelImg(last, "img/wheel.png", True)
#file.close()
#file = open('img/lastWheel.txt', 'w')
#last = file.write(str(last + 1))
#file.close()
