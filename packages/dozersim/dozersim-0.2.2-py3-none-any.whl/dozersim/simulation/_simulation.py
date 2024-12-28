from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Callable, Any, TYPE_CHECKING

import itertools
# from trust_constr import minimize, NonlinearConstraint, LinearConstraint, Bounds
import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import NonlinearConstraint, minimize, Bounds

if TYPE_CHECKING:
    from dozersim.modelling import Model
    from dozersim.path import Path
    from dozersim.parameters import Parameter, SettingsParameter
    from dozersim.objectives import Objective
from dozersim.results import Result, Analysis, ParameterValue



def get_non_iterable(parameters: dict[Parameter, Any]):
    iterable_pars = []
    for parameter in parameters.keys():
        try:
            iter(parameter)
        except TypeError:
            iterable_pars.append(parameter)

    return tuple(iterable_pars)


def get_iterable(parameters: dict[Parameter, Any]):
    iterable_pars = []
    for parameter in parameters.keys():
        try:
            iter(parameter)
            iterable_pars.append(parameter)
        except TypeError:
            pass

    return tuple(iterable_pars)


class Simulation:
    """ 
    Simulation object with all the basic function to solve a items tree for a set of load cases

        Methods
        -------------
        add_parameter: add a parameter to use in the optimization
        add_objective: add an objective function

    """

    def __init__(self, paths: list[Path] = None):
        self.paths = paths
        self._model_steps: list[Step] = []
        self._load_steps: dict[str, list[Step]] = {}
        self._analysis: Analysis = Analysis()
        self._parameters: dict[Parameter, Any] = {}
        self._objectives: list[Objective] = []
        self._has_run: bool = False

    def add_model_steps(self, steps: Step | list[Step]):
        if type(steps) is not list: steps = [steps]
        for step in steps:
            self._model_steps.append(step)

    def add_load_steps(self, steps: Step | list[Step], name: str):
        if type(steps) is not list: steps = [steps]
        try:
            # if load case exists
            self._load_steps[name].extend(steps)
        except KeyError:
            # if load case dit not exists add new load case
            self._load_steps.update({name: steps})

    def add_parameter(self, *parameters: Parameter):
        """ Add a parameter to the latest step """
        for parameter in parameters:
            self._parameters[parameter] = None

    def add_objective(self, *objectives: Objective):
        for objective in objectives:
            self._objectives.append(objective)

    def get_analysis(self):
        return self._analysis

    def reset(self):
        """
        Reset simulation. All parameters, objectives, analysis will be removed.

        """
        #
        self._parameters = dict()
        self._objectives = list()
        self._analysis = Analysis()
        self._has_run = False

    @property
    def analysis(self) -> Analysis:
        return self._analysis

    @property
    def load_cases(self):
        return list(self._load_steps.keys())

    def run(self):
        """
        This method executes the necessary system evaluations depending on the added parameters and objectives
         the analysis are stored in _analysis (a Analysis class).

        """
        if not self._has_run:
            # First, attach objective functions to system and sources
            for objective in self._objectives:
                objective.engage()
            # The evaluation order depends on the parameters that are added to the simulation
            if not self._parameters:
                # No parameters in simulation step, just one evaluation needed
                result = self.evaluate()
                self._analysis.add_result(result)
            else:
                # Parameters are present in simulation step
                if get_iterable(self._parameters):
                    # There are iterable parameters in this step
                    # get list of tuples that yield all combinations of parameters
                    combinations = list(itertools.product(*get_iterable(self._parameters)))
                else:
                    # There are no iterable parameters and thus no combinations
                    combinations = [()]
                # Now we start iterating the combinations
                n_comb = 1
                for combination in combinations:
                    # First evaluate system for iterable system
                    self.update_parameters(pars=get_iterable(self._parameters),
                                           values=combination)
                    if get_non_iterable(self._parameters):
                        # There are optimization parameters in this step
                        # create optimizer and optimize parameters
                        optimizer = Optimizer(eval_func=self.evaluate, update_fun=self.update_parameters,
                                              pars=get_non_iterable(self._parameters))
                        optimizer.optimize()
                    # Get result and store
                    result = self.evaluate()
                    result.id = n_comb
                    n_comb += 1
                    # store result list in collection
                    self._analysis.add_result(result)
            # After running the simulation all objective wil be detached
            for objective in self._objectives:
                objective.disengage()
            # Lock simulation until it has been reset
            self._has_run = True
        else:
            raise Exception("This simulation has already run and is locked until a reset() is given!")

    def update_parameters(self, pars: tuple[Parameter] = (), values: tuple = ()):
        for parameter, value in zip(pars, values):
            self._parameters[parameter] = value

    def evaluate(self) -> Result:
        """
            update the values for the parameters and evaluate system
        """
        # Set all paramter values
        for parameter, value in self._parameters.items():
            parameter.set_value(value)
        # create result object
        result = Result()
        # Solve the system for all load cases
        for load_case in self.load_cases:
            steps = self._load_steps[load_case] + self._model_steps
            for step in steps:
                for item in step.items:
                    item.evaluate(paths=step.paths)
            for path in self.paths:
                variable_list, result_objects = path.unload()
                result.add_result_objects(load_case, variable_list, result_objects)
                path.reset()

            # create list of parameter value
            par_list = [ParameterValue(value=val, parent=par) for par, val in self._parameters.items()]
            result.add_result_objects(load_case=load_case, result_objs=par_list) if par_list else None
        return result


