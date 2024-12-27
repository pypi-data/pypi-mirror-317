# PrimeGenerators - Prime Number Generation and Utilities

## Command Line Interface

The prime generator can be run from the command line. The output can be piped or redirected to a separate file or
process.

```bash
usage: primegenerators [-h] [-c COUNT] [-f {text,json}]

Random number generator and analyzer.

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        The number of values to generate
  -f {text,json}, --format {text,json}
                        The format of the output
```

## Python Library

The prime generator should be created using the factory method, e.g.:

```python
from primegenerators import get_generator

# Details elided

generator = get_generator("eratosthenes")

for index, prime in enumerate(generator.primes()):
    sys.stdout.write(str(prime))

    # Further processing and exit conditions
```

### Member Functions

```python
primes() -> Iterator[int]
```

Generate an endless series of prime numbers, starting with 2.

Returns an iterator over the series of prime numbers.

```python
primes_range(minimum: int, maximum: int) -> Iterator[int]
```

Return an iterator over the series of prime numbers between minimum
and maximum inclusive.

**minimum:** The minimum number in the series. If this number is not prime,
the first number in the series is the first prime higher than this number.

**maximum:** The maximum number in the series. If this number is not prime,
the last number in the series is the last prime lower than this number.

```python
is_prime(number: int) -> bool
```

Determine whether a given number is prime or not.

**number:** The number to be checked for prime-ness

Returns `True` if the candidate number is prime, otherwise `False`

```python
prime_factors(self, number: int) -> Counter
```

Calculate the prime factors of a number.

**number:** The number to be factorized

Returns a `collections.Counter` object containing the prime factors of `number`

## Download Statistics

[![Downloads](https://static.pepy.tech/badge/primegenerators)](https://pepy.tech/project/primegenerators)
[![Downloads](https://static.pepy.tech/badge/primegenerators/month)](https://pepy.tech/project/primegenerators)
[![Downloads](https://static.pepy.tech/badge/primegenerators/week)](https://pepy.tech/project/primegenerators)
