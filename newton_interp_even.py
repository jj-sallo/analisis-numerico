from collections.abc import Iterable
from functools import cache
from operator import mul
from math import isclose
from math import factorial as fact

# Para cualquier conjunto y_1, y_2, ..., y_i, ..., y_n
# el operador de diferencia Δ^k a_i se define como
#
#           | 1                               si k = 0
# Δ^k a_i = | y_{i+1} - y_i                   si k = 1
#           | Δ^{k-1} y_{i+1} + Δ^{k-1} y_{i} si k > 1
#
# donde n >= 2
#       0 <= k < n - 1
#       0 <= i < n - k - 1
def mkDifference(ys: [float]):
    # Tenemos que crear esta función que retorna otra función
    # porque @cache sólo puede actuar sobre valores hasheables,
    # y las listas no son hasheables.

    n = len(ys)
    # @cache va a guardar los valores previamente calculados
    # tal que, si previamente calculamos delta(3, 0), ya no tenemos
    # que calcularlo de nuevo y nos ahorramos su cómputo
    @cache
    def difference(k: int, i: int) -> float:
        if   n < 2:
            raise ValueError("n debe ser mayor a 2")
        elif k < 0 or k > n - 1:
            raise ValueError("k debe estar en el rango 0 <= k < n - 1")
        elif i < 0 or i > n - k - 1:
            raise ValueError("i debe estar en el rango 0 <= i < n - k - 1")
        elif k == 0:
            return ys[0]
        elif k == 1:
            return ys[i + 1] - ys[i]
        else: # i > 0, k > 1
            return difference(k - 1, i + 1) - difference(k - 1, i)
    return difference

# Para cualquier conjunto x_0, x_1, ..., x_N,
# la base de Newton se define de la siguiente manera
#
# n_j(x) = | 1                           si j = 0
#          | Π^(j-1)_{i=0} (x - x_i)     si j > 0
#
# Esto se puede reescribir de forma recursiva como
#
# n_j(x) = | 1                           si j = 0
#          | (x - x_{j-1}) * n_{j-1}(x)  si j > 0
#
# donde N >= 2
#       j <= N
def mkNewtonBasis(xs: [float]):
    n = len(xs)
    @cache
    def newtonBasis(x: float, i: float) -> float:
        if   i < 0:  raise ValueError("i no puede ser menor a 0")
        elif i > n:  raise ValueError("i no puede ser mayor a n")
        elif i == 0: return 1
        else:        return (x - xs[i - 1]) * newtonBasis(x, i - 1)
    return newtonBasis

def mkNewtonPolynomial(xs: [float], ys: [float]):
    n = len(xs)
    spacing = abs(xs[0] - xs[1])
    haveSameSpacing = \
        [isclose(abs(xs[i] - xs[i + 1]), spacing) for i in range(1, n - 1)]
    if not all(haveSameSpacing):
        raise ValueError(
            "Los valores de x tienen que tener el mismo espaciado entre ellos"
        )
    difference = mkDifference(ys)
    basis = mkNewtonBasis(xs)
    def newtonPolynomial(x) -> float:
        def term(i: int) -> float:
            return difference(i, 0) * basis(x, i) / (fact(i) * spacing ** i)
        return sum(term(i) for i in range(n))
    return newtonPolynomial
