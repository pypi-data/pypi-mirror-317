"""test the binomial distribution against the scipy library"""
import random
import scipy
from utility import compare_distributions
import promethium
import time

def test_binomial_pmf():
    expected_function = scipy.stats.binom.pmf
    observed_function = promethium.binomial.pmf
    for _ in range(100):
        x = random.randint(0, 500)
        n = random.randint(0, 500) + x
        p = random.uniform(0, 1.0)
        compare_distributions(expected_function, observed_function, (x, n, p))

def test_binomial_cdf():
    expected_function = scipy.stats.binom.cdf
    observed_function = promethium.binomial.cdf
    for _ in range(100):
        x = random.randint(0, 500)
        n = random.randint(0, 500) + x
        p = random.uniform(0, 1.0)
        compare_distributions(expected_function, observed_function, (x, n, p))

def test_binomial_ppf():
    start_time = time.time()

    expected_function = scipy.stats.binom.ppf
    observed_function = promethium.binomial.ppf
    for _ in range(100):
        y = random.uniform(0, 1.0)
        n = random.randint(0, 500)
        p = random.uniform(0, 1.0)
        compare_distributions(expected_function, observed_function, (y, n, p))

    end_time = time.time()

    print(end_time - start_time)

if __name__ == '__main__':
    test_binomial_pmf()
    test_binomial_cdf()
    test_binomial_ppf()
