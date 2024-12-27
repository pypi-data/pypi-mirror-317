import argparse
import sys
from enum import Enum

from primegenerators import get_generator


class OutputFormat(Enum):
    TEXT = 1
    JSON = 2
    CSV = 3


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Random number generator and analyzer."
    )

    parser.add_argument(
        "-c", "--count", type=int, default=10, help="The number of values to generate"
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json"],
        default="text",
        help="The format of the output",
    )

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    output_format = OutputFormat[arguments.format.upper()]

    if output_format == OutputFormat.JSON:
        prefix = "["
        separator = ", "
        postfix = "]"
    else:
        prefix = ""
        separator = "\n"
        postfix = "\n"

    sys.stdout.write(prefix)

    generator = get_generator("eratosthenes")

    for prime in range(2, 5000000):
        if generator.is_prime(prime):
            # sys.stdout.write(str(prime))
            # sys.stdout.write(separator)
            pass

    if False:
        for index, prime in enumerate(generator.primes()):
            sys.stdout.write(str(prime))

            if index != arguments.count - 1:
                sys.stdout.write(separator)
            else:
                break

    sys.stdout.write(postfix)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
