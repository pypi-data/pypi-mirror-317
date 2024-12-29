import math

def check_connection():
    return "checking passed successfully"

class Fraction:
    def __init__(self, numerator, denominator, simplify=True, separator='/'):
        self.numerator = numerator
        self.denominator = denominator
        self.simplify = simplify
        self.separator = separator
        self.__reduction()

    def __reduction(self):
        if self.simplify:
            a = math.gcd(self.numerator, self.denominator)
            self.numerator //= a
            self.denominator //= a
        return self.numerator, self.denominator

    def out(self):
        print(str(self.numerator) + self.separator + str(self.denominator))

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    def __repr__(self):
        return f"Fraction('{self.numerator}/{self.denominator}')"

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __add__(self, other):
        denominator = self.denominator * other.denominator
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        return Fraction(numerator, denominator)

    def __sub__(self, other):
        denominator = self.denominator * other.denominator
        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        return Fraction(numerator, denominator)

    def __iadd__(self, other):
        common_denominator = self.denominator * other.denominator
        self.numerator = self.numerator * other.denominator + other.numerator * self.denominator
        self.denominator = common_denominator
        self.__reduction()
        return self

    def __isub__(self, other):
        common_denominator = self.denominator * other.denominator
        self.numerator = self.numerator * other.denominator - other.numerator * self.denominator
        self.denominator = common_denominator
        self.__reduction()
        return self

    def __mul__(self, other):
        den = self.denominator * other.denominator
        num = self.numerator * other.numerator
        return Fraction(num, den)

    def __imul__(self, other):
        self.denominator *= other.denominator
        self.numerator *= other.numerator
        self.__reduction()
        return self

    def get_denominator(self):
        return self.denominator

    def get_numerator(self):
        return self.numerator

    def __truediv__(self, other):
        num = self.numerator * other.denominator
        den = self.denominator * other.numerator
        return Fraction(num, den)

    def reverse(self):
        return Fraction(self.denominator, self.numerator)

    def __itruediv__(self, other):
        self.numerator *= other.denominator
        self.denominator *= other.numerator
        self.__reduction()
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)