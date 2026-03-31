## Editing RocketPy Source (`flight.py`)

> **Important:** RocketPy hardcodes the simulation `max_time` to **600 seconds**. For cases such as *main-only recovery*, this is not sufficient and can truncate the trajectory before landing. This value must be increased to properly capture full descent and landing dispersion.

To modify this, edit the RocketPy source inside your conda environment. The exact environment name and file paths will depend on your setup; the example below shows a typical workflow.

Activate your environment:
```bash
conda activate rocketpy312
```

Locate where RocketPy is installed:
```bash
python -c "import rocketpy; print(rocketpy.__file__)"
```

Example output:
```bash
/opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/__init__.py
```

This points to `__init__.py`, but indicates the full package directory:
```bash
/opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/
```

Navigate to the simulation module and open `flight.py`:
```bash
cd /opt/anaconda3/envs/rocketpy312/lib/python3.12/site-packages/rocketpy/
cd simulation
open -a "Visual Studio Code" flight.py
```

In `flight.py`, search for `max_time` and update it to:
```python
max_time = 10000
```

Save the file and rerun your simulation. Changes take effect immediately since the installed package is edited directly.
