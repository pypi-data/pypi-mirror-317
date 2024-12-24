"""
Cryptocurrency Wallet Seed Finder Package

This package implements a parallel processing system to find cryptocurrency wallet seeds
by generating and testing permutations of seed phrases.
"""

from .core import Core

__version__ = "1.0.9"
__all__ = ['Core']
