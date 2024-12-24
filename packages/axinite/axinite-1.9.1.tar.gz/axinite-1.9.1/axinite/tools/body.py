from astropy.coordinates import CartesianRepresentation
from astropy.constants import G
from axinite.functions import vector_to, apply_to_vector, vector_magnitude, unit_vector
import astropy.units as u
from math import pi
from numpy import float64

class Body:
    def __init__(self, name, mass: u.Quantity, position: CartesianRepresentation, velocity: CartesianRepresentation, radius: u.Quantity, color:str="", light:bool=False, retain=None, radius_multiplier=1):
        self.mass = mass
        self.r = { float64(0): position}
        self.v = { float64(0): velocity}
        self.name = name
        self.radius = radius * radius_multiplier
        self.color = color
        self.light = light
        self.retain = retain
        self.radius_multiplier = radius_multiplier

    def gravitational_force(self, r: CartesianRepresentation, m: u.Quantity):
        return -G * ((self.mass * m) / vector_magnitude(r)**2) * unit_vector(r)