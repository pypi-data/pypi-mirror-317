# mGenS/__init__.py

"""
mGenS - A package for support functions.
"""

# Import functions from func.py
from .func import manipulator, merge_lists, save_matching_value, last_non_zero, keep_last_non_zero, remove_last_number, fill_missing, fill_na, payoutCalculator, payoutCalculatorFP, bonusPool, PD400calculator, PD400Evaluator, focusproductGenerator  # Replace with actual function names

# You can also define package-level variables or metadata here
__version__ = "0.1.1"
__author__ = "Hathaway Zhang"
__email__ = "hathaway.zhang@example.com"

# Optionally, you can define what is imported when using 'from mGenS import *'
__all__ = ['manipulator', 'merge_lists', 'save_matching_value', 'last_non_zero', 'keep_last_non_zero', 'remove_last_number', 'fill_missing', 'fill_na', 'payoutCalculator', 'payoutCalculatorFP', 'bonusPool', 'PD400calculator', 'PD400Evaluator', 'focusproductGenerator']  # Add all functions you want to expose