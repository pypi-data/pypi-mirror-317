import click
import logging
import tantri
import numpy
import tantri.cli.input_files.write_dipoles
import tantri.cli.file_importer
import tantri.binning
import json
import tantri.dipoles
import tantri.dipoles.event_time_series
import pathlib


_logger = logging.getLogger(__name__)

LOG_PATTERN = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


POTENTIAL = "electric-potential"
X_ELECTRIC_FIELD = "x-electric-field"


def _set_up_logging(filename):
	handlers = [logging.StreamHandler()]
	if filename is not None:
		handlers.append(logging.FileHandler(filename))
	logging.basicConfig(
		level=logging.DEBUG,
		format=LOG_PATTERN,
		handlers=handlers,
	)
	logging.getLogger("pdme").setLevel(logging.INFO)
	logging.captureWarnings(True)


@click.group()
@click.option(
	"--log", help="Enable logging to stream only", is_flag=True, default=False
)
@click.option("--log-file", help="A filename to use for logging (implies --log)")
@click.version_option(tantri.get_version())
def cli(log, log_file):
	"""Utilities for generating simulated TLS time series data."""
	if log or (log_file is not None):
		# log file has been provided, let's log
		_set_up_logging(log_file)


@cli.command()
@click.option(
	"--dipoles-file",
	default="dipoles.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dipoles",
)
@click.option(
	"--dots-file",
	default="dots.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dots",
)
@click.option(
	"--measurement-type",
	type=click.Choice([POTENTIAL, X_ELECTRIC_FIELD]),
	default=POTENTIAL,
	help="The type of measurement to simulate",
	show_default=True,
)
@click.option(
	"--delta-t",
	"-t",
	type=float,
	default=1,
	help="The delta t between time series iterations.",
	show_default=True,
)
@click.option(
	"--num-iterations",
	"-n",
	type=int,
	default=10,
	help="The number of iterations.",
	show_default=True,
)
@click.option(
	"--time-series-rng-seed",
	"-s",
	type=int,
	default=None,
	help="A seed to use to create an override default rng. You should set this.",
)
@click.option(
	"output_file",
	"-o",
	type=click.Path(path_type=pathlib.Path),
	help="The output file to write, in csv format",
	required=True,
)
@click.option("--header-row/--no-header-row", default=False, help="Write a header row")
@click.option(
	"--event-based/--no-event-based", default=False, help="Use new event-based method"
)
def write_time_series(
	dipoles_file,
	dots_file,
	measurement_type,
	delta_t,
	num_iterations,
	time_series_rng_seed,
	output_file,
	header_row,
	event_based,
):
	"""
	Generate a time series for the passed in parameters.
	"""
	_write_time_series(
		dipoles_file,
		dots_file,
		measurement_type,
		delta_t,
		num_iterations,
		time_series_rng_seed,
		output_file,
		header_row,
		event_based,
	)


def _write_time_series(
	dipoles_file,
	dots_file,
	measurement_type,
	delta_t,
	num_iterations,
	time_series_rng_seed,
	output_file,
	header_row,
	new_method,
):
	_logger.debug(
		f"Received parameters [dipoles_file: {dipoles_file}] and [dots_file: {dots_file}]"
	)
	dipoles = tantri.cli.file_importer.read_dipoles_json_file(dipoles_file)
	dots = tantri.cli.file_importer.read_dots_json_file(dots_file)

	if measurement_type == POTENTIAL:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.ELECTRIC_POTENTIAL
		value_name = "V"
	elif measurement_type == X_ELECTRIC_FIELD:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.X_ELECTRIC_FIELD
		value_name = "Ex"

	_logger.debug(f"Using measurement {measurement_enum.name}")
	labels = [dot.label for dot in dots]
	with output_file.open("w") as out:
		if header_row:
			value_labels = ", ".join([f"{value_name}_{label}" for label in labels])
			out.write(f"t (s), {value_labels}\n")

		_logger.debug(
			f"Going to simulate {num_iterations} iterations with a delta t of {delta_t}"
		)

		if new_method:
			_logger.info("Using new method")
			_logger.debug(f"Got seed {time_series_rng_seed}")
			if time_series_rng_seed is None:
				time_series = tantri.dipoles.event_time_series.EventDipoleTimeSeries(
					dipoles, dots, measurement_enum, delta_t, num_iterations
				)
			else:
				rng = numpy.random.default_rng(time_series_rng_seed)
				time_series = tantri.dipoles.event_time_series.EventDipoleTimeSeries(
					dipoles, dots, measurement_enum, delta_t, num_iterations, rng
				)
			output_series = time_series.create_time_series()
			for time, time_series_dict in output_series:
				values = ", ".join(str(time_series_dict[label]) for label in labels)
				out.write(f"{time}, {values}\n")

		else:
			# in the old method
			_logger.debug(f"Got seed {time_series_rng_seed}")
			if time_series_rng_seed is None:
				time_series = tantri.dipoles.DipoleTimeSeries(
					dipoles, dots, measurement_enum, delta_t
				)
			else:
				rng = numpy.random.default_rng(time_series_rng_seed)
				time_series = tantri.dipoles.DipoleTimeSeries(
					dipoles, dots, measurement_enum, delta_t, rng
				)

			for i in range(num_iterations):
				transition = time_series.transition()
				transition_values = ", ".join(
					str(transition[label]) for label in labels
				)
				out.write(f"{i * delta_t}, {transition_values}\n")


