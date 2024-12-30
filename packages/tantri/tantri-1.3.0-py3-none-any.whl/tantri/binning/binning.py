import typing
import numpy
import logging
from dataclasses import dataclass


_logger = logging.getLogger(__name__)


@dataclass
class BinConfig:
	log_scale: bool  # true means that our bins of the x coordinate will be in
	# if linear scale (not log_scale) then the semantics are
	# min_x, min_x + bin_width, .... min_x + A * bin_width, max_x (and the last bin may not be evenly spaced)
	# if log_scale then log(min_x), log(min_x) + bin_width, log(min_x) + 2 bin_width etc.
	# (so essentially the units of bin_width depend on log_scale)
	bin_width: float
	# never log, will be logarithmed if needed
	bin_min: typing.Optional[float] = None

	# note that min_points_required must be >= 2
	min_points_required: int = 2

	def __post_init__(self):
		if self.min_points_required < 2:
			raise ValueError(
				f"Can't compute summary statistics with bins of size < 2, so {self.min_points_required} is invalid"
			)


@dataclass
class BinSummaryValue:
	mean_y: float
	stdev_y: float


def _summarise_values(ys: numpy.ndarray) -> BinSummaryValue:
	mean_y = ys.mean(axis=0).item()
	stdev_y = ys.std(axis=0, ddof=1).item()
	return BinSummaryValue(mean_y, stdev_y)


@dataclass
class BinSummary:
	mean_x: float
	summary_values: typing.Dict[str, BinSummaryValue]


@dataclass
class Bin:
	bindex: int  # this is going to be very specific to a particular binning but hey let's include it
	x_min: float
	# points is a tuple of (freqs, value_dicts: Dict[str, numpy.ndarray])
	# this conforms well to APSD result
	point_xs: numpy.ndarray
	point_y_dict: typing.Dict[str, numpy.ndarray]

	def mean_point(self) -> typing.Tuple[float, typing.Dict[str, float]]:
		mean_x = self.point_xs.mean(axis=0).item()
		mean_y_dict = {k: v.mean(axis=0).item() for k, v in self.point_y_dict.items()}
		return (mean_x, mean_y_dict)

	def summary_point(self) -> BinSummary:
		mean_x = self.point_xs.mean(axis=0).item()
		summary_dict = {k: _summarise_values(v) for k, v in self.point_y_dict.items()}
		return BinSummary(mean_x, summary_dict)


def _construct_bins(xs: numpy.ndarray, bin_config: BinConfig) -> numpy.ndarray:
	min_x_raw = numpy.min(xs)

	# if the bin config requested bin_min is None, then we can ignore it.

	if bin_config.bin_min is not None:
		_logger.debug(f"Received a desired bin_min={bin_config.bin_min}")
		if bin_config.bin_min > min_x_raw:
			raise ValueError(
				f"The lowest x value of {xs=} was {min_x_raw=}, which is lower than the requested bin_min={bin_config.bin_min}"
			)
		else:
			_logger.debug(f"Setting minimum to {bin_config.bin_min}")
			min_x_raw = bin_config.bin_min

	max_x_raw = numpy.max(xs)

	if bin_config.log_scale:
		min_x = numpy.log10(min_x_raw)
		max_x = numpy.log10(max_x_raw)
	else:
		min_x = min_x_raw
		max_x = max_x_raw

	num_points = numpy.ceil(1 + (max_x - min_x) / bin_config.bin_width)
	bins = min_x + (numpy.arange(0, num_points) * bin_config.bin_width)

	if bin_config.log_scale:
		return 10**bins
	else:
		return bins


def _populate_bins(
	xs: numpy.ndarray, ys: typing.Dict[str, numpy.ndarray], bins: numpy.ndarray
) -> typing.Sequence[Bin]:
	indexes = numpy.digitize(xs, bins) - 1
	output_bins = []

	seen = set()

	for bindex in indexes:
		if bindex not in seen:
			seen.add(bindex)

			matched_x = xs[indexes == bindex]
			matched_output_dict = {k: v[indexes == bindex] for k, v in ys.items()}
			output_bins.append(
				Bin(
					bindex,
					x_min=bins[bindex].item(),
					point_xs=matched_x,
					point_y_dict=matched_output_dict,
				)
			)

	return output_bins


def bin_lists(
	xs: numpy.ndarray, ys: typing.Dict[str, numpy.ndarray], bin_config: BinConfig
) -> typing.Sequence[Bin]:
	bins = _construct_bins(xs, bin_config)
	raw_bins = _populate_bins(xs, ys, bins)
	return [
		bin for bin in raw_bins if len(bin.point_xs) >= bin_config.min_points_required
	]
