from typing import Callable, List, Tuple
from time import sleep

type Row = Tuple[float, float, float, float]
type Matrix = Tuple[Row, Row, Row]
type Results = Tuple[float, float, float]
type Error = Tuple[float, float, float]

def main():
    print(
        "# Método Gauss-Seidel para sistemas de ecuaciones que forman" +
        "una matriz diagonalmente dominante. #" +
        "\nPara introducir las ecuaciones, " +
        "ingrese los índices separados por espacios."
    )
    toRow: Callable[[List[str]], Row] = \
        lambda x: (float(x[0]), float(x[1]), float(x[2]), float(x[3]))
    row_1 = toRow(input("Inserte los índices de la ecuación 1: ").split(" "))
    row_2 = toRow(input("Inserte los índices de la ecuación 2: ").split(" "))
    row_3 = toRow(input("Inserte los índices de la ecuación 3: ").split(" "))
    m = (row_1, row_2, row_3)
    print("Su matriz:",
        "\n[", m[0][0], m[0][1], m[0][2], "|", m[0][3], "]",
        "\n[", m[1][0], m[1][1], m[1][2], "|", m[1][3], "]",
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
    current = (0, 0, 0)
    i = 1
    while True:
        previous = current
        current = approximate(current)
        error = getError(current, previous)
        print(f"${i}: "
            f"Previous: (${previous[0]:.4f}, ${previous[1]:.4f}, ${previous[2]:.4f})"
            f"Current: (${current[0]:.4f}, ${current[1]:.4f}, ${current[2]:.4f})" 
            f"Error: (${error[0]:.4f}, ${error[1]:.4f}, ${error[2]:.4f})"
        )
        sleep(1)
        i += 1
        if withinError(expectedError, error): break
    return current

def mkApproximate(m: Matrix) -> Callable[[Results], Results]:
    def approximate(x: Results):
        x_1 = (m[0][3] - m[0][1]*x[1] - m[0][2]*x[2]) / m[0][0]
        x_2 = (m[1][3] - m[1][0]*x_1  - m[1][2]*x[2]) / m[1][1]
        x_3 = (m[2][3] - m[2][0]*x_1  - m[2][1]*x_2 ) / m[2][2]
        return (x_1, x_2, x_3)
    return approximate

def getError(current_iter: Results, prev_iter: Results) -> Error:
    return (
        abs((current_iter[0] - prev_iter[0]) / current_iter[0]) * 100,
        abs((current_iter[1] - prev_iter[1]) / current_iter[1]) * 100,
        abs((current_iter[2] - prev_iter[2]) / current_iter[2]) * 100)

def withinError(expectedError: float, error: Error) -> bool:
    return error[0] <= expectedError and \
           error[1] <= expectedError and \
           error[2] <= expectedError

def diagonallyDominant(m: Matrix) -> bool:
    return m[0][0] > m[0][1] and m[0][0] > m[0][2] and \
           m[1][1] > m[1][0] and m[1][1] > m[1][2] and \
           m[2][2] > m[2][0] and m[2][2] > m[2][1]

if(__name__ == "__main__"):
    main()