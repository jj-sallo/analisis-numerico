from typing import Callable
from time import sleep

type Row = tuple[float, float, float, float]
type Matrix = tuple[Row, Row, Row]
type Results = tuple[float, float, float]
type Error = tuple[float, float, float]

def main():
    print(
        "# Método Gauss-Seidel para sistemas de ecuaciones que forman" +
        "una matriz diagonalmente dominante. #" +
        "\nPara introducir las ecuaciones, " +
        "ingrese los índices separados por espacios."
    )
    # (string, string, string) -> (float, float, float)
    toRow = lambda x: (float(x[0]), float(x[1]), float(x[2]), float(x[3]))
    row_1 = toRow(input("Inserte los índices de la ecuación 1: ").split(" "))
    row_2 = toRow(input("Inserte los índices de la ecuación 2: ").split(" "))
    row_3 = toRow(input("Inserte los índices de la ecuación 3: ").split(" "))
    m = (row_1, row_2, row_3)
    print("Su matriz:",
        "\n[", m[0][0], m[0][1], m[0][2], "|", m[0][3], "]",
        "\n[", m[1][0], m[1][1], m[1][2], "|", m[1][3], "]"
        "\n[", m[2][0], m[2][1], m[2][2], "|", m[2][3], "]")
    if not diagonallyDominant(m):
        print("La matriz ingresada no es diagonalmente dominante")
        return
    expectedError = float(input("Ingrese el error esperado: "))
    result = gaussSeidel(expectedError, m)
    print("Resultado: ",
        "\nx_1: ", result[0],
        "\nx_2: ", result[1],
        "\nx_3: ", result[2])
    print(
        "eq1: ",   m[0][0]*result[0] + m[0][1]*result[1] + m[0][2]*result[2], "=", m[0][3],
        "\neq2: ", m[1][0]*result[0] + m[1][1]*result[1] + m[1][2]*result[2], "=", m[1][3],
        "\neq3: ", m[2][0]*result[0] + m[2][1]*result[1] + m[2][2]*result[2], "=", m[2][3])

def gaussSeidel(expectedError: float, m: Matrix) -> Results:
    approximate = mkApproximate(m)
    previous = approximate((0, 0, 0))
    current = approximate(previous)
    error = getError(previous, current)
    # El código descomentado te permite ver las iteraciones paso a paso
    # print("0: ", previous, current, error)
    # i = 0
    while not withinError(expectedError, error):
        previous = current
        current = approximate(current)
        error = getError(previous, current)
        # i += 1
        # print(str(i) + ": ", previous, current, error)
        # sleep(1)
    return current

def mkApproximate(m: Matrix) -> Callable[[tuple[float, float, float]], float]:
    def approximate(x: Results):
        x_1 = (m[0][3] - m[0][1]*x[1] - m[0][2]*x[2]) / m[0][0]
        x_2 = (m[1][3] - m[1][0]*x_1  - m[1][2]*x[2]) / m[1][1]
        x_3 = (m[2][3] - m[2][0]*x_1  - m[2][1]*x_2 ) / m[2][2]
        return (x_1, x_2, x_3)
    return approximate

def getError(current_iter: Results, prev_iter: Results) -> Error:
    e_1 = abs((current_iter[0] - prev_iter[0]) / current_iter[0]) * 100
    e_2 = abs((current_iter[1] - prev_iter[1]) / current_iter[1]) * 100
    e_3 = abs((current_iter[2] - prev_iter[2]) / current_iter[2]) * 100
    return (e_1, e_2, e_3)

def withinError(expectedError: float, error: float) -> bool:
    isWithinExpected_1 = error[0] < expectedError
    isWithinExpected_2 = error[1] < expectedError
    isWithinExpected_3 = error[2] < expectedError
    return isWithinExpected_1 and isWithinExpected_2 and isWithinExpected_3

def diagonallyDominant(m: Matrix) -> bool:
    isDominant_1 = m[0][0] > m[0][1] and m[0][0] > m[0][2]
    isDominant_2 = m[1][1] > m[1][0] and m[1][1] > m[1][2]
    isDominant_3 = m[2][2] > m[2][0] and m[2][2] > m[2][1]
    return isDominant_1 and isDominant_2 and isDominant_3

if(__name__ == "__main__"):
    main()