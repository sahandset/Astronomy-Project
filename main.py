import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astropy.time import Time
from astroquery.jplhorizons import Horizons
from datetime import datetime
import mpld3

current_day = datetime.today()
sim_start_date = "{}-{}-{}".format(current_day.year, current_day.month, current_day.day)     # simulating a solar system starting from this date
sim_duration = 10 * 365            # Running the simulation for 10 years, can be adjusted


def scale(metric): # planets
    return metric / 10 ** 5

def scale2(metric):
    return metric / 10 ** 2 # orbits

def scale3(metric):
    return metric / 15000  # sun


class Object:                   # define the objects: the Sun, Earth, Mercury, etc
    def __init__(self, name, rad, color, r, v):
        self.name   = name
        self.r      = np.array(r, dtype = np.float)
        self.v      = np.array(v, dtype = np.float)
        self.xs     = []
        self.ys     = []
        self.plot   = ax.scatter(r[0], r[1], color = color, s = rad ** 1, edgecolors = None, zorder = 10, label = "{}".format(name))
        self.line,  = ax.plot([], [], color = color, linewidth = 1.4)

class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.planets = []
        self.time = None
        self.timestamp = ax.text(.03, .94, 'Date: ', color = 'w', transform = ax.transAxes, fontsize = 'x-large')

    def add_planet(self, planet):
        self.planets.append(planet)

    def evolve(self):           # evolve the trajectories
        dt = 1.0
        self.time += dt
        plots = []
        lines = []
        for p in self.planets:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r ** 2) ** (3. / 2)  # in units of AU/day^2
            p.v += acc * dt
            p.xs.append(p.r[0])
            p.ys.append(p.r[1])
            p.plot.set_offsets(p.r[:2])
            p.line.set_xdata(p.xs)
            p.line.set_ydata(p.ys)
            plots.append(p.plot)
            lines.append(p.line)
        self.timestamp.set_text('Date: ' + Time(self.time, format = 'jd', out_subfmt = 'date').iso)
        return plots + lines + [self.timestamp]

plt.style.use('dark_background')
fig = plt.figure(figsize = [10, 10])
ax = plt.axes([0., 0., 1., 1], xlim = (-10, 10), ylim = (-10, 10))
ax.set_aspect('equal')
ax.axis('off')
# ss = SolarSystem(Object("Sun", scale3(1.3927E6), 'yellow', [0, 0, 0], [0, 0, 0]))
ss = SolarSystem(Object("Sun", 1000, 'yellow', [0, 0, 0], [0, 0, 0]))
ss.time = Time(sim_start_date).jd
colors = ['gray', 'orange', 'blue', 'red', 'navajowhite', 'goldenrod', 'mediumaquamarine', 'steelblue', 'lightgray'] # colors of planets in order
sizes = [scale(4879.4), scale(12104), scale(12742), scale(6779), scale(139820), scale(116460), scale(50724), scale(49244), scale(2376.6)] # Diameters compared to Earth
# names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
# texty = [scale2(7.031E7), scale2(1.092E8), scale2(21.496E8), scale2(2.2739E8), scale2(7.779E8) , scale2(1.4331E9) , scale2(2.87527E9), scale2(4.50439E9), scale2(5.8942E9)] # AU distance of planets from sun

for i, nasaid in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9]):  # Going through the nine planets in the SolarSystem
    obj = Horizons(id = nasaid, location = "@sun", epochs = ss.time, id_type = 'id').vectors()
    ss.add_planet(Object(nasaid, 1000 * sizes[i], colors[i],[np.double(obj[xi]) for xi in ['x','y','z']], [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]))
    ax.legend(loc = 'upper right')


def animate(i):
    return ss.evolve()

ani = animation.FuncAnimation(fig, animate, repeat = False, frames = sim_duration, blit = True, interval = 20)

plt.show()
