"""just for calculate"""
import sys
import os
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(parent_dir)
import aocs_lab.utils.constants as const
import aocs_lab.utils.time as time_utils


q1 = [0.652414, 0.163893,  0.728890, 0.127337]
q2 = [-0.652697, -0.161832, -0.729456, -0.125259]

r1 = R.from_quat(q1, scalar_first=True)
r2 = R.from_quat(q2, scalar_first=True)
dr = r2.inv() * r1

rotvec_norm_deg = np.linalg.norm(dr.as_rotvec(degrees=True))

print(f"{rotvec_norm_deg:.6f}")


r1 = R.from_euler('XYZ', [0,  90, -20], degrees=True)
r2 = R.from_euler('ZYX', [-90,  70, -90], degrees=True)

print(r1.as_quat(scalar_first=True))
print(r2.as_quat(scalar_first=True))

t2009 = 1230768000
t0503 = 1734841931
print(t0503 - t2009)

h = np.linspace(400e3, 1000e3, 100)
a = h + 6378e3

Omega_dot = 2*np.pi/(365.25*86400)
k = -3/2 * np.sqrt(const.GM_EARTH) * const.J2 * const.EARTH_EQUATORIAL_RADIUS**2

i = np.acos(Omega_dot/k * a**(7/2))

plt.plot((a - 6378e3)/1e3, np.rad2deg(i))
plt.title('altitude vs inclination in sun synchronous orbit')
plt.xlabel('altitude (km)')
plt.ylabel('inclination (deg)')
plt.grid()
plt.show()
