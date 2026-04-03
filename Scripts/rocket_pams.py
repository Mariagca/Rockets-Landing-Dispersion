  
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

        # effective drag area (Cd * S) for the main parachute
        # Cd is taken ~0.97 (typical for round parachutes)
        # S = π (D/2)^2 → projected area using parachute diameter
        # here D = 7.315 m (~24 ft), previously different sizes were tested
        self.cd_s_main = 0.970 * np.pi * ((7.315/2)**2)

        # effective drag area (Cd * S) for the drogue parachute
        # same equation: Cd * π (D/2)^2
        # here D = 1.829 m (~6 ft), previously changed from other values
        self.cd_s_drogue = 0.970 * np.pi * ((1.829/2)**2)

        # launch site latitude (degrees)
        self.lat = 35.34723

        # launch site longitude (degrees)
        self.long = -117.81

        # launch site elevation above sea level (meters)
        self.elv = 610

        # environment object defining atmospheric conditions at launch site
        # used for wind profiles, air density, pressure, etc.
        self.env = Environment(latitude=self.lat, longitude=self.long, elevation=self.elv)
                

        # sets the date and time used for the atmospheric model (year, month, day, hour UTC)
        # this determines which sounding / weather profile is pulled but not relevant for wyoming_sounding profile
        self.env.set_date((2025, 5, 30, 12))

        # specifies the type of atmospheric data source being used
        # "wyoming_sounding" → uses radiosonde (weather balloon) data from University of Wyoming
        self.atmosphere_type = 'wyoming_sounding'

        # URL to the sounding data
        # STNM=72393 → station ID (Edwards AFB, commonly used near FAR site)
        # FROM=3012 → day 30 at 12 UTC
        # this provides vertical profiles of wind, temperature, pressure, etc.
        self.atmosphere_file = 'https://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=2025&MONTH=05&FROM=3012&TO=3012&STNM=72393'

        # applies the atmospheric model to the environment
        # combines the selected type and the specific sounding file
        # this is what the simulation uses for wind profiles and air properties vs altitude
        self.env.set_atmospheric_model(
            type=self.atmosphere_type,
            file=self.atmosphere_file
        )
        # --- Inputs (from OpenRocket / design) ---

        # total mass of the rocket without propellant (structure, avionics, recovery, etc.)
        self.dry_mass = 39.7459        # [kg]

        # total length of the rocket from nose to tail
        self.rocket_length = 5.67      # [m]

        # outer radius of the rocket body
        # given diameter = 0.196 m → radius = D/2
        self.rocket_radius = 0.196 / 2   # [m]

        # mass used for simulation when propellant is not included (used in some configs)
        # slightly different from dry_mass depending on modeling assumptions
        self.mass_without_propellant = 28.550   # [kg]

        # center of gravity location along the rocket (from nose tip)
        # important for stability and moment calculations
        self.cg_m = 2.45   # [m] 


        # simplified geometry used for inertia approximation
        # L → characteristic length (slightly different from full rocket length depending on model)
        self.L = 5.45

        # R → rocket radius (same as defined above)
        self.R = self.rocket_radius


        # inertia assuming simplified cylindrical body (no propellant)
        # Ixx, Iyy → rotation about axes perpendicular to length (pitch / yaw)
        # (1/12) m L^2 comes from slender rod / cylinder approximation
        self.Ixx = (1/12) * self.mass_without_propellant * self.L**2
        self.Iyy = self.Ixx

        # Izz → rotation about longitudinal axis (roll)
        # (1/2) m R^2 → standard solid cylinder formula
        self.Izz = (1/2) * self.mass_without_propellant * self.R**2


        # --- Inertia calculations (full rocket approximation) ---

        # transverse inertia (pitch / yaw)
        # includes both length and radius contribution → more complete rigid body approximation
        # (1/12) m (L^2 + 3R^2)
        self.I_perp = (1/12) * self.dry_mass * (self.rocket_length**2 + 3 * self.rocket_radius**2)

        # axial inertia (roll)
        # same idea: rotation around central axis
        # (1/2) m R^2
        self.I_axial = 0.5 * self.dry_mass * self.rocket_radius**2
   #'/Users/mariacuevas/Desktop/Rockets/Open Rocket/Q-8159_columbia-hybrid.rse',#"Q-7793.rse"
    def rocket_motor(self, path_to_motor_file):

    # defines a generic motor using a thrust curve file
    # this is not a full hybrid model → treated as a simplified motor with fixed properties
        gen_motor = GenericMotor(

        # thrust curve input (time vs thrust)
        thrust_source=path_to_motor_file,

        # total burn duration from thrust curve
        burn_time=12.7,

        # combustion chamber geometry
        chamber_radius=0.1905/2,   # [m]
        chamber_height=3.7256,     # [m]

        # reference position for chamber (along rocket axis)
        chamber_position=0,

        # total propellant mass used in the simulation
        # since this is a GenericMotor (not a full hybrid model),
        # the propellant mass is approximated as a single value
        # this value was taken as the sum of two components (fuel + oxidizer)
        propellant_initial_mass = 42.286,

        # nozzle geometry
        nozzle_radius=0.127,   # [m]

        # dry mass of the motor (structure without propellant)
        dry_mass=39.745,

        # location of motor dry mass center along rocket
        center_of_dry_mass_position=self.rocket_length - 3.22,

        # inertia of motor (using rocket-level approximations)
        dry_inertia=(self.I_perp, self.I_perp, self.I_axial),

        # nozzle position reference
        nozzle_position=0,

        # keeps thrust curve as-is (no reshaping)
        reshape_thrust_curve=False,

        # linear interpolation between thrust data points
        interpolation_method="linear",

        # coordinate system definition (important for sign conventions)
        coordinate_system_orientation="nozzle_to_combustion_chamber",
        )

        return gen_motor
    
    def rocket_body(self, motor, drag_off, drag_on, flight_type):

        # defines the rocket body using geometry + mass properties
        deterministic_rocket = Rocket(
            radius=self.rocket_radius,                 # outer radius of rocket
            mass=self.mass_without_propellant,         # mass excluding propellant (used for this configuration)
            inertia=(self.Ixx, self.Iyy, self.Izz),    # inertia tensor (simplified body approximation)

            # aerodynamic drag curves
            # power_off → no thrust (coasting / descent)
            # power_on → during motor burn
            power_off_drag=drag_off,
            power_on_drag=drag_on,

            # center of mass location without motor
            center_of_mass_without_motor=self.cg_m,

            # coordinate system runs from nose → tail
            coordinate_system_orientation="nose_to_tail"
        )

        # attaches motor to the rocket at specified position (from nose)
        deterministic_rocket.add_motor(motor, position=5.45)


        # --- Rail buttons ---
        # defines launch rail attachment points
        rail_buttons = deterministic_rocket.set_rail_buttons(
            lower_button_position=5.22,   # near tail
            upper_button_position=3.92,   # further up body
            angular_position=135          # orientation around body
        )


        # --- Nose cone ---
        # von Kármán profile → minimizes drag
        nose = deterministic_rocket.add_nose(
            length=0.9017,
            kind="von karman",
            position=0                   # starts at nose tip
        )


        # --- Fins ---
        # trapezoidal fin geometry (stability + control of CP)
        trapezoidal_fins = deterministic_rocket.add_trapezoidal_fins(
            n=4,                         # number of fins
            root_chord=0.5053,
            tip_chord=0.1524,
            span=0.2286,
            sweep_length=0.4174,
            position=4.70,               # location along body
            cant_angle=0.0               # no spin induced
        )


        # --- Tail section ---
        # transition at aft section (affects drag + flow)
        tail = deterministic_rocket.add_tail(
            top_radius=0.0979,
            bottom_radius=0.0705,
            length=0.1704,
            position=5.25
        )


        # ============================================
        # Flight configurations (recovery logic)
        # ============================================

        if flight_type == "nominal":

            # drogue deploys at apogee (stabilizes descent)
            drogue = deterministic_rocket.add_parachute(
                name="drogue",
                cd_s=self.cd_s_drogue,
                trigger="apogee",
                lag=1
            )

            # main deploys at fixed altitude (~457 m ≈ 1500 ft)
            main = deterministic_rocket.add_parachute(
                name="main",
                cd_s=self.cd_s_main,
                trigger=457.2,
                lag=1
            )

            return deterministic_rocket, rail_buttons, nose, trapezoidal_fins, tail, drogue, main


        if flight_type == "main_only":

            # main deployed at apogee (no drogue case)
            main = deterministic_rocket.add_parachute(
                name="main",
                cd_s=self.cd_s_main,
                trigger='apogee',
                lag=1
            )

            return deterministic_rocket, rail_buttons, nose, trapezoidal_fins, tail, main


        if flight_type == "drogue":

            # drogue only → no main deployment
            drogue = deterministic_rocket.add_parachute(
                name="drogue",
                cd_s=self.cd_s_drogue,
                trigger="apogee",
                lag=1
            )

            return deterministic_rocket, rail_buttons, nose, trapezoidal_fins, tail, drogue


        if flight_type == "ballistic":

            # no parachutes → purely ballistic descent
            return deterministic_rocket, rail_buttons, nose, trapezoidal_fins, tail


        return deterministic_rocket


            





