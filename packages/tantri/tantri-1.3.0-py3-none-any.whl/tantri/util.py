import typing

A = typing.TypeVar("A")
B = typing.TypeVar("B")


def dict_reduce(
	list_of_dicts: typing.Sequence[typing.Dict[str, A]],
	func: typing.Callable[[typing.Sequence[A]], B],
) -> typing.Dict[str, B]:
	"""
	Reduce over list of dicts with function that can coalesce list of dict values.
	Assumes the keys in the first dictionary are the same as the keys for every other passed in dictionary.
	"""
	keys = list_of_dicts[0].keys()

	collated = {}
	for key in keys:
		collated[key] = [dct[key] for dct in list_of_dicts]

	return {k: func(v) for k, v in collated.items()}
