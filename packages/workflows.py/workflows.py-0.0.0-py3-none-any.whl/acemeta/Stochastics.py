"""
Module for stochastics
"""

from random import randint

def binomialDF(n: int, k: int, p: float, mode: str = "exact") -> float:
    """
    Calculates a probability using the binomial distribution function

    #### Arguments
        n (int): Number of Bernoulli experiments performed
        k (int): Number of succesfull experiments
        p (float): The probability of success of a single experiment
        mode: "exact", "max", "min", "morethen" or "lessthen"

    #### Returns
        float: The requested probability
    """
    def factorial(n: int) -> int:
        out: int = 1
        for i in range(1, n + 1):
            out *= i
        return out
    def binominalC(n: int, k: int) -> float:
        return factorial(n) / (factorial(k) * factorial(n - k))
    def binominalD(n: int, k: int, p: float) -> float:
        return binominalC(n, k) * (p ** k) * ((1-p) ** (n - k))
    def bdf_max(n: int, k_max: int, p: float) -> float:
        out: float = 0
        for i in range(0, k_max + 1):
            out = out + binominalD(n, i, p)
        return out
    
    match mode:
        case "exact":
            return binominalD(n, k, p)
        case "max":
            out: float = 0
            for i in range(0, k + 1):
                out = out + binominalD(n, i, p)
            return out
        case "min":
            return 1 - bdf_max(n, k - 1, p)
        case "morethen":
            return 1 - bdf_max(n, k, p)
        case "lessthen":
            return bdf_max(n, k - 1, p)
        case _:
            raise SyntaxError("mode in binomialDF() must be one of \"exact\", \"max\", \"min\", \"morethen\" or \"lessthen\"") 