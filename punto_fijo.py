from typing import Callable
# importamos math para usarlo dentro de eval()
import math

class DivergenceException(Exception): pass

def main():
    fn = parsefn()
    if type(fn) == str: return print(f'ERROR: {fn}')
    x = float(input("x_0: "))
    e = float(input("% de error: "))
    try:
        r = pfijo(x, e, fn)
        print("Raiz encontrada:", r)
        print(f"f({r:.4f}) =", fn(r))
    except DivergenceException:
        print("El algoritmo diverge con la función y el valor inicial dado")

def pfijo(x: float, e: float, fn: Callable[[float], float]):
    i = 0
    curr = fn(x) + x
    cerr = math.inf
    print(f"0: x = {curr:.4f} err = inf")
    while True:
        i += 1
        prev = curr # x_i
        curr = fn(prev) + prev # x_{i+1} -> fn(x_i) + x_i
        perr = cerr
        cerr = err(prev, curr)
        print(f"{i}: x = {curr:.4f} err = {cerr:.4f}")
        # Si en algún momento e_{i+1} >= e_i el algoritmo
        # diverge con f(x) y x_0
        if cerr >= perr:
            raise DivergenceException()
        if cerr <= e:
            return curr

def err(prev: float, curr: float) -> float:
    return abs((curr - prev) / curr) * 100

def parsefn() -> Callable[[float], float] | str:
    print(
      "Ingrese la función f(x)"
      "\nNota: la variable debe de ser x y estar"
      "\nen notación de Python"
      "\ne.g. f(x) = x**2 - 2*x + 1"
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
