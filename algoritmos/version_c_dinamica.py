from __future__ import annotations
from typing import Dict, Optional


def lcs_dinamica(
    cadena_a: str,
    cadena_b: str,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
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