@cli.command()
@click.option(
	"--dipoles-file",
	default="dipoles.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dipoles",
)
@click.option(
	"--dots-file",
	default="dots.json",
	show_default=True,
	type=click.Path(exists=True, path_type=pathlib.Path),
	help="File with json array of dots",
)
@click.option(
	"--measurement-type",
	type=click.Choice([POTENTIAL, X_ELECTRIC_FIELD]),
	default=POTENTIAL,
	help="The type of measurement to simulate",
	show_default=True,
)
@click.option(
	"--delta-t",
	"-t",
	type=float,
	default=1,
	help="The delta t between time series iterations.",
	show_default=True,
)
@click.option(
	"--num-iterations",
	# Note we're keeping this name to match write-time-series
	"-n",
	type=int,
	default=10,
	help="The number of time steps per time series, total time is num_iterations * delta_t.",
	show_default=True,
)
@click.option(
	"--num-time-series",
	type=int,
	default=20,
	help="The number of simulated time series, which will be averaged over",
	show_default=True,
)
@click.option(
	"--time-series-rng-seed",
	"-s",
	type=int,
	default=None,
	help="A seed to use to create an override default rng. You should set this.",
)
@click.option(
	"--output-file",
	"-o",
	type=click.Path(path_type=pathlib.Path),
	help="The output file to write, in csv format",
	required=True,
)
@click.option(
	"--binned-output-file",
	"-b",
	type=click.Path(path_type=pathlib.Path),
	help="Optional binned output file",
)
@click.option(
	"--bin-widths",
	type=float,
	default=1,
	show_default=True,
	help="The default log(!) bin width, 1 means widths of a decade",
)
@click.option("--header-row/--no-header-row", default=False, help="Write a header row")
def write_apsd(
	dipoles_file,
	dots_file,
	measurement_type,
	delta_t,
	num_iterations,
	num_time_series,
	time_series_rng_seed,
	output_file,
	binned_output_file,
	bin_widths,
	header_row,
):
	"""
	Generate an APSD for the passed in parameters, averaging over multiple (num_time_series) iterations.
	"""
	_write_apsd(
		dipoles_file,
		dots_file,
		measurement_type,
		delta_t,
		num_iterations,
		num_time_series,
		time_series_rng_seed,
		output_file,
		binned_output_file,
		bin_widths,
		header_row,
	)


