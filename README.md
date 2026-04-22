## About This Project

These scripts use **RocketPy**, an open-source Python library for high-power rocket trajectory simulation.

RocketPy supports full 6-DOF flight simulations, including motor performance, aerodynamics, parachute descent, and realistic atmospheric conditions. It also includes built-in tools for Monte Carlo analysis, making it well-suited for landing dispersion studies. 

The documentation is well-developed and covers most use cases, including environment setup, flight simulation, and dispersion analysis:

https://docs.rocketpy.org/en/latest/

This repository provides example scripts built on top of RocketPy to run dispersion simulations, extract results, and visualize landing spread.

If you have any questions about these scripts or how to use them, please reach out:

mariacuevasabad@gmail.com
## Setup

Make sure you are using **Python 3.12 or newer**.

I recommend using Visual Studio Code as your development environment. Once installed, download the following extensions:

Python extension for Visual Studio Code https://marketplace.visualstudio.com/items?itemName=ms-python.python
Jupyter extension for Visual Studio Code https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter

This setup makes it much easier to run and debug scripts, especially if you are working with notebooks or running multiple simulations.

## Editing RocketPy Source (`flight.py`)

> **Important:** RocketPy hardcodes the simulation `max_time` to **600 seconds**. For cases such as *main-only recovery*, this is not sufficient and can truncate the trajectory before landing. This value must be increased to properly capture full descent and landing dispersion.

To modify this, edit the RocketPy source code installed on your system. The exact file path will depend on your Python installation, but the steps below show a typical workflow.

Install RocketPy from the terminal if you have not already:

```bash
pip install rocketpy
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

Instead of using a standard atmosphere model, atmospheric profiles are obtained from the University of Wyoming sounding database:  
https://weather.uwyo.edu/upperair/sounding_legacy.html

Vandenberg (station **72393**) is used because it is geographically close to the launch site, making it a reasonable approximation of local atmospheric conditions.

These soundings provide altitude-dependent profiles of:
- Temperature  
- Pressure  
- Wind speed and direction  


---

### How to Select a Sounding

1. Open the Wyoming sounding page.
2. Set:
   - **Region**: North America  
   - **Type of plot**: Text: List  
   - **Station Number**: `72393` (Vandenberg)  

3. Choose your desired:
   - **Year**
   - **Month**
   - **Day + Time** (00Z or 12Z)

4. Hit enter on your keyboard.

--

### Updating the Simulation

After generating a sounding, copy the resulting URL and update your atmospheric input in your configuration file (e.g., `rocket_params.py`).

For example:

```bash
self.atmosphere_file = "https://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2026&MONTH=04&FROM=0212&TO=0212&STNM=72672"
```
### Selecting Realistic Atmospheric Conditions (FAR Site)

To guide the date selection based on specific criteria, historical surface weather data can be used.

A useful reference is:  
https://www.wunderground.com/dashboard/pws/KCACANTI2/table/2026-03-2/2026-03-2/daily  

This corresponds to a personal weather station near the FAR launch site (Randsburg, CA), which provides historical observations such as wind speed, direction, and temperature.

Navigate to the **monthly view**, then select **table** to see daily averages (e.g., wind speeds). Based on this, choose a representative date and use it in the Wyoming sounding tool to retrieve the corresponding atmospheric profile.
