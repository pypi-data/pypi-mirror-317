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

        if kwargs and kwargs.get("clear_cache", False):
            self._primes.clear()

    def __str__(self) -> str:
        return f"Fast search: {self.fast_search}, {len(self._primes)} primes, {self._primes}"

    def _next_prime(self, current_value) -> int:

        while True:
            is_prime = True
            current_value += 2 if current_value % 2 else 1
            for factor in self._primes:
                if not current_value % factor:
                    is_prime = False
                    break

                if factor * factor > current_value:
                    break

            if is_prime:
                return current_value

    def primes(self) -> Iterator[int]:
        """
        Generate an endless series of prime numbers, starting with 2.

        :return: An iterator over the series of prime numbers.
        """

        if not self._primes:
            self._primes.append(2)

        prime_index = 0

        while True:
            if prime_index == len(self._primes):
                self._primes.append(self._next_prime(self._primes[-1]))

            yield self._primes[prime_index]
            prime_index += 1

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

        if not self.fast_search or minimum <= 2 or not self._primes:
            for p in self.primes():
                # Return if in range
                if p > maximum:
                    break

                if p >= minimum:
                    yield p

        else:

            # Under development

            while minimum > self._primes[-1]:
                self._primes.append(self._next_prime(self._primes[-1]))

            if minimum <= self._primes[-1]:
                # The minimum number is in the range of the _primes collection.
                # Find the next prime, if this isn't it.

                prime_index = bisect_left(self._primes, minimum)

                while self._primes[prime_index] <= maximum:
                    if prime_index < len(self._primes):
                        yield self._primes[prime_index]
                        prime_index += 1
                    else:
                        self._primes.append(self._next_prime(self._primes[-1]))
                        if (prime_value := self._primes[prime_index]) <= maximum:
                            yield self._primes[prime_index]
                            prime_index += 1

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

            if factor * factor >= candidate:
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
