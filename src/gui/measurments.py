import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

dt = 0.01
t = np.arange(0, 2, dt)
nse1 = np.random.randn(len(t))                 # white noise 1
nse2 = np.random.randn(len(t))                 # white noise 2

# Two signals with a coherent part at 10Hz and a random part
sens1 = np.sin(2 * np.pi * 10 * t) + nse1
sens2 = np.sin(2 * np.pi * 10 * t) + nse2




def makeTempPlots(time, AirTemp, WaterTemp, show=False):
	imgFileName = "tempPlots.png"
	fig, axs = plt.subplots(2, 1)

	def plot(subpotID, time, data, dataLabel):
		#axs[subpotID].hold(True)
		for d in data:
			axs[subpotID].plot(t, d)
		axs[subpotID].set_xlabel('Time')
		axs[subpotID].set_ylabel(dataLabel)
		axs[subpotID].grid(True)

	plot(0,time,AirTemp,"Air temp\n[degC]")
	plot(1,time,WaterTemp,"Water temp\n[degC]")
	fig.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	return imgFileName

def makeHumPowerPlots(time, Humidity, Power, show=False):
	imgFileName = "humPowerPlots.png"
	fig, axs = plt.subplots(2, 1)

	def plot(subpotID, time, data, dataLabel):
		#axs[subpotID].hold(True)
		for d in data:
			axs[subpotID].plot(t, d)
		axs[subpotID].set_xlabel('Time')
		axs[subpotID].set_ylabel(dataLabel)
		axs[subpotID].grid(True)

	plot(0,time,Humidity,"Humidity\n[%]")
	plot(1,time,Power,"Power cons.\n[W]")
	fig.tight_layout()

	plt.savefig(imgFileName)
	if show :
		plt.show()

	return imgFileName



makeTempPlots(t, (5*sens1+10, 5*sens2+10), (2*sens1+5, 2*sens2+5), True)
makeHumPowerPlots(t, (50*sens1+50, 50*sens2+50), (sens1+200, sens2+200), True)


