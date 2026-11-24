"""Implementación desde cero de las tres versiones del problema LCS
(Subsecuencia Común Más Larga) usando únicamente la biblioteca estándar de Python.
"""

from __future__ import annotations
from array import array
from typing import Dict, Optional


def lcs_recursiva(
    cadena_a: str,
    cadena_b: str,
    i: Optional[int] = None,
    j: Optional[int] = None,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
    """Versión A: Recursión directa sin memorización (Tema 1).

    Evalúa la recurrencia clásica sobre los prefijos cadena_a[:i] y cadena_b[:j]
    sin almacenar resultados intermedios.
    """
    if i is None:
        i = len(cadena_a)
    if j is None:
        j = len(cadena_b)

    if metricas is not None:
        metricas["llamadas"] = metricas.get("llamadas", 0) + 1

    if i == 0 or j == 0:
        return ""

    if cadena_a[i - 1] == cadena_b[j - 1]:
        return lcs_recursiva(cadena_a, cadena_b, i - 1, j - 1, metricas) + cadena_a[i - 1]

    rama_arriba = lcs_recursiva(cadena_a, cadena_b, i - 1, j, metricas)
    rama_izquierda = lcs_recursiva(cadena_a, cadena_b, i, j - 1, metricas)

    if len(rama_arriba) >= len(rama_izquierda):
        return rama_arriba
    return rama_izquierda


def _fila_puntuaciones_directa(
    a: str,
    a_ini: int,
    a_fin: int,
    b: str,
    b_ini: int,
    b_fin: int,
    metricas: Optional[Dict[str, int]] = None,
) -> array:
    """Calcula la última fila de longitudes LCS en sentido directo usando dos filas."""
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
    """Calcula la última fila de longitudes LCS recorriendo ambas subcadenas al revés."""
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
    """Núcleo recursivo de Hirschberg operando con índices para evitar copias de cadenas."""
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

    # Liberamos los vectores antes de bajar en la recursión para mantener espacio lineal
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
    """Versión B: Estrategia divide y conquista de Hirschberg (Tema 2).

    Coloca la cadena más corta como segunda entrada para garantizar espacio O(min(m, n) + log m).
    """
    if len(cadena_a) < len(cadena_b):
        return _hirschberg_rangos(cadena_b, 0, len(cadena_b), cadena_a, 0, len(cadena_a), metricas)
    return _hirschberg_rangos(cadena_a, 0, len(cadena_a), cadena_b, 0, len(cadena_b), metricas)


def lcs_dinamica(
    cadena_a: str,
    cadena_b: str,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
    """Versión C: Programación dinámica tabular ascendente con retroceso (Tema 3)."""
    m = len(cadena_a)
    n = len(cadena_b)

    if m == 0 or n == 0:
        return ""

    tabla = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        char_a = cadena_a[i - 1]
        fila_ant = tabla[i - 1]
        fila_act = tabla[i]
        for j in range(1, n + 1):
            if metricas is not None:
                metricas["celdas"] = metricas.get("celdas", 0) + 1
            if char_a == cadena_b[j - 1]:
                fila_act[j] = fila_ant[j - 1] + 1
            else:
                arriba = fila_ant[j]
                izq = fila_act[j - 1]
                fila_act[j] = arriba if arriba >= izq else izq

    # Reconstrucción de la subsecuencia por retroceso (backtracking)
    i, j = m, n
    resultado = []
    while i > 0 and j > 0:
        if cadena_a[i - 1] == cadena_b[j - 1]:
            resultado.append(cadena_a[i - 1])
            i -= 1
            j -= 1
        elif tabla[i - 1][j] >= tabla[i][j - 1]:
            i -= 1
        else:
            j -= 1

    resultado.reverse()
    return "".join(resultado)
