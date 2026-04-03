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

For production runs, aim for ~500–1000 simulations for a stable dispersion estimate, but for testing or debugging you can reduce this (e.g., number_of_simulations=10) in the dispersion.simulate(...) call within each flight type script.

```bash


dispersion.simulate(
    number_of_simulations=20,   # total number of runs (each run samples new random values) aim for like 500-1000
.....
)
```


## Rocket Configuration (`rocket_sim` Class)

The `rocket_sim` class defines the full rocket setup used across all simulations. It centralizes vehicle properties, environment configuration, and helper functions to ensure consistency between deterministic and stochastic runs.

Got it — you want **literal README text**, not fenced blocks.

Here it is exactly how you’d write it:

---

## Notes on running the scripts

If you are using Windows, or if you are not planning to actively test and instead want to run many hundreds of Monte Carlo simulations, it is recommended to run the code as a .py script rather than a notebook (.ipynb). This makes long runs more stable and easier to manage.

This is the part of the code that runs the Monte Carlo and builds landing dispersion statistics:


```bash


dispersion.simulate(
  number_of_simulations=500,   # total number of runs (each run samples new random values)

  append=False,               # overwrite previous results (do not add to existing file)

  include_function_data=False,# do not store full time-series (saves memory, only key outputs)

  parallel=False,              # run simulations in parallel
  n_workers=10                # number of CPU workers used
)
```


 builds landing dispersion statistics

The parallel argument depends on the operating system and environment. In some setups (especially on Windows), parallel execution may not behave as expected. For this reason, in the .py version this is set to parallel=False, which runs one simulation at a time.

Because this can take a long time, it is useful to run the script in the background using screen.

Running in the background with screen:

```bash
screen -S montecarlo_run
```
Note: it is better to put the script name in quotation marks, especially if the filename contains spaces.
```bash
python "your_script.py"
```
Detach and leave it running in the background:

```bash
Ctrl + A, then D
```
At this point, the simulation continues running even if you close the terminal. You can leave the process and everything will still run and save as the script progresses.

To return to the session later (thought not necessary since the script is not actively printing anything):

```bash
screen -r montecarlo_run
```
This is especially useful for long Monte Carlo runs where you do not want to wait for all iterations to finish interactively.

Everything will be saved automatically: the .csv file containing the dispersion results (which can be used for further analysis or plotting), and the corresponding plot showing the dispersion over the FAR area for a specific flight case.
This setup is helpful if you are only interested in running the simulations and generating results; if you want to do more detailed or individual analysis (e.g., access intermediate variables, inspect trajectories, or modify parameters interactively), it is better to use the .ipynb file.


## Plotting
`plotting.ipynb` is used to visualize the landing dispersion for all three flight cases together:
Ballistic
Main Only
Nominal (Main + Drogue)
In the notebook, make sure to update the dataset paths in this section:
```bash
datasets = {
    "Main Only": ("landing_dispersion_main_only.csv", "blue"),
    "Ballistic": ("landing_dispersion_ballistic.csv", "red"),
    "Main + Drogue": ("landing_dispersion_nominal.csv", "green"),
}
```
Replace these filenames with the actual .csv files generated from your Monte Carlo runs.
Each individual simulation (per flight type) already outputs its own corresponding dispersion plot. This notebook is simply used to combine all three cases into a single plot for comparison.
