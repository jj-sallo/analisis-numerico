from typing import Callable
# importamos math para usarlo dentro de eval()
import math

def main():
    fn = parsefn()
    if type(fn) == str: return print(f'ERROR: {fn}')
    e = float(input("% de error: "))
    r = pfijo(0, e, fn)
    print(r)

def pfijo(x: float, e: float, fn: Callable[[float], float]):
    i = 0
    curr = x
    while True:
        prev = curr
        curr = fn(prev)
        print(curr, err(prev, curr))
        if err(prev, curr) <= e:
            return curr

def err(prev: float, curr: float) -> float:
    return abs((curr - prev) / curr) * 100

def parsefn() -> Callable[[float], float] | str:
    print(
      "Ingrese la función g(x) que proviene"
      "\ndel despeje x_{i+1}=g(x_i)"
      "\nNota: la variable debe de ser x y estar"
      "\nen notación de Python"
      "\ne.g. g(x) = x**2 + 2*x + 1"
      "\n     g(x) = math.e(-x)"
    )
    s = input("g_(x) = ")
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
