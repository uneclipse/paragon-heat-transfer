# Paragon Heat Transfer Simulation


## Overview

This project aims to simulate the use of paragon extract chilling balls. It models the temperature evolution of these balls through various stages, including cooldown and heating phases. The simulation uses spherical coordinates to accurately represent the heat conduction through different materials: inner core made of water, steel shell, the outer coffee layer, and ambient air.

## Equations

The heat transfer in spherical coordinates is governed by the following equation:

$\frac{\partial T}{\partial t} = \alpha \left[ \frac{1}{r^2} \frac{\partial}{\partial r} \left( r^2 \frac{\partial T}{\partial r} \right) \right]$

where $\alpha = \frac{k}{\rho c}$ is the thermal diffusivity, $k$ is the thermal conductivity, $\rho$ is the density, and $c$ is the specific heat capacity.

### Boundary Conditions

1. **Center (Symmetry):**
   $\frac{\partial T}{\partial r} = 0 \text{ at } r = 0$
   
   Approximated by:
   
   $\frac{\partial T}{\partial t} = 6 \cdot \alpha_w \cdot \frac{T[1] - T[0]}{dr^2}$

3. **Outer Edge (Fixed Temperature):**
   $T_{\text{outer}} = 293 \text{ K}$

4. **Interface Conditions:**
   - **Water to Steel:** Ensure continuity of temperature and heat flux.
   - **Steel to Outer Water:** Ensure continuity of temperature and heat flux.


## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/uneclipse/paragon-heat-transfer.git
cd paragon-heat-transfer
```

## Usage

To generate and view plots for cooldowns and espresso shots, follow these steps:

1. **First Cooldown Phase:**

- Run the simulation with the initial temperatures (ball at -70°C or -20°C). You will need to modify these temperatures in the file 'cooldown.py'.
- To run the cooldown simulation, use
```bash
python3 cooldown.py
```

2. **Espresso Shot:**

- Use the final temperature profile from the cooldown phase as the initial temperature for the espresso shot simulation.
- Generate the plot to visualize the temperature during the espresso shot phase.
To run the espresso shot simulation, use
```bash
python3 espresso_shot_simulation.py
```

Of course, you can simulate back-to-back shots just by using previous results as intial temperatures. Simply adapt the initial conditions and follow the steps described above.

## Example

<table>
  <tr>
    <td style="text-align: center;">
      <img src="-20 degrees/temperatures_apres_etape_1.png" alt="Image 1" style="width: 40%; height: auto;"/>
      <br/>
      Temperature evolution of a -20°C steel ball from the freezer to the espresso machine.
    </td>
    <td style="text-align: center;">
      <img src="-20 degrees/temperatures_apres_etape_2.png" alt="Image 2" style="width: 40%; height: auto;"/>
      <br/>
      Temperature evolution of the system during an espresso shot.
    </td>
  </tr>
</table>


