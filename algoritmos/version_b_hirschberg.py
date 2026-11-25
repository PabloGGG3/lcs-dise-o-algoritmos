from __future__ import annotations
from array import array
from typing import Dict, Optional


def _fila_puntuaciones_directa(
    a: str,
    a_ini: int,
    a_fin: int,
    b: str,
    b_ini: int,
    b_fin: int,
    metricas: Optional[Dict[str, int]] = None,
) -> array:
    ancho = b_fin - b_ini
    anterior = array("I", [0]) * (ancho + 1)
    actual = array("I", [0]) * (ancho + 1)

    for idx_a in range(a_ini, a_fin):
        char_a = a[idx_a]
        actual[0] = 0
        for col in range(1, ancho + 1):
            if metricas is not None:
                metricas["celdas"] = metricas.get("celdas", 0) + 1
            if char_a == b[b_ini + col - 1]:
                actual[col] = anterior[col - 1] + 1
            else:
                arriba = anterior[col]
                izq = actual[col - 1]
                actual[col] = arriba if arriba >= izq else izq
        anterior, actual = actual, anterior

    return anterior


def _fila_puntuaciones_inversa(
    a: str,
    a_ini: int,
    a_fin: int,
    b: str,
    b_ini: int,
    b_fin: int,
    metricas: Optional[Dict[str, int]] = None,
) -> array:
    ancho = b_fin - b_ini
    anterior = array("I", [0]) * (ancho + 1)
    actual = array("I", [0]) * (ancho + 1)

    for idx_a in range(a_fin - 1, a_ini - 1, -1):
        char_a = a[idx_a]
        actual[0] = 0
        for col in range(1, ancho + 1):
            if metricas is not None:
                metricas["celdas"] = metricas.get("celdas", 0) + 1
            if char_a == b[b_fin - col]:
                actual[col] = anterior[col - 1] + 1
            else:
                arriba = anterior[col]
                izq = actual[col - 1]
                actual[col] = arriba if arriba >= izq else izq
        anterior, actual = actual, anterior

    return anterior


def _hirschberg_rangos(
    a: str,
    a_ini: int,
    a_fin: int,
    b: str,
    b_ini: int,
    b_fin: int,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
    m = a_fin - a_ini
    n = b_fin - b_ini

    if m == 0 or n == 0:
        return ""

    if m == 1:
        simbolo = a[a_ini]
        if metricas is not None:
            metricas["celdas"] = metricas.get("celdas", 0) + n
        for idx_b in range(b_ini, b_fin):
            if b[idx_b] == simbolo:
                return simbolo
        return ""

    if n == 1:
        simbolo = b[b_ini]
        if metricas is not None:
            metricas["celdas"] = metricas.get("celdas", 0) + m
        for idx_a in range(a_ini, a_fin):
            if a[idx_a] == simbolo:
                return simbolo
        return ""

    mitad = a_ini + (m // 2)

    puntuacion_izq = _fila_puntuaciones_directa(a, a_ini, mitad, b, b_ini, b_fin, metricas)
    puntuacion_der = _fila_puntuaciones_inversa(a, mitad, a_fin, b, b_ini, b_fin, metricas)

    mejor_k = 0
    mejor_valor = -1
    for k in range(n + 1):
        suma = puntuacion_izq[k] + puntuacion_der[n - k]
        if suma > mejor_valor:
            mejor_valor = suma
            mejor_k = k

    del puntuacion_izq
    del puntuacion_der

    corte_b = b_ini + mejor_k
    parte_1 = _hirschberg_rangos(a, a_ini, mitad, b, b_ini, corte_b, metricas)
    parte_2 = _hirschberg_rangos(a, mitad, a_fin, b, corte_b, b_fin, metricas)
    return parte_1 + parte_2


def lcs_hirschberg(
    cadena_a: str,
    cadena_b: str,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
    if len(cadena_a) < len(cadena_b):
        return _hirschberg_rangos(cadena_b, 0, len(cadena_b), cadena_a, 0, len(cadena_a), metricas)
    return _hirschberg_rangos(cadena_a, 0, len(cadena_a), cadena_b, 0, len(cadena_b), metricas)
