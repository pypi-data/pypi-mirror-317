"""
Cryptocurrency Wallet Seed Finder Package

This package implements a parallel processing system to find cryptocurrency wallet seeds
by generating and testing permutations of seed phrases.
"""

from .core import main, validate_device, get_config, save_config, start_process

__version__ = "1.0.7"
__all__ = ['main', 'validate_device', 'get_config', 'save_config', 'start_process']
