Editing RocketPy Source (flight.py)
Important: RocketPy hardcodes the simulation max_time to 600 seconds.
For cases such as main-only recovery, this is not sufficient and can truncate the trajectory before landing.
This value must be increased to properly capture full descent and landing dispersion.
To modify the simulation time in RocketPy, you need to edit the library files inside your conda environment.
Note: The environment name and file paths will depend on your local setup. The example below shows a typical workflow.
1. Activate environment
conda activate rocketpy312
2. Locate RocketPy installation
python -c "import rocketpy; print(rocketpy.__file__)"
Example output:
/opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/__init__.py
Although this points to __init__.py, it indicates the directory where the full RocketPy package is installed:
/opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/
3. Navigate to the package
cd /opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/
cd simulation
4. Open flight.py
open -a "Visual Studio Code" flight.py
5. Modify simulation time
Search for max_time and update it to:
max_time = 10000
6. Save and rerun
Save the file and rerun your simulation. Changes take effect immediately since the installed package is edited directly.
