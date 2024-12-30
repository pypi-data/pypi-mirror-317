from .eratosthenes_generator import EratosthenesGenerator
from .prime_generator import PrimeGenerator


def get_generator(name: str = "Eratosthenes") -> PrimeGenerator | None:
    """
    Creates and returns a prime generator.
    :param name: The name of a type of prime generator.
    Currently only 'Eratosthenes' is accepted.
    :return: A generator of the specified type, or None if an unknown
    type was specified.
    """

    if not name:
        raise ValueError("Prime generator type cannot be specified as 'None'")

    if name.casefold() == "eratosthenes":
        return EratosthenesGenerator()

    return None
