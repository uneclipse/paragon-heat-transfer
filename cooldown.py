import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parameters
R = 0.014  # Radius of the inner water sphere (m)
d = 0.001  # Thickness of the steel shell (m)
outer_water_thickness = 0.0079  # Thickness of the outer water layer (m)
air_thickness = 0.05  # Thickness of the outer air layer (m)
k_w = 0.6  # Thermal conductivity of water (W/m·K)
rho_w = 1000  # Density of water (kg/m³)
c_w = 4184  # Specific heat capacity of water (J/kg·K)
k_s = 50  # Thermal conductivity of steel (W/m·K)
rho_s = 7800  # Density of steel (kg/m³)
c_s = 500  # Specific heat capacity of steel (J/kg·K)
k_air = 0.025  # Thermal conductivity of air (W/m·K)
rho_air = 1.2  # Density of air (kg/m³)
c_air = 1005  # Specific heat capacity of air (J/kg·K)
T_initial = 203  # Initial temperature of the sphere (K)
T_air = 293  # Fixed temperature of the air outside the outer water layer (K)
time_end = 2  # Total simulation time (s)
N = 400  # Number of radial points

# Time discretization
dt = 1  # Time step (s)
time_points = np.arange(0, time_end, dt)

# changer ici
time_end = 15
time_points = [0, 15]

# Discretization
r_w = np.linspace(0, R, 1400)  # Radial points in the inner water region
r_s = np.linspace(R, R + d, 100)  # Radial points in the steel region
r_air = np.linspace(R + d , R + d + air_thickness, 5000)  # Radial points in the air layer

# Combine all radial points and set up initial temperature distribution
r = np.concatenate([r_w, r_s, r_air])

# changer ici
with open('n70_temperatures_apres_etape_2.npy', 'rb') as f:
    temps_after_shot = np.load(f)

initial_temp = np.concatenate([temps_after_shot[:1500],
                                 np.full_like(r_air, T_air)])

# initial_temp = np.concatenate([np.full_like(r_w, T_initial), 
#                                  np.full_like(r_s, T_initial), 
#                                  np.full_like(r_air, T_air)])

# Thermal diffusivities
alpha_w = k_w / (rho_w * c_w)
alpha_s = k_s / (rho_s * c_s)
alpha_aw = k_w / (rho_w * c_w)
alpha_air = k_air / (rho_air * c_air)


r = np.linspace(0, R + d + air_thickness, 1400 +100 + 5000)  # Radial points in the air layer
dr = r[1] - r[0]

# Function to compute the heat equation
def heat_equation(t, T):
    dTdt = np.zeros_like(T)
    N = len(r)

    # Iterate over all radial points
    for i in range(1, N - 1):
        
        # Inner core region
        if i < 1400:
            alpha = alpha_w
        
        # Steel shell region
        elif i < 1400 + 100:
            alpha = alpha_s

        # Air region
        else:
            alpha = alpha_air
        
        r_i = r[i]
        dTdt[i] = alpha * ((T[i+1] - 2*T[i] + T[i-1]) / dr**2 + (2/r_i) * (T[i+1] - T[i]) / dr)
    
    # Boundary conditions
    dTdt[0] = 6 * alpha_w * (T[1] - T[0]) / dr**2  # Symmetry at the center
    dTdt[-1] = 0  # Fixed temperature at the outer edge (approximation)

    return dTdt

# Initial conditions
initial_conditions = initial_temp

# Solve the ODE
solution = solve_ivp(heat_equation, [0, time_end], initial_conditions, t_eval=time_points, method='BDF')

# changer ici le nom
temps = solution.y[:1500,-1]
np.save('n70_temperatures_apres_etape_3', temps)

# Plotting
plt.figure(figsize=(12, 8))

for i in range(0, len(time_points), max(1, len(time_points) // 10)):
    plt.plot(np.concatenate((r_w, r_s, r_air))*1000, solution.y[:, i]-273, label=f't={time_points[i]:.1f}s')


plt.vlines(14, -70, 90, linestyle='dashed')
plt.vlines(15, -70, 90, linestyle='dashed')
# plt.vlines(22.9, -70, 90, linestyle='dashed')
plt.xlabel('Distance to center (mm)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Distribution Over Time')
plt.legend()
plt.grid()
plt.show()
