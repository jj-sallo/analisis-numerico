from typing import Callable, List, Iterable
from time import sleep
from functools import reduce
from operator import add
from copy import deepcopy

type Row = List[float]
type Matrix = List[Row]
type Results = List[float]
type Error = List[float]

class ParseError:
    def __init__(self, message: str):
        self.message = message

def main():
    print("# Método Gauss-Seidel para sistemas de ecuaciones"
          " que forman una matriz diagonalmente dominante. #")
    matrix = parseMatrix()
    if isinstance(matrix, ParseError): return print(matrix.message)
    printMatrix(matrix)
    expectedError = float(input("Ingrese el error esperado: "))
    result = gaussSeidel(expectedError, matrix)
    print(f"Resultado: {truncated(result)}")
    printEqualities(matrix, result)

def gaussSeidel(expectedError: float, matrix: Matrix) -> Results:
    approximate = mkApproximate(matrix)
    current: Results = [0] * (len(matrix[0]) - 1)
    i = 1
    while True:
        previous = current
        current = approximate(previous)
        error = getError(current, previous)
        print(f"Iteración {i}:"
            f"\n\tPrevio: {truncated(previous)}"
            f"\n\tActual: {truncated(current)} "
            f"\n\tError:  {truncated(error)}"
        )
        sleep(0.8)
        i += 1
        if withinError(expectedError, error): break
    return current

def mkApproximate(m: Matrix) -> Callable[[Results], Results]:
    def approximate(x: Results):
        r: Results = deepcopy(x)
        for i in range(len(m)):
            *c, d = m[i]
            min = [c[j] * r[j] for j in range(len(c)) if j != i]
            r[i] = (d - sum(min, 0)) / m[i][i]
        return r
    return approximate

def getError(current: Results, previous: Results) -> Error:
    return [
        abs((current[i] - previous[i]) / current[i]) * 100
        for i in range(len(current))
    ]

# Returns true if all obtained error rates are within the expected error rate
def withinError(expectedError: float, error: Error) -> bool:
    return allTrue(lambda e: e <= expectedError, error)

# Returns true if the given condition is true for all elements
def allTrue[T](cond: Callable[[T], bool], it: Iterable[T]) -> bool: 
    return reduce(lambda p, c: p and cond(c), it, True)

# Returns the given list without the i-th element
# Non-mutating
def without[T](l: List[T], i: int) -> List[T]:
    return [l[j] for j in range(len(l)) if j != i]

def parseMatrix() -> Matrix | ParseError:
    length = 0
    matrix: Matrix = []
    i = 0
    print(f"Inserte los índices de la ecuación dada o END para terminar.")
    while(True):
        strArr = input(f"eq {i + 1}: ").split(" ")
        if strArr[0] == "END": return matrix
        if i == 0: length = len(strArr)
        elif len(strArr) != length: return ParseError("Se ingresaron matrices de distinta longitud")
        # TODO: This doesn't check if the given coefficient is 0
        try: c = [float(c_ij) for c_ij in strArr]
        except: return ParseError("Se ingresó un valor no-numérico")
        if c[i] < sum(without(c[:-1], i), 0): return ParseError("La matriz no es diagonalmente dominante")
        matrix.append(c)
        i += 1

def printMatrix(m: Matrix):
    message = "Su matriz:"
    for row in m:
        *rest, last = row
        message += f"\n[ " + " ".join([f"{c} " for c in rest]) + f" | {last} ]"
    print(message)

def truncated(l: List[float]):
    *rest, last = l
    return "(" + " ".join([f"{x:.4f}," for x in rest]) + f" {last})"
    
def printEqualities(matrix: Matrix, results: Results):
    message = "Verificación:"
    for i in range(len(matrix)):
        l = reduce(add, [x*y for (x, y) in zip(matrix[i][:-1], results)], 0)
        r = matrix[i][-1]
        message += f"\nEq {i + 1}: {l:.4f} = {r:.4f}"
    print(message)

if(__name__ == "__main__"):
    main()
