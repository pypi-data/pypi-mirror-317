""" This module contains the basic building blocks for creating models

submodules
-----------
paths :
    module that provide the Path class that track the flow of energy through the system.
settings : 
    module that contains the Settings class that is used to built settings objects.
tree : 
    module that contains a Composite design pattern (models and Composite class) that is used to built tree structures.
_variables :
    module that yields the Variable class that contains the flow and effort of the system.

"""
from .settings import Settings
