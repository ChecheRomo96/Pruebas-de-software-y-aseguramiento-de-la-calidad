"""
Initialization module for the application.

Imports core classes to make them available at the package level.
"""

from .base_classes.hotel import Hotel
from .base_classes.customer import Customer
from .base_classes.reservation import Reservation

__all__ = ["Hotel", "Customer", "Reservation"]  # Mark them as intended exports