def _write_apsd(
	dipoles_file,
	dots_file,
	measurement_type,
	delta_t,
	num_iterations,
	num_time_series,
	time_series_rng_seed,
	output_file,
	binned_output_file,
	bin_widths,
	header_row,
):
	_logger.debug(
		f"Received parameters [dipoles_file: {dipoles_file}] and [dots_file: {dots_file}]"
	)
	dipoles = tantri.cli.file_importer.read_dipoles_json_file(dipoles_file)
	dots = tantri.cli.file_importer.read_dots_json_file(dots_file)

	if measurement_type == POTENTIAL:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.ELECTRIC_POTENTIAL
		value_name = "APSD_V"
	elif measurement_type == X_ELECTRIC_FIELD:
		measurement_enum = tantri.dipoles.DipoleMeasurementType.X_ELECTRIC_FIELD
		value_name = "APSD_Ex"

	_logger.debug(f"Using measurement {measurement_enum.name}")
	labels = [dot.label for dot in dots]
	with output_file.open("w") as out:
		if header_row:
			value_labels = ", ".join([f"{value_name}_{label}" for label in labels])
			out.write(f"f (Hz), {value_labels}\n")

		_logger.debug(
			f"Going to simulate {num_iterations} iterations with a delta t of {delta_t}"
		)

		_logger.debug(f"Got seed {time_series_rng_seed}")
		if time_series_rng_seed is None:
			time_series = tantri.dipoles.DipoleTimeSeries(
				dipoles, dots, measurement_enum, delta_t
			)
		else:
			rng = numpy.random.default_rng(time_series_rng_seed)
			time_series = tantri.dipoles.DipoleTimeSeries(
				dipoles, dots, measurement_enum, delta_t, rng
			)

		apsd = time_series.generate_average_apsd(
			num_series=num_time_series, num_time_series_points=num_iterations
		)

		values_list = zip(*[apsd.psd_dict[label] for label in labels])
		for freq, values in zip(apsd.freqs, values_list):
			value_string = ", ".join(str(v) for v in values)
			out.write(f"{freq}, {value_string}\n")
	if binned_output_file is not None:
		with binned_output_file.open("w") as out:
			if header_row:
				value_labels = ["mean bin f (Hz)"]
				for label in labels:
					value_labels.append(f"{value_name}_{label}_mean")
					value_labels.append(f"{value_name}_{label}_stdev")
				value_labels_text = ", ".join(value_labels)
				out.write(value_labels_text + "\n")
			binned = tantri.binning.bin_lists(
				apsd.freqs,
				apsd.psd_dict,
				tantri.binning.BinConfig(
					True, bin_width=bin_widths, bin_min=1e-6, min_points_required=2
				),
			)
			for bin_result in binned:
				summary = bin_result.summary_point()
				out_list = [str(summary.mean_x)]
				for label in labels:
					out_list.append(str(summary.summary_values[label].mean_y))
					out_list.append(str(summary.summary_values[label].stdev_y))
				out_string = ", ".join(out_list) + "\n"
				out.write(out_string)


@cli.command()
@click.argument(
	"generation_config",
	type=click.Path(exists=True, path_type=pathlib.Path),
)
@click.argument(
	"output_file",
	type=click.Path(path_type=pathlib.Path),
)
@click.option(
	"--override-rng-seed", type=int, help="Seed to override the generation config spec."
)
def generate_dipoles(generation_config, output_file, override_rng_seed):
	_generate_dipoles(generation_config, output_file, override_rng_seed)


def _generate_dipoles(generation_config, output_file, override_rng_seed):
	"""Generate random dipoles as described by GENERATION_CONFIG and output to OUTPUT_FILE.

	GENERATION_CONFIG should be a JSON file that matches the appropriate spec, and OUTPUT_FILE will contain JSON formatted contents.
	OUTPUT_FILE will be overwritten, if it exists.

	If the --override-rng-seed is set, it's better to keep logs of the generation!
	"""
	_logger.debug(
		f"generate_dipoles was called, with config file {click.format_filename(generation_config)}"
	)
	_logger.debug(f"override_rng_seed: [{override_rng_seed}]")

	with open(generation_config, "r") as config_file:
		data = json.load(config_file)
	config = tantri.dipoles.DipoleGenerationConfig(**data)

	override_rng = None
	if override_rng_seed is not None:
		_logger.info(f"Overriding the rng with a new one with seed {override_rng_seed}")
		override_rng = numpy.random.default_rng(override_rng_seed)
	_logger.debug(f"generating dipoles with config {config}...")
	generated = tantri.dipoles.make_dipoles(config, override_rng)

	with output_file.open("w") as out:
		out.write(
			json.dumps(
				[g.as_dict() for g in generated],
				cls=tantri.cli.input_files.write_dipoles.NumpyEncoder,
			)
		)
