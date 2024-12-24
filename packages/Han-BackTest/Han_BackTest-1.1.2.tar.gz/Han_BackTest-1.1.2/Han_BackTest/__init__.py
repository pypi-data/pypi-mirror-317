# Han_BackTest/__init__.py
from .DataClass import DataClass
from .FactorClass import FactorClass, FactorLibrary
from .StrategyClass import StrategyClass
from .BackTestClass import BackTestClass

__all__ = ["DataClass", "FactorClass", "FactorLibrary", "StrategyClass", "BackTestClass"]

__version__ = "1.1.1"
__author__ = "Jiaheng Han"
__email__ = "hanjiaheng@stu.pku.edu.cn"

import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)