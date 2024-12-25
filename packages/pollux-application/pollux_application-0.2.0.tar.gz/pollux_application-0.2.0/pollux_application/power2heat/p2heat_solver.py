from pollux_application.application_abstract import ApplicationAbstract
from pollux_model.power_supply.power_supply_profiles import PowerSupply
from pollux_model.power_demand.power_demand_profiles import PowerDemand
from pollux_model.heat_demand.heat_demand_profiles import HeatDemand
from pollux_model.heat_pump.heat_pump_physics_based import HeatpumpNREL
from pollux_model.splitter.splitter import Splitter
from pollux_model.solver.solver import Solver
from pollux_model.solver.step_function import StepFunction
from pollux_model.solver.key_performance_indicators import Objective, rmse

import json
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
import os


def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert ndarray to list
    elif isinstance(obj, dict):
        return {
            key: convert_ndarray_to_list(value) for key, value in obj.items()
        }  # Recurse for dicts
    elif isinstance(obj, list):
        return [convert_ndarray_to_list(item) for item in obj]  # Recurse for lists
    else:
        return obj  # Return the object if it is not ndarray, dict, or list


class Power2Heat(ApplicationAbstract):
    def __init__(self):
        super().__init__()

        # Parameters
        self.time_horizon = None
        self.step_size_control = None
        self.time_vector = []
        self.time_vector_control = []
        self.splitter1_control = []

        # Input profiles
        self.power_supply_profile = dict()
        self.power_demand_profile = dict()
        self.heat_demand_profile = dict()

        # Controls
        self.components_with_control = []
        self.control_init = []
        self.control_reshaped = []
        self.function_value = []
        self.control_scaled_value = []

        # Components
        self.power_supply = None
        self.power_demand = None
        self.heat_demand = None
        self.splitter1 = None
        self.heatpump = None

        # Solver
        self.solver = None

        # Optimisation
        self.function_value = []

        # Outputs
        self.outputs = dict()
        self.kpis = dict()

    def init_parameters(self, inputs):
        """Function to initialize the model parameters"""
        # TODO: Make it flexible so it can load multiple components
        ##########################################################################
        # Setting up time arrays for user input profiles and for the control
        ##########################################################################
        self.time_horizon = inputs["time_horizon"]  # hours (integer)
        self.step_size_control = inputs[
            "control_step"
        ]  # time_horizon/step_size_control (integer)
        if self.time_horizon % self.step_size_control != 0:
            raise ValueError(
                f"time_horizon ({self.time_horizon}) is not divisible \
                              by step_size_control ({self.step_size_control})"
            )

        # time_vector = np.linspace(0, time_horizon, 97) # stepsize=0.25 hrs
        self.time_vector = np.linspace(0, self.time_horizon, self.time_horizon + 1)[
                           :-1
                           ]  # stepsize=1 hrs
        # if using stairs instead of step for plotting:
        self.time_vector_control = np.linspace(
            0, self.time_horizon, self.time_horizon // self.step_size_control + 1
        )

        ##########################################################################
        # Defining time profiles for supply and demand
        ##########################################################################
        profiles = inputs["profiles_parameters"]

        # POWER SUPPLY
        power_supply_function = StepFunction(profiles["power_supply"], 1)
        self.power_supply = PowerSupply()
        self.power_supply.set_time_function(power_supply_function)

        # POWER DEMAND
        power_demand_function = StepFunction(profiles["power_demand"], 1)
        self.power_demand = PowerDemand()
        self.power_demand.set_time_function(power_demand_function)

        # HEAT DEMAND
        heat_demand_function = StepFunction(profiles["heat_demand"], 1)
        self.heat_demand = HeatDemand()
        self.heat_demand.set_time_function(heat_demand_function)

        ##########################################################################
        # Setting up the components
        ##########################################################################

        # SPLITTER 1 (Power splitter)
        step_function = StepFunction(profiles["splitter1"], self.step_size_control)
        self.splitter1 = Splitter()
        self.splitter1.set_time_function(step_function)
        self.control_init = self.control_init + profiles["splitter1"]

        # heat pump
        self.heatpump = HeatpumpNREL()
        param = dict()
        param["second_law_efficiency_flag"] = False
        param["print_results"] = False
        param["refrigerant_flag"] = True
        param["refrigerant"] = "R365MFC"
        self.heatpump.update_parameters(param)

        u = dict()
        heatpump_parameters = inputs["component_parameters"]["heatpump_parameters"]
        u["hot_temperature_desired"] = heatpump_parameters["hot_temperature_desired"]
        u["hot_temperature_return"] = heatpump_parameters["hot_temperature_return"]
        u["cold_temperature_available"] = heatpump_parameters[
            "cold_temperature_available"
        ]
        u["cold_deltaT"] = heatpump_parameters["cold_deltaT"]
        u["process_heat_requirement"] = "NaN"
        u["hot_mass_flowrate"] = "NaN"
        u["electricity_power_in"] = heatpump_parameters["electricity_power_in"]
        self.heatpump.input = u

        # A list to retrieve object by their names. Specific order of components is not relevant.
        components = {
            "power_supply": self.power_supply,
            "power_demand": self.power_demand,
            "splitter1": self.splitter1,
            "heatpump": self.heatpump,
            "heat_demand": self.heat_demand,
        }

        ##########################################################################
        # Setting up the system and solve
        ##########################################################################

        # List of components with control. For now: number of controls per component are equal
        self.components_with_control = ["splitter1"]

        # Solver object
        self.solver = Solver(self.time_vector, components, self.components_with_control)

        # Connect components
        self.connect_components()

    def connect_components(self):
        """Function to connect components"""
        # Connect the components.
        # Ordering is important here. For now we assume a fixed configuration.
        # The ordering can be calculated to generalise the implementation but is not done yet.
        # solver.connect(predecessor,     successor,        'predecessor_output', 'successor_input')
        self.solver.connect(
            self.power_supply, self.splitter1, "power_supply", "input"
        )
        self.solver.connect(
            self.splitter1, self.power_demand, "output_0", "power_input"
        )
        self.solver.connect(
            self.splitter1, self.heatpump, "output_1", "electricity_power_in"
        )
        self.solver.connect(
            self.heatpump, self.heat_demand, "process_heat_requirement", "heat_input"
        )

        # power supply

    def calculate(self, inputs):
        """Function to run the solver"""
        mode = inputs["mode"]

        if mode == "optimisation":
            objective_name = "kpi_rmse_demand"
        elif mode == "simulation":
            objective_name = ""

        if objective_name == "":
            # TODO: test and
            ##########################################################################
            # Run the solver, loop over time
            ##########################################################################

            self.solver.run(self.control_init)  # run the solver with the initial values

            self.control_reshaped = np.array(self.control_init).reshape(
                len(self.components_with_control), -1)
        else:
            ##########################################################################
            # Run an optimisation
            ##########################################################################

            # bounds
            scaling_factor = np.array(inputs["controls"]["ub"])
            bounds = [
                (
                    inputs["controls"]["lb"][ii] / scaling_factor[ii],
                    inputs["controls"]["ub"][ii] / scaling_factor[ii],
                )
                for ii in range(len(inputs["controls"]["init"]))
            ]
            control_init_scaled = [
                (self.control_init[ii] / scaling_factor[ii])
                for ii in range(len(self.control_init))
            ]

            # objective function
            objective = Objective(self.solver, scaling_factor)
            objective_function = getattr(objective, objective_name)
            # Note: objective function is function of scaled control

            method = inputs["optimisation"]["optimiser"]
            # method='trust-constr', 'SLSQP', 'L-BFGS-B', 'Nelder-Mead'

            function_value = []
            control_scaled_value = []
            match method:
                case "trust-constr":

                    def call_back(x, convergence):
                        function_value.append(objective_function(x))
                        control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        tol=1e-6,
                        options={
                            "maxiter": inputs["optimisation"]["maxiter"],
                            "verbose": True,
                            "disp": True,
                            "finite_diff_rel_step": inputs["optimisation"][
                                "finite_diff_step"
                            ],
                        },
                        bounds=bounds,
                        callback=call_back,
                    )

                case "L-BFGS-B":

                    def call_back(x):
                        function_value.append(objective_function(x))
                        control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        options={
                            "maxiter": inputs["optimisation"]["maxiter"],
                            "verbose": True,
                            "disp": True,
                            # absolute stepsize:
                            "eps": inputs["optimisation"]["finite_diff_step"],
                            "ftol": 1e-16,
                        },
                        bounds=bounds,
                        callback=call_back,
                    )
                case "Powell":
                    # TNC does only do one iteration, not clear why. dont use it for now!
                    # Powell has a reporting issue result.x does not reproduce reported
                    # minimal objective function value. below an attempt to repair it in
                    # the callback function. Powell seems however very efficient.
                    def call_back(x):
                        function_value.append(objective_function(x))
                        iteration = len(function_value)
                        if iteration >= 3:
                            minimum = min(function_value[:-2])
                            if function_value[-1] > minimum:
                                control_scaled_value.append(control_scaled_value[-1])
                            else:
                                control_scaled_value.append(x)
                        else:
                            control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        options={
                            "maxiter": inputs["optimisation"]["maxiter"],
                            "verbose": True,
                            "disp": True,
                            # absolute stepsize
                            "eps": inputs["optimisation"]["finite_diff_step"],
                            "return_all": True,
                            # 'maxfun': 10000,
                            # 'stpmax': 0.001
                        },
                        bounds=bounds,
                        callback=call_back,
                    )

                case "differential-evolution":

                    def call_back(x, convergence=None):
                        function_value.append(objective_function(x))
                        control_scaled_value.append(x)

                    result = differential_evolution(
                        objective_function,
                        maxiter=inputs["optimisation"]["maxiter"],
                        bounds=bounds,
                        callback=call_back,
                    )

            function_value = np.array(function_value)
            control_scaled_value = np.array(control_scaled_value)
            print(f"Objective function values: {function_value}")
            control_scaled = result.x  # optimized control
            control = np.array(
                [
                    control_scaled[ii] * scaling_factor[ii]
                    for ii in range(len(control_scaled))
                ]
            )

            number_of_components_with_control = len(self.components_with_control)
            control_reshaped = control.reshape(number_of_components_with_control, -1)
            for ii in range(number_of_components_with_control):
                print(f"control variables {self.components_with_control[ii]}")
                print(f"Optimized solution: {control_reshaped[ii]}")
            print(f"Objective function value: {result.fun}")

            # Do a run with optimized control
            self.solver.run(control)

    def get_output(self):
        ##########################################################################
        # Pass on outputs
        ##########################################################################
        output_dict = dict()

        output_dict["power_supply_outputs"] = self.solver.outputs[self.power_supply]
        output_dict["splitter1_outputs"] = self.solver.outputs[self.splitter1]
        output_dict["power_demand_outputs"] = self.solver.outputs[self.power_demand]
        output_dict["heatpump_outputs"] = self.solver.outputs[self.heatpump]
        output_dict["heat_demand_outputs"] = self.solver.outputs[self.heat_demand]

        # Power profiles [MW]
        output_dict["power_supply"] = [
            row[0] * 1e-6 for row in output_dict["power_supply_outputs"]
        ]
        output_dict["power_delivered"] = [
            row[0] * 1e-6 for row in output_dict["splitter1_outputs"]
        ]  # output_0
        output_dict["heatpump_power_input"] = [
            row[1] * 1e-6 for row in output_dict["splitter1_outputs"]
        ]  # output_1
        output_dict["power_demand"] = [
            row[0] * 1e-6 for row in output_dict["power_demand_outputs"]
        ]

        output_dict["power_difference"] = [
            (output_dict["power_demand"][ii] - output_dict["power_delivered"][ii])
            / output_dict["power_demand"][ii]
            for ii in range(len(output_dict["power_demand"]))
        ]

        # Heat profiles
        output_dict["heat_delivered"] = [
            row[5] * 1e-6 for row in output_dict["heatpump_outputs"]
        ]  # heat [MW]
        output_dict["heat_demand"] = [row[0] * 1e-6 for row in output_dict["heat_demand_outputs"]]
        output_dict["heat_difference"] = [
            (output_dict["heat_demand"][ii] - output_dict["heat_delivered"][ii])
            / output_dict["heat_demand"][ii]
            for ii in range(len(output_dict["heat_demand"]))
        ]

        ##########################################################################
        # Calculate KPIs
        ##########################################################################
        kpis_dict = dict()

        kpis_dict["kpi_rmse_power_demand"] = rmse(
            output_dict["power_demand"], output_dict["power_delivered"]
        )  # MW
        kpis_dict["kpi_rmse_heat_demand"] = rmse(
            output_dict["heat_demand"], output_dict["heat_delivered"]
        )  # [kg/hr]
        kpis_dict["kpi_rmse_demand"] = (
                kpis_dict["kpi_rmse_power_demand"] + kpis_dict["kpi_rmse_heat_demand"]
        )

        # Assign outputs and KPIs to self
        self.outputs = output_dict
        self.kpis = kpis_dict

    def save_results(
            self, project_folder, project_name, scenario_name, mode, solver_param
    ):
        output_dir = os.path.join(project_folder, project_name, "results")
        os.makedirs(output_dir, exist_ok=True)

        # Create output filenames
        output_filename = os.path.join(
            output_dir, f"{project_name}_{scenario_name}_{mode}_output.json"
        )

        outputs_dict = convert_ndarray_to_list(self.outputs)
        kpis_dict = convert_ndarray_to_list(self.kpis)
        solver_param_dict = convert_ndarray_to_list(solver_param)

        results_dict = {
            "outputs": outputs_dict,
            "kpis": kpis_dict,
            "solver_param": solver_param_dict,
        }

        with open(output_filename, "w") as output_file:
            json.dump(results_dict, output_file, indent=4)
