from dataclasses import dataclass
import numpy
import numpy.random
import typing
from tantri.dipoles.types import DipoleTO, DotPosition, DipoleMeasurementType
import tantri.dipoles.supersample
import tantri.util
import scipy.stats
import scipy.fft
import logging

_logger = logging.getLogger(__name__)


@dataclass
class APSDResult:
	psd_dict: typing.Dict[str, numpy.ndarray]
	freqs: numpy.ndarray


@dataclass
class TimeSeriesResult:
	series_dict: typing.Dict[str, numpy.ndarray]
	num_points: int
	delta_t: float

	def get_time_points(self):
		return [t * self.delta_t for t in range(self.num_points)]

	def get_apsds(self) -> APSDResult:
		def sq(a):
			return numpy.real(a * numpy.conjugate(a))

		def psd(v):
			_logger.debug("Using real part correction and multiplying PSD by 2")
			return 2 * sq(scipy.fft.rfft(v)[1:]) * self.delta_t / self.num_points

		fft_dict = {k: psd(v) for k, v in self.series_dict.items()}
		freqs = scipy.fft.rfftfreq(self.num_points, self.delta_t)[1:]

		return APSDResult(fft_dict, freqs)


def average_apsds(apsds: typing.Sequence[APSDResult]) -> APSDResult:
	def mean(list_of_arrays: typing.Sequence[numpy.ndarray]) -> numpy.ndarray:
		return numpy.mean(numpy.array(list_of_arrays), axis=0)

	if len(apsds) >= 1:
		for subsequent in apsds[1:]:
			if not numpy.array_equal(subsequent.freqs, apsds[0].freqs):
				raise ValueError(
					f"Could not average apsds, as {subsequent} does not match the frequencies in {apsds[0]}"
				)
	freqs = apsds[0].freqs

	average_dict = tantri.util.dict_reduce([apsd.psd_dict for apsd in apsds], mean)
	return APSDResult(average_dict, freqs)


@dataclass
class WrappedDipole:
	# assumed len 3
	p: numpy.ndarray
	s: numpy.ndarray

	# should be 1/tau up to some pis
	w: float

	# For caching purposes tell each dipole where the dots are
	# TODO: This can be done better by only passing into the time series the non-repeated p s and w,
	# TODO: and then creating a new wrapper type to include all the cached stuff.
	# TODO: Realistically, the dot positions and measurement type data should live in the time series.
	dot_positions: typing.Sequence[DotPosition]

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

	def transition(
		self, dt: float, rng_to_use: typing.Optional[numpy.random.Generator] = None
	) -> typing.Dict[str, float]:
		rng: numpy.random.Generator
		if rng_to_use is None:
			rng = numpy.random.default_rng()
		else:
			rng = rng_to_use
		# if on average flipping often, then just return 0, basically this dipole has been all used up.
		# Facilitates going for different types of noise at very low freq?
		if dt * 10 >= 1 / self.w:
			# _logger.warning(
			# 	f"delta t {dt} is too long compared to dipole frequency {self.w}"
			# )
			self.state = rng.integers(0, 1, endpoint=True)
		else:
			prob = dt * self.w
			if rng.random() < prob:
				# _logger.debug("flip!")
				self.flip_state()
		return {k: self.state * v for k, v in self.cache.items()}

	def time_series(
		self,
		dt: float,
		num_points: int,
		rng_to_use: typing.Optional[numpy.random.Generator] = None,
	) -> typing.Dict[str, numpy.ndarray]:

		# don't forget to set rng
		if rng_to_use is None:
			rng = numpy.random.default_rng()
		else:
			rng = rng_to_use

		# scale effective mu by the sample rate.
		# mu (or w) has units of events/time, so effective rate is events/time * dt, giving mu per dt
		eff_mu = dt * self.w
		events = scipy.stats.poisson.rvs(eff_mu, size=num_points, random_state=rng)
		telegraph_sequence = numpy.cumprod((-1) ** events)

		return {k: telegraph_sequence * v for k, v in self.cache.items()}

	def flip_state(self):
		self.state *= -1


def get_wrapped_dipoles(
	dipole_tos: typing.Sequence[DipoleTO],
	dots: typing.Sequence[DotPosition],
	measurement_type: DipoleMeasurementType,
) -> typing.Sequence[WrappedDipole]:
	return [
		WrappedDipole(
			p=dipole_to.p,
			s=dipole_to.s,
			w=dipole_to.w,
			dot_positions=dots,
			measurement_type=measurement_type,
		)
		for dipole_to in dipole_tos
	]


class DipoleTimeSeries:
	def __init__(
		self,
		dipoles: typing.Sequence[DipoleTO],
		dots: typing.Sequence[DotPosition],
		measurement_type: DipoleMeasurementType,
		dt: float,
		rng_to_use: typing.Optional[numpy.random.Generator] = None,
	):
		self.rng: numpy.random.Generator
		if rng_to_use is None:
			self.rng = numpy.random.default_rng()
		else:
			self.rng = rng_to_use

		self.dipoles = get_wrapped_dipoles(dipoles, dots, measurement_type)
		self.state = 0

		self.real_delta_t = dt

		# we may need to supersample, because of how dumb this process is.
		# let's find our highest frequency
		max_frequency = max(d.w for d in self.dipoles)

		super_sample = tantri.dipoles.supersample.get_supersample(max_frequency, dt)
		self.dt = super_sample.super_dt
		self.super_sample_ratio = super_sample.super_sample_ratio

	def _sub_transition(self) -> typing.Dict[str, float]:
		new_vals = [dipole.transition(self.dt, self.rng) for dipole in self.dipoles]

		ret = {}
		for transition in new_vals:
			for k, v in transition.items():
				if k not in ret:
					ret[k] = v
				else:
					ret[k] += v
		return ret

	def transition(self) -> typing.Dict[str, float]:
		return [self._sub_transition() for i in range(self.super_sample_ratio)][-1]

	def _generate_series(
		self, num_points: int, delta_t: float
	) -> typing.Dict[str, numpy.ndarray]:

		serieses = [
			dipole.time_series(delta_t, num_points, self.rng) for dipole in self.dipoles
		]

		result = {}
		for series in serieses:
			for k, v in series.items():
				if k not in result:
					result[k] = v
				else:
					result[k] += v

		return result

	def generate_series(
		self, num_points: int, override_delta_t: typing.Optional[float] = None
	) -> TimeSeriesResult:

		delta_t_to_use: float
		if override_delta_t is not None:
			delta_t_to_use = override_delta_t
		else:
			delta_t_to_use = self.real_delta_t

		series = self._generate_series(num_points, delta_t_to_use)

		return TimeSeriesResult(
			series_dict=series, num_points=num_points, delta_t=delta_t_to_use
		)

	def generate_average_apsd(
		self,
		num_series: int,
		num_time_series_points: int,
		override_delta_t: typing.Optional[float] = None,
	) -> APSDResult:

		apsds = [
			self.generate_series(num_time_series_points, override_delta_t).get_apsds()
			for _ in range(num_series)
		]

		_logger.debug(f"Averaging {num_series} series")

		return average_apsds(apsds)
