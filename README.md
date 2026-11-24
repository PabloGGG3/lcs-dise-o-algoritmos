# Actividad 1 — Diseño, análisis y comparación de algoritmos (LCS)

Implementación desde cero en Python de tres enfoques para resolver el problema de la **Subsecuencia Común Más Larga (LCS)**:

- **Versión A (`lcs_recursiva`)**: Recursión directa sin memorización (Tema 1).
- **Versión B (`lcs_hirschberg`)**: Estrategia divide y conquista de Hirschberg con espacio lineal (Tema 2).
- **Versión C (`lcs_dinamica`)**: Programación dinámica tabular ascendente con reconstrucción por retroceso (Tema 3).

## Requisitos

- Python 3.9 o superior (el cálculo de LCS y las mediciones solo emplean la biblioteca estándar).
- `matplotlib` (opcional, únicamente para generar la gráfica comparativa).

## Ejecución con un único comando

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

Este comando ejecuta automáticamente:
1. La batería de pruebas unitarias (`tests_lcs.py`).
2. La generación reproducible de datasets en `datos/`.
3. El benchmark de tiempo de CPU, memoria pico y operaciones en `resultados/resultados.csv`.
4. La gráfica comparativa en `resultados/grafica_comparativa.png` (si `matplotlib` está instalado).

## Estructura del proyecto

- `algoritmos.py`: Implementación de las tres versiones del algoritmo LCS.
- `tests_lcs.py`: Pruebas unitarias con `unittest` (casos límite y pruebas aleatorias).
- `benchmark.py`: Generación de datos, medición de tiempos (`time.process_time`), memoria (`tracemalloc`) y gráficas.
- `main.py`: Script lanzador único.
- `datos/`: Parejas de cadenas generadas con semilla fija (`4096`).
- `resultados/`: Métricas en CSV, metadatos del entorno y gráfica comparativa.
