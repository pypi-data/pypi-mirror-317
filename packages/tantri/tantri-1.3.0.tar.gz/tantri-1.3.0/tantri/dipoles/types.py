import numpy
from dataclasses import dataclass, asdict
from enum import Enum


# Lazily just separating this from Dipole where there's additional cached stuff, this is just a thing
# we can use as a DTO For dipole info.
@dataclass
class DipoleTO:
	# assumed len 3
	p: numpy.ndarray
	s: numpy.ndarray

	# should be 1/tau up to some pis
	w: float

	def as_dict(self) -> dict:
		return asdict(self)


class Orientation(str, Enum):
	# Enum for orientation, making string for json serialisation purposes
	#
	# Note that this might not be infinitely extensible?
	# https://stackoverflow.com/questions/75040733/is-there-a-way-to-use-strenum-in-earlier-python-versions
	XY = "XY"
	Z = "Z"
	RANDOM = "RANDOM"


# A description of the parameters needed to generate random dipoles
@dataclass
class DipoleGenerationConfig:
	# note no actual checks anywhere that these are sensibly defined with min less than max etc.
	x_min: float
	x_max: float
	y_min: float
	y_max: float
	z_min: float
	z_max: float

	mag: float

	# these are log_10 of actual value
	w_log_min: float
	w_log_max: float

	orientation: Orientation

	dipole_count: int
	generation_seed: int

	def __post_init__(self):
		# This allows us to transparently set this with a string, while providing early warning of a type error
		self.orientation = Orientation(self.orientation)

	def as_dict(self) -> dict:
		return_dict = asdict(self)

		return_dict["orientation"] = return_dict["orientation"].value

		return return_dict


class DipoleMeasurementType(Enum):
	ELECTRIC_POTENTIAL = 1
	X_ELECTRIC_FIELD = 2


@dataclass(frozen=True)
class DotPosition:
	# assume len 3
	r: numpy.ndarray
	label: str
