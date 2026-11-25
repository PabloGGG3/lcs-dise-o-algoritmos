from __future__ import annotations
from typing import Dict, Optional


def lcs_recursiva(
    cadena_a: str,
    cadena_b: str,
    i: Optional[int] = None,
    j: Optional[int] = None,
    metricas: Optional[Dict[str, int]] = None,
) -> str:
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
