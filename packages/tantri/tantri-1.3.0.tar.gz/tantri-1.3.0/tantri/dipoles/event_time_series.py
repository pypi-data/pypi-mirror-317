import numpy.random
from typing import Callable, Sequence, Tuple, Optional, Dict, List
from dataclasses import dataclass
from tantri.dipoles.types import DipoleTO, DotPosition, DipoleMeasurementType
import logging

_logger = logging.getLogger(__name__)


@dataclass
class EventWrappedDipole:
	# assumed len 3
	p: numpy.ndarray
	s: numpy.ndarray

	# should be 1/tau up to some pis
	w: float

	# For caching purposes tell each dipole where the dots are
	# TODO: This can be done better by only passing into the time series the non-repeated p s and w,
	# TODO: and then creating a new wrapper type to include all the cached stuff.
	# TODO: Realistically, the dot positions and measurement type data should live in the time series.
	dot_positions: Sequence[DotPosition]

	measurement_type: DipoleMeasurementType

	def __post_init__(self) -> None:
		"""
		Coerce the inputs into numpy arrays.
		"""
		self.p = numpy.array(self.p)
		self.s = numpy.array(self.s)

		self.state = 1
		self.cache = {}
		for pos in self.dot_positions:
			if self.measurement_type is DipoleMeasurementType.ELECTRIC_POTENTIAL:
				self.cache[pos.label] = self.potential(pos)
			elif self.measurement_type is DipoleMeasurementType.X_ELECTRIC_FIELD:
				self.cache[pos.label] = self.e_field_x(pos)

	def potential(self, dot: DotPosition) -> float:
		# let's assume single dot at origin for now
		r_diff = self.s - dot.r
		return self.p.dot(r_diff) / (numpy.linalg.norm(r_diff) ** 3)

	def e_field_x(self, dot: DotPosition) -> float:
		# let's assume single dot at origin for now
		r_diff = self.s - dot.r
		norm = numpy.linalg.norm(r_diff)

		return (
			((3 * self.p.dot(r_diff) * r_diff / (norm**2)) - self.p) / (norm**3)
		)[0]

	def get_time_series(
		self, dt: float, num_samples: int, rng: numpy.random.Generator
	) -> Sequence[Tuple[float, Dict[str, float]]]:
		_logger.debug(
			f"Creating time series with params {dt=}, {num_samples=}, scale={self.w}"
		)
		raw_time_series = create_exponential_time_series(rng, dt, num_samples, self.w)
		output = []

		for time, state in raw_time_series:
			output.append((time, {k: state * v for k, v in self.cache.items()}))
		return output


def get_event_wrapped_dipoles(
	dipole_tos: Sequence[DipoleTO],
	dots: Sequence[DotPosition],
	measurement_type: DipoleMeasurementType,
) -> Sequence[EventWrappedDipole]:
	return [
		EventWrappedDipole(
			p=dipole_to.p,
			s=dipole_to.s,
			w=dipole_to.w,
			dot_positions=dots,
			measurement_type=measurement_type,
		)
		for dipole_to in dipole_tos
	]


class EventDipoleTimeSeries:
	def __init__(
		self,
		dipoles: Sequence[DipoleTO],
		dots: Sequence[DotPosition],
		measurement_type: DipoleMeasurementType,
		dt: float,
		num_samples: int,
		rng_to_use: Optional[numpy.random.Generator] = None,
	):
		self.rng: numpy.random.Generator
		if rng_to_use is None:
			self.rng = numpy.random.default_rng()
		else:
			self.rng = rng_to_use

		self.dt = dt
		self.num_samples = num_samples
		self.dipoles = get_event_wrapped_dipoles(dipoles, dots, measurement_type)

	def create_time_series(self) -> Sequence[Tuple[float, Dict[str, float]]]:
		collected_dictionary: Dict[float, Dict[str, float]] = {}
		_logger.debug("Creating time series")

		for dipole in self.dipoles:
			_logger.debug(f"Doing dipole {dipole}")
			series = dipole.get_time_series(self.dt, self.num_samples, self.rng)
			for time, meases in series:
				if time in collected_dictionary:
					for k, v in meases.items():

						collected_dictionary[time][k] += v
				else:
					collected_dictionary[time] = meases

		return [(k, v) for k, v in collected_dictionary.items()]


def get_num_events_before(
	rng: numpy.random.Generator, scale: float, total_time: float
) -> Callable[[float], int]:

	_logger.debug(
		f"Creating the events before function for params {scale=} {total_time=}"
	)
	event_times: List = []
	random_size = max(1, int(total_time // scale))
	while sum(event_times) < total_time:
		event_times.extend(rng.exponential(scale=scale, size=random_size))

	accumulator = 0
	scanned_times = [accumulator := accumulator + t for t in event_times]

	def num_events_before(time: float) -> int:
		return len([t for t in scanned_times if t < time])

	return num_events_before


def create_exponential_time_series(
	rng: numpy.random.Generator, dt: float, num_samples: int, scale: float
) -> Sequence[Tuple[float, int]]:
	_logger.debug("Creating an exponential time series")
	total_time = dt * num_samples
	_logger.debug(f"Have a total time {total_time}")
	events_before = get_num_events_before(rng, scale, total_time)
	_logger.debug("Finished getting the events before function")
	return [(dt * i, (events_before(dt * i) % 2) * 2 - 1) for i in range(num_samples)]
