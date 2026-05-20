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
    val = input_queue.get()
    if(val is None):
        return 
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
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()

    q1.put(values[0])
    q1.put(values[1])
    q1.put(values[2])
    q1.put(values[3])

    w1 = multiprocessing.Process(target=_worker_factorial,args=(q1,q2))
    w2 = multiprocessing.Process(target=_worker_factorial,args=(q1,q2))
    w3 = multiprocessing.Process(target=_worker_factorial,args=(q1,q2))
    w4 = multiprocessing.Process(target=_worker_factorial,args=(q1,q2))

    w1.start()
    w2.start()
    w3.start()
    w4.start()

    r1 = q2.get()
    r2 = q2.get()
    r3 = q2.get()
    r4 = q2.get()

    res = {
        r1[0]:r1[1],
        r2[0]:r2[1],
        r3[0]:r3[1],
        r4[0]:r4[1],
    }

    w1.join()
    w2.join()
    w3.join()
    w4.join()

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
    with ProcessPoolExecutor(max_workers=4) as w:
        res1 = w.submit(_worker_factorial,values[0])
        res2 = w.submit(_worker_factorial,values[1])
        res3 = w.submit(_worker_factorial,values[2])
        res4 = w.submit(_worker_factorial,values[3])

    r1 = res1.result()
    r2 = res2.result()
    r3 = res3.result()
    r4 = res4.result()



    rez = {
    r1[0]:r1[1],
    r2[0]:r2[1],
    r3[0]:r3[1],
    r4[0]:r4[1],
    }

    res1.join()
    res2.join()
    res3.join()
    res4.join()

    return rez
