import numpy as np
import matplotlib.pyplot as plt
import constants as cst

# Fixing random state for reproducibility
np.random.seed(19680801)

dt = 0.01
t = np.arange(0, 2, dt)
nse1 = np.random.randn(len(t))                 # white noise 1
nse2 = np.random.randn(len(t))                 # white noise 2

# Two signals with a coherent part at 10Hz and a random part
sens1 = np.sin(2 * np.pi * 10 * t) + nse1
sens2 = np.sin(2 * np.pi * 10 * t) + nse2




def makeTempPlots(airTime, airTemp, waterTime, waterTemp, show=False):
	imgFileName = cst._RESOURCE_FOLDER + "tempPlots.png"
	fig, axs = plt.subplots(2, 1)

	def plot(subpotID, time, data, dataLabel):
		#axs[subpotID].hold(True)
		#for d in data:
		#	axs[subpotID].plot(t, d)
		axs[subpotID].plot(time, data)
		axs[subpotID].set_xlabel('Time')
		axs[subpotID].set_ylabel(dataLabel)
		axs[subpotID].grid(True)

	plot(0,airTime,airTemp,"Air temp\n[degC]")
	plot(1,waterTime,waterTemp,"Water temp\n[degC]")
	fig.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	plt.close()

	return imgFileName

def makeHumPowerPlots(humidityTime, humidity, powerTime, power, show=False):
	imgFileName = cst._RESOURCE_FOLDER + "humPowerPlots.png"
	fig, axs = plt.subplots(2, 1)

	def plot(subpotID, time, data, dataLabel):
		#axs[subpotID].hold(True)
		#for d in data:
		#	axs[subpotID].plot(t, d)
		axs[subpotID].plot(time, data)
		axs[subpotID].set_xlabel('Time')
		axs[subpotID].set_ylabel(dataLabel)
		axs[subpotID].grid(True)

	plot(0,humidityTime,humidity,"Humidity\n[%]")
	plot(1,powerTime,power,"Power cons.\n[W]")
	fig.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	plt.close()

	return imgFileName



#makeTempPlots(t, (5*sens1+10, 5*sens2+10), t, (2*sens1+5, 2*sens2+5), True)
#makeHumPowerPlots(t, (50*sens1+50, 50*sens2+50), t, (sens1+200, sens2+200), True)


