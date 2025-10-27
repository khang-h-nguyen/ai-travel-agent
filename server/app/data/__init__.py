"""
Data Layer

Static data and mock databases for destinations, activities, etc.
"""

from .destinations import DESTINATIONS_DB, get_destination

__all__ = ["DESTINATIONS_DB", "get_destination"]
