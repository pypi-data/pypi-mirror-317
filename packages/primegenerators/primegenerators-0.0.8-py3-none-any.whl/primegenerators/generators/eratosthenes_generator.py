from bisect import bisect_left
from collections import Counter
from typing import Iterator

from primegenerators.algorithms import binary_search
from .prime_generator import PrimeGenerator


# noinspection SpellCheckingInspection
class EratosthenesGenerator(PrimeGenerator):
    """
    Prime number generator using the Sieve of Eratosthenes
    """

    _primes = []

    def __init__(self, *args, **kwargs):
        """
        Create a new EratosthenesGenerator
        :param args: Do not use these
        :param kwargs: Do not use these
        """
        self.fast_search = kwargs.get("fast_search", False) if kwargs else False

    def _uncached_primes(self) -> Iterator[int]:
        """
        Generate an infinite series of prime numbers, starting from the first
        prime not in the cache.
        :return:
        """
        current_value = 1 if not self._primes else self._primes[-1]
        while True:
            is_prime = True

            current_value += 2

            for factor in self._primes:
                if not current_value % factor:
                    is_prime = False
                    break

                if factor * factor > current_value:
                    break

            if is_prime:
                if not self._primes or self._primes[-1] < current_value:
                    self._primes.append(current_value)

                yield current_value

    def primes(self) -> Iterator[int]:
        """
        Generate an endless series of prime numbers, starting with 2.

        :return: An iterator over the series of prime numbers.
        """

        yield 2

        # Run through the cache
        for prime in self._primes:
            yield prime

        yield from self._uncached_primes()

    def primes_range(self, minimum: int, maximum: int) -> Iterator[int]:
        """
        Return an iterator over the series of prime numbers between minimum
        and maximum inclusive.

        :param minimum: The smallest possible value in the range to be returned.
        If this is not prime, then the next prime greater than this will be returned.
        :param maximum: The largest possible value in the range to be returned.
        If this is not prime, then the last prime smaller than this will be returned.
        :return:
        """

        if not self.fast_search:
            for p in self.primes():
                # Return if in range
                if p > maximum:
                    break

                if p >= minimum:
                    yield p

        # Under development
        if minimum <= 2:
            # All primes
            for p in self.primes():
                if p <= maximum:
                    yield p
                else:
                    return

        if minimum <= self._primes[-1]:
            # The minimum number is in the range of the _primes collection.
            # Find the next prime, if this isn't it.

            index = bisect_left(self._primes, minimum)

            for p in self._primes[index:]:
                if p <= maximum:
                    yield p
                else:
                    return

        # Here, either minimum was in the cache and we've run to the
        # end, or it was bigger than the biggest cache value.
        # Either way, we need to add numbers to the cache and return
        # them as appropriate.

        for p in self._uncached_primes():
            # Return if in range
            if p > maximum:
                break

            if p >= minimum:
                yield p

    def is_prime(self, candidate: int) -> bool:
        """
        Determine whether a given number is prime or not.

        :param candidate: The number to be checked for prime-ness
        :return: True if the candidate number is prime, otherwise False
        """

        if candidate < 2 or candidate % 2 == 0:
            return False

        # If the number is in the cache, it must be prime
        # if candidate in self._primes:
        if binary_search(self._primes, candidate) >= 0:
            return True

        for factor in self.primes():
            if candidate % factor == 0:
                return candidate == factor

            if factor * factor > candidate:
                break

        return True

    def prime_factors(self, number: int) -> Counter:
        """
        Calculate the prime factors of a number.

        :param number: The number to be factorized
        :return: A Counter object containing the prime factors of number
        """

        factors = []

        for factor in self.primes():
            while number % factor == 0:
                factors.append(factor)
                number //= factor
            if number == 1:
                break

        return Counter(factors)
