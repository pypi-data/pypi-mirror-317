"""
Top-level module for BigQuery Migrations

This module
- tracks the version of the package

"""
from .migration import Migration

__all__ = [
    "Migration"
]
__version__ = "0.5.2"
