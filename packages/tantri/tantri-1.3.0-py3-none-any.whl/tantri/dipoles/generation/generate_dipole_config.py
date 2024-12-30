import numpy
from typing import Sequence, Optional
from tantri.dipoles.types import DipoleTO, DipoleGenerationConfig, Orientation
import logging


# stuff for generating random dipoles from parameters

_logger = logging.getLogger(__name__)


def make_dipoles(
	config: DipoleGenerationConfig,
	rng_override: Optional[numpy.random.Generator] = None,
) -> Sequence[DipoleTO]:

	if rng_override is None:
		_logger.info(
			f"Using the seed [{config.generation_seed}] provided by configuration for dipole generation"
		)
		rng = numpy.random.default_rng(config.generation_seed)
	else:
		_logger.info("Using overridden rng, of unknown seed")
		rng = rng_override

	dipoles = []

	for i in range(config.dipole_count):
		sx = rng.uniform(config.x_min, config.x_max)
		sy = rng.uniform(config.y_min, config.y_max)
		sz = rng.uniform(config.z_min, config.z_max)

		# orientation
		# 0, 1, 2
		# xy, z, random

		if config.orientation is Orientation.RANDOM:
			theta = numpy.arccos(2 * rng.random() - 1)
			phi = 2 * numpy.pi * rng.random()
		elif config.orientation is Orientation.Z:
			theta = 0
			phi = 0
		elif config.orientation is Orientation.XY:
			theta = numpy.pi / 2
			phi = 2 * numpy.pi * rng.random()
		else:
			raise ValueError(
				f"this shouldn't have happened, orientation index: {config}"
			)

		px = config.mag * numpy.cos(phi) * numpy.sin(theta)
		py = config.mag * numpy.sin(phi) * numpy.sin(theta)
		pz = config.mag * numpy.cos(theta)

		w = 10 ** rng.uniform(config.w_log_min, config.w_log_max)

		dipoles.append(
			DipoleTO(numpy.array([px, py, pz]), numpy.array([sx, sy, sz]), w)
		)

	return dipoles
