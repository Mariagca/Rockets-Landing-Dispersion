## About This Project

These scripts use **RocketPy**, an open-source Python library for high-power rocket trajectory simulation.

RocketPy supports full 6-DOF flight simulations, including motor performance, aerodynamics, parachute descent, and realistic atmospheric conditions. It also includes built-in tools for Monte Carlo analysis, making it well-suited for landing dispersion studies. :contentReference[oaicite:0]{index=0}

The documentation is well-developed and covers most use cases, including environment setup, flight simulation, and dispersion analysis:

https://docs.rocketpy.org/en/latest/

This repository provides example scripts built on top of RocketPy to run dispersion simulations, extract results, and visualize landing spread.

If you have any questions about these scripts or how to use them, please reach out:

mariacuevasabad@gmail.com

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

## Sectional Map (Los Angeles)

The landing dispersion is plotted on a sectional map of the Los Angeles area. The raster file used for visualization can be downloaded here:

https://drive.google.com/file/d/1ByOub7LoXazj-BtKquNb6xmyBYC_9d7j/view?usp=sharing

This `.tif` file is loaded using `rasterio` and cropped around the launch location. All Monte Carlo landing points are plotted in meters relative to the launch site (defined as the origin), and 1σ / 2σ dispersion ellipses are overlaid on top of the map.


## Launch Environment Configuration

The launch environment is defined using geographic location and real atmospheric data.

- Latitude: 35.34723  
- Longitude: -117.81  
- Elevation: 610 m  

An `Environment` object is created using these values.

Instead of using a standard atmosphere model, real atmospheric data is loaded from a Wyoming sounding:

- Source: University of Wyoming weather balloon (radiosonde) data  
- Station: 72393 (Vandenberg)  
- Date: May 30, 2025 at 12 UTC  

Atmospheric data link:
https://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2025&MONTH=05&FROM=3012&TO=3012&STNM=72393

Vandenberg is used because it is geographically close to the launch site, making it a reasonable approximation of local atmospheric conditions.

This dataset provides altitude-dependent profiles of temperature, pressure, and wind, which are used in the simulation instead of a standard atmosphere model.

Note: This link can be modified to use different dates, times, or stations depending on the desired conditions.