class Optimizer:
    """ 
    Optimizer optimizes a set of parameters for the objective(s)
    that are found in the items or load case trees
    
        Attributes
        ------------
        memory (bool): if true all optimization steps are stored

        Methods
        ------------
        optimize: start parameter optimization

    """

    def __init__(self, eval_func: Callable, update_fun: Callable, pars: tuple[SettingsParameter]):
        self._parameters = pars
        self._eval_fun = eval_func
        self.update_fun = update_fun

    def _eval_constraints(self, par_values: ArrayLike):
        """evaluates the constraints of a system-load_case pair. It first updates the parameters, and then evaluates the constraints

        Parameters
        ----------
        par_values: ArrayLike
            Set of parameter values
        """
        self.update_fun(pars=self._parameters,
                        values=par_values)
        # self system
        results = self._eval_fun()

        constraint_values = [constraint.evaluate() for constraint in results.constraints]
        # print(f"Parameter values are {par_values} and constraint values are {constraint_values}")
        # get constraint status
        return constraint_values

    def _eval_cost(self, par_values: ArrayLike):
        """evaluates the cost of a system-load_case pair. It first updates the parameters, and then evaluates the cost

        Parameters
        ----------
        par_values: ArrayLike
            Set of parameter values
        """
        self.update_fun(pars=self._parameters,
                        values=par_values)
        # calculate the model
        results = self._eval_fun()

        # evaluate the costs
        result_scope = list(filter(lambda cost: cost.parent.optimize, results.costs))

        cost_values = [cost.evaluate() for cost in result_scope]

        # print(f"Parameter values are {par_values} and cost is {cost_values}")
        return sum(cost_values)

    def optimize(self):
        methods = ['trust-constr', 'SLSQP', 'COBYLA']

        lower_bound = []
        upper_bound = []
        init_guess = []
        for parameter in self._parameters:
            lower_bound.append(parameter.lb)
            upper_bound.append(parameter.ub)
            init_guess.append(parameter.x0)

        bounds = Bounds(lb=lower_bound, ub=upper_bound, keep_feasible=True)
        nonlinear_constraint = NonlinearConstraint(fun=self._eval_constraints, lb=-np.inf, ub=0, jac='3-point')
        x0 = np.array(init_guess)

        res = minimize(self._eval_cost, x0=x0, method=methods[1], constraints=nonlinear_constraint,
                       options={'verbose': 1}, bounds=bounds)
        print(res)


@dataclass(slots=True)
class Step(ABC):
    name: str
    paths: list[Path] | Path
    items: list[Model] | Model

    def __post_init__(self):
        if type(self.paths) is not list: self.paths = [self.paths]
        if type(self.items) is not list: self.items = [self.items]
