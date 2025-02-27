from typing import Callable
# importamos math para usarlo dentro de eval()
import math

def main():
    fn = parsefn()
    if type(fn) == str: return print(f'ERROR: {fn}')
    e = float(input("% de error: "))
    # TODO: Puede que se quiera proveer la x inicial
    # en ese caso hay que añadir otro input
    r = pfijo(0, e, fn)
    print("Raiz encontrada:", r)
    print(f"f({r}) =", fn(r))

def pfijo(x: float, e: float, fn: Callable[[float], float]):
    i = 0
    curr = x
    while True:
        prev = curr
        # el + x viene del despeje f(x) + x - x = 0
        curr = fn(prev) + prev
        print(curr, err(prev, curr))
        # TODO: Si en algún momento e_{i+1} >= e_i
        # el algoritmo diverge y la función no tiene punto fijo
        if err(prev, curr) <= e:
            return curr

def err(prev: float, curr: float) -> float:
    return abs((curr - prev) / curr) * 100

def parsefn() -> Callable[[float], float] | str:
    print(
      "Ingrese la función f(x)"
      "\nNota: la variable debe de ser x y estar"
      "\nen notación de Python"
      "\ne.g. f(x) = x**2 + 2*x + 1"
      "\n     f(x) = math.e**(-x) - x"
    )
    s = input("f(x) = ")
    # la lambda encapsula el valor de x dentro de su scope
    fn = lambda x: eval(s)
    # la función tiene que aceptar un valor flotante
    # y retornar otro valor flotante
    def isinvalid(x: float):
        try: float(fn(x)); return False
        except: return True
    # es posible que la función sea válida pero contenga
    # una asíntota en uno de los valores de prueba
    # por lo que probamos 5 distintos
    if not all(isinvalid(x) for x in range(5)):
        return fn
    return "La función ingresada debe aceptar y retornar valores numericos flotantes"

if __name__ == "__main__":
    main()
