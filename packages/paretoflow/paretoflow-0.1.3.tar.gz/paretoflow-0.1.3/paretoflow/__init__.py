"""
ParetoFlow: A Python Library for Multi-Objective Optimization by using
Generative Flows and Multi Predictors Guidance to approximate the Pareto Front.
"""

__version__ = "0.1.3"
__author__ = "Ye Yuan, Can Chen"
__credits__ = (
    "Mila - Quebec AI Institute, McGill University Cyber Physical System Lab (CPSL)"
)

from paretoflow.flow_net import FlowMatching, VectorFieldNet
from paretoflow.multiple_model_predictor import MultipleModels
from paretoflow.paretoflow import ParetoFlow
