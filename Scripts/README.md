# Landing Dispersion Scripts

This folder contains scripts used to simulate rocket trajectories and compute landing dispersion using Monte Carlo methods with RocketPy.

## Overview

The workflow is:

1. Define a deterministic rocket + flight  
2. Add uncertainties (stochastic models)  
3. Run Monte Carlo simulations  
4. Extract and store results  
5. Analyze and visualize dispersion  

Separate scripts are used for each flight configuration (`nominal`, `main_only`, `drogue_only`, `ballistic`) to keep results organized and avoid confusion when comparing cases. While it is possible to run multiple flight types within a single script, this can lead to instability or crashes in RocketPy, so isolating each case into its own script ensures more reliable execution.
