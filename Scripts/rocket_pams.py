  
import datetime
import pandas as pd
import numpy as np

from rocketpy import Environment, Flight, Function, MonteCarlo, Rocket, SolidMotor, Fluid, CylindricalTank, MassFlowRateBasedTank, HybridMotor, GenericMotor
from rocketpy.stochastic import (
    StochasticEnvironment,
    StochasticFlight,
    StochasticNoseCone,
    StochasticParachute,
    StochasticRailButtons,
    StochasticRocket,
    StochasticSolidMotor,
    StochasticTail,
    StochasticTrapezoidalFins)


class rocket_sim:

    def __init__(self):

        self.cd_s_main=  0.970 *np.pi*((7.315/2)**2) #used to be 18 ft 29 ft #changing to 24
        self.cd_s_drogue=  0.970 *np.pi*((1.829/2)**2) # used to be 5ft changing to 8 ft #changing to 6
        self.lat=35.34723
        self.long= -117.81
        self.elv=610
        self.env = Environment(latitude=self.lat, longitude=self.long, elevation=self.elv)
        

        self.env.set_date((2025, 5, 30, 12))
        self.atmosphere_type='wyoming_sounding'
    
        #self.atmosphere_file='https://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=06&FROM=1800&TO=1800&STNM=72393'
        
        self.atmosphere_file='https://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2025&MONTH=05&FROM=3012&TO=3012&STNM=72393'
        self.env.set_atmospheric_model(type=self.atmosphere_type,file=self.atmosphere_file)

        # --- Inputs (from OpenRocket / design) ---
        self.dry_mass = 39.7459        # dry mass [kg]
        self.rocket_length = 5.67         # rocket length [m]
        self.rocket_radius= 0.196 / 2    # rocket outer radius [m]
        self.mass_without_propellant=28.550 #kg
        self.cg_m=2.45 


        self.L= 5.45
        self.R = self.rocket_radius
       

        self.Ixx = (1/12) *  self.mass_without_propellant * self.L**2
        self.Iyy = self.Ixx
        self.Izz = (1/2) *  self.mass_without_propellant * self.R**2

        # --- Inertia calculations ---
        # Transverse (pitch / yaw)
        self.I_perp = (1/12) *  self.dry_mass * (self.rocket_length**2 + 3 * self.rocket_radius**2)

        # Axial (roll)
        self.I_axial = 0.5 * self.dry_mass * self.rocket_radius**2
   #'/Users/mariacuevas/Desktop/Rockets/Open Rocket/Q-8159_columbia-hybrid.rse',#"Q-7793.rse"
    def rocket_motor(self,path_to_motor_file):
        gen_motor = GenericMotor(
        thrust_source = path_to_motor_file,
        burn_time = 12.7,
        chamber_radius =  0.1905/2,
        chamber_height = 3.7256,
        chamber_position = 0,
        propellant_initial_mass = 42.286,
        nozzle_radius = 0.127,
        dry_mass = 39.745,
        center_of_dry_mass_position = self.rocket_length-3.22,
        dry_inertia = (self.I_perp,self.I_perp,self.I_axial),
        nozzle_position = 0,
        reshape_thrust_curve = False,
        interpolation_method = "linear",
        coordinate_system_orientation = "nozzle_to_combustion_chamber",
        )


        return gen_motor
    
    def rocket_body(self,motor,drag_off,drag_on,flight_type):
        deterministic_rocket = Rocket(
        radius=self.rocket_radius,
        mass=self.mass_without_propellant,
        inertia=(self.Ixx, self.Iyy, self.Izz),
        power_off_drag=drag_off,#"/Users/mariacuevas/Desktop/Rockets/Files/drag_off.csv",
        power_on_drag=drag_on,#"/Users/mariacuevas/Desktop/Rockets/Files/drag_on.csv",
        center_of_mass_without_motor=self.cg_m,
        coordinate_system_orientation="nose_to_tail" )

        deterministic_rocket.add_motor(motor, position=5.45)


        #adding rail_buttons 
        rail_buttons=deterministic_rocket.set_rail_buttons(
        lower_button_position=5.22,   # 1 in from tail
        upper_button_position=3.92,    # 167.976 in from tail
        angular_position=135)

        #adding nosecone 
        nose=deterministic_rocket.add_nose(
        length=0.9017,
        kind="von karman",
        position=0)
       
        #adding trapezoidal_fins 
        trapezoidal_fins=deterministic_rocket.add_trapezoidal_fins(
        n=4,
        root_chord=0.5053,
        tip_chord=0.1524,
        span=0.2286,
        sweep_length=0.4174,
        position=4.70,
        cant_angle=0.0)

        #adding tail 
        tail=deterministic_rocket.add_tail(
                top_radius=0.0979,
                bottom_radius=0.0705,
                length=0.1704,
                position=5.25 )
        

        if flight_type=="nominal":
            drogue=deterministic_rocket.add_parachute(
            name="drogue",
            cd_s=self.cd_s_drogue,
            trigger="apogee",
            lag=1)

                        # Main at 305 m (≈ 1000 ft)
            main=deterministic_rocket.add_parachute(
                name="main",
                cd_s=self.cd_s_main,
                trigger=457.2,
                lag=1)
            
            return deterministic_rocket, rail_buttons, nose,trapezoidal_fins,tail,drogue,main
        
        if flight_type=="main_only":
                        # Main at 305 m (≈ 1000 ft)
            main=deterministic_rocket.add_parachute(
                name="main",
                cd_s=self.cd_s_main,
                trigger='apogee',
                lag=1)
            
            return deterministic_rocket, rail_buttons, nose,trapezoidal_fins,tail,main
        

        if flight_type=="drogue":
            drogue=deterministic_rocket.add_parachute(
            name="drogue",
            cd_s=self.cd_s_drogue,
            trigger="apogee",
            lag=1)

            return deterministic_rocket, rail_buttons, nose,trapezoidal_fins,tail,drogue

        if flight_type=="ballistic":


            return deterministic_rocket, rail_buttons, nose,trapezoidal_fins,tail
        




            

        

            
        
        










        return deterministic_rocket
    






        





