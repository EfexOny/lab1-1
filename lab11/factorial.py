"""
Calcul factorial paralel folosind multiprocessing.

Tema 1: calculează n! simultan pentru mai multe valori,
folosind atât multiprocessing.Queue + Process cât și ProcessPoolExecutor.
"""

import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import math


# TODO: Implementează funcția factorial
def factorial(n: int) -> int:
    """Calculează n! (factorial).

    Args:
        n: Numărul pentru care se calculează factorialul. Trebuie să fie >= 0.

    Returns:
        n! ca întreg.

    Raises:
        ValueError: Dacă n este negativ.

    Exemple:
        factorial(0) == 1
        factorial(1) == 1
        factorial(5) == 120
    """
    if(n < 0 ):
        raise ValueError("n este negativ")
    if(n==0 or n==1):
        return 1
    return n*factorial(n-1)


def _worker_factorial(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue) -> None:
    """Funcție worker pentru procesul multiprocessing.

    Citește valori din input_queue, calculează factorialul și trimite
    rezultatele în output_queue sub forma (n, factorial(n)).

    Se oprește când primește None din input_queue.

    Args:
        input_queue: Coada de unde se citesc valorile n.
        output_queue: Coada unde se trimit perechile (n, rezultat).
    """
    # TODO: Implementează bucla worker
    while True:
        val = input_queue.get()
        if(val is None):
            break
        rez = math.factorial(val)
        output_queue.put((val,rez))


# TODO: Implementează funcția parallel_factorial_multiprocessing
def parallel_factorial_multiprocessing(values: list[int]) -> dict[int, int]:
    """Calculează factorialul pentru mai multe valori în paralel.

    Folosește 4 procese worker cu multiprocessing.Queue și multiprocessing.Process.

    Args:
        values: Lista valorilor pentru care se calculează factorialul.

    Returns:
        Dict {n: factorial(n)} pentru toate valorile din lista.

    Exemplu:
        result = parallel_factorial_multiprocessing([5, 6, 7, 8])
        # {5: 120, 6: 720, 7: 5040, 8: 40320}
    """

    if not values:
        return {}

    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()

    for valori in values:
        q1.put(valori)

    for _ in range(4):
        q1.put(None)

    workers = []

    for _ in range(4):
        w = multiprocessing.Process(target=_worker_factorial,args=(q1,q2))
        w.start()
        workers.append(w)

    res = {}
    for _ in range(len(values)):
        v1, v2 = q2.get()
        res[v1] = v2

    for wor in workers:
        wor.join()

    return res;

# TODO: Implementează funcția parallel_factorial_futures
def parallel_factorial_futures(values: list[int]) -> dict[int, int]:
    """Calculează factorialul pentru mai multe valori în paralel.

    Folosește concurrent.futures.ProcessPoolExecutor cu max_workers=4.

    Args:
        values: Lista valorilor pentru care se calculează factorialul.

    Returns:
        Dict {n: factorial(n)} pentru toate valorile din lista.

    Exemplu:
        result = parallel_factorial_futures([5, 6, 7, 8])
        # {5: 120, 6: 720, 7: 5040, 8: 40320}
    """

    if not values:
        return {}
    
    rez ={}
    with ProcessPoolExecutor(max_workers=4) as w:
        rezlucr = []

        for val in values:
            peter = w.submit(factorial,val)
            rezlucr.append((val,peter))
        
        for v1 ,v2 in rezlucr:
            rez[v1]= v2.result()


    return rez
