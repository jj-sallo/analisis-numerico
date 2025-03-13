from functools import cache
from math import isclose
from math import factorial as fact

# Para cualquier conjunto de tamaño n
#   y₀, y₁, y₂, ..., yᵢ, ..., yₙ
# el operador de diferencia Δᵏaᵢ se define como
#
#        | 1                 si k = 0
# Δᵏyᵢ = | yᵢ₊₁ - yᵢ         si k = 1
#        | Δᵏ⁻¹yᵢ₊₁ + Δᵏ⁻¹yᵢ si k > 1
#
# donde n ≥ 1
#       0 ≤ k < n
#       0 ≤ i < n - k
#       n, i, k ∈ ℕ
def mkDifference(ys: list[float]):
    @cache
    def difference(k: int, i: int) -> float:
        if   k == 0: return ys[0]
        elif k == 1: return ys[i + 1] - ys[i]
        else:        return difference(k - 1, i + 1) - difference(k - 1, i)
    return difference

# Para cualquier conjunto de tamaño n
#   x₀, x₁, ..., xⱼ, ..., xₙ
# la base de Newton se define de la siguiente manera
#
# nⱼ(x) = | 1                    si j = 0
#         | Πʲ⁻¹ᵢ₌₀ (x - xᵢ)     si j > 0
#
# Esto se puede reescribir de forma recursiva como
#
# nⱼ(x) = | 1                     si j = 0
#         | (x - xⱼ₋₁) * nⱼ₋₁(x)  si j > 0
#
# donde n ≥ 0
#       0 ≤ j < n
#       n, j ∈ ℕ
def mkNewtonBasis(xs: list[float]):
    @cache
    def newtonBasis(x: float, j: int) -> float:
        if j == 0: return 1
        else:      return (x - xs[j - 1]) * newtonBasis(x, j - 1)
    return newtonBasis

# Dado un conjunto de puntos
#   (x₀, y₀), (x₁, y₁), ..., (xₙ, yₙ), (xₙ₊₁, yₙ₊₁)
# El polinomio de Newton esta dado por la formula:
#   Pₙ(x) = Σⁿᵢ₌₀  Δᵏyᵢ * nⱼ(x) / (i! * hⁱ)
# donde n ≥ 1
#       n ∈ ℕ
def mkNewtonPolynomial(xs: list[float], ys: list[float]):
    n = len(xs)
    spacing = abs(xs[0] - xs[1])
    difference = mkDifference(ys)
    basis = mkNewtonBasis(xs)
    def newtonPolynomial(x: float) -> float:
        def term(i: int) -> float:
            return difference(i, 0) * basis(x, i) / (fact(i) * spacing ** i)
        return sum(term(i) for i in range(n))
    return newtonPolynomial

def sameSpacingBetween(xs: list[float]) -> bool:
    n = len(xs)
    spacing = abs(xs[0] - xs[1])
    haveSameSpacing = [isclose(abs(xs[i] - xs[i + 1]), spacing) for i in range(1, n - 1)]
    return all(haveSameSpacing)

def parsePoints() -> tuple[list[float], list[float]]:
    i = 1
    xs: list[float] = []
    ys: list[float] = []
    print(
        "Ingrese los puntos a interpolar."
        "\nCada punto debe consistir en dos números separados por espacios."
    )
    while True:
        s = input(f"{i}: ").strip()
        if s == "END": return (xs, ys)
        try:
            first, second = s.split(" ")
            xs.append(float(first))
            ys.append(float(second))
            i += 1
        except ValueError:
            print("Se insertaron valores inválidos, intente de nuevo.")

def parseX() -> float:
    print("Ingrese el valor de x a aproximar")
    while True:
        try:    return float(input("x: "))
        except: print("El valor ingresado no es válido, intente de nuevo.")

def main():
    xs, ys = parsePoints()
    if not sameSpacingBetween(xs):
        print("Los valores de x tienen que tener el mismo espaciado entre ellos")
        return
    if len(xs) == 0:
        print("No se ingresaron puntos")
        return
    x = parseX()
    newtonPolynomial = mkNewtonPolynomial(xs, ys)
    y = newtonPolynomial(x)
    print(f"Valor obtenido: {y}")
    print(f"Nuevo punto: ({x}, {y:.4f})")

if __name__ == "__main__":
    main()
