from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterator


class PrimeGenerator(ABC):
    """
    Prime number generator interface.
    """

    @abstractmethod
    def primes(self) -> Iterator[int]:
        """
        Generate an endless series of prime numbers, starting with 2.

        :return: An iterator over the series of prime numbers.
        """
        pass

    @abstractmethod
    def primes_range(self, minimum: int, maximum: int) -> Iterator[int]:
        """
        Return an iterator over the series of prime numbers between minimum
        and maximum inclusive.

        :param minimum: The minimum number in the series. If this number is not prime,
        the first number in the series is the first prime higher than this number.
        :param maximum: The maximum number in the series. If this number is not prime,
        the last number in the series is the last prime lower than this number.
        :return:
        """

        pass

    @abstractmethod
    def is_prime(self, number: int) -> bool:
        """
        Determine whether a given number is prime or not.
        :param number: The number to be checked for prime-ness
        :return: True if the candidate number is prime, otherwise False
        """
        pass

    def prime_factors(self, number: int) -> Counter:
        """
        Calculate the prime factors of a number.

        :param number: The number to be factorized
        :return: A Counter object containing the prime factors of number
        """

        pass
