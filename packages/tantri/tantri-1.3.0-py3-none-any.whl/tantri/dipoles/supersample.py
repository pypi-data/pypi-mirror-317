import dataclasses
import logging
import math

_logger = logging.getLogger(__name__)

# how many times faster than the max frequency we want to be, bigger is more accurate but 10 is probably fine
DESIRED_THRESHOLD = 10


@dataclasses.dataclass
class SuperSample:
	super_dt: float
	super_sample_ratio: int


def get_supersample(max_frequency: float, dt: float) -> SuperSample:
	# now we want to sample at least 10x faster than max_frequency, otherwise we're going to skew our statistics
	# note that this is why if performance mattered we'd be optimising this to pre-gen our flip times with poisson statistics.
	# so we want (1/dt) > 10 * max_freq
	if DESIRED_THRESHOLD * dt * max_frequency < 1:
		# can return unchanged
		_logger.debug("no supersampling needed")
		return SuperSample(super_dt=dt, super_sample_ratio=1)
	else:
		# else we want a such that a / dt > 10 * max_freq, or a > 10 * dt * max_freq, a = math.ceil(10 * dt * max_freq)
		a = math.ceil(DESIRED_THRESHOLD * dt * max_frequency)
		_logger.debug(
			f"max_frequency {max_frequency} and delta_t {dt} needs a ratio of {a}"
		)
		ret_val = SuperSample(super_dt=dt / a, super_sample_ratio=a)
		_logger.debug(ret_val)
		return ret_val
