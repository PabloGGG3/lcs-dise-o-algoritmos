# Actividad 1 — Diseño, análisis y comparación de algoritmos (LCS)

Implementación desde cero en Python de tres enfoques para resolver el problema de la **Subsecuencia Común Más Larga (LCS)**:

- **Versión A (`algoritmos/version_a_recursiva.py`)**: Recursión directa sin memorización (Tema 1).
- **Versión B (`algoritmos/version_b_hirschberg.py`)**: Estrategia divide y conquista de Hirschberg con espacio lineal (Tema 2).
- **Versión C (`algoritmos/version_c_dinamica.py`)**: Programación dinámica tabular ascendente con reconstrucción por retroceso (Tema 3).

## Requisitos

- Python 3.13.14 (el cálculo de LCS y las mediciones solo emplean la biblioteca estándar).
- `matplotlib` (opcional, únicamente para generar la gráfica comparativa si no se tiene instalada no generará la gráfica).

## Ejecución con un único comando

Desde la carpeta raíz del proyecto ponemos cmd:

```bash
python main.py
```

Este comando ejecuta automáticamente:
1. La batería de pruebas unitarias (`tests_lcs.py`).
2. La generación de los datasets en `datos/`.
3. El benchmark de tiempo de CPU, memoria pico y operaciones por consola y en `resultados/resultados.csv`.
4. La gráfica comparativa en `resultados/grafica_comparativa.png` (si `matplotlib` está instalado).

## Estructura del proyecto

- `algoritmos/`: Paquete con las tres versiones separadas (`version_a_recursiva.py`, `version_b_hirschberg.py`, `version_c_dinamica.py`).
- `tests_lcs.py`: Pruebas unitarias con `unittest` (casos límite y pruebas aleatorias).
- `benchmark.py`: Generación de datos, medición de tiempos (`time.process_time`), memoria (`tracemalloc`) y gráficas.
- `main.py`: Script lanzador único.
- `datos/`: Parejas de cadenas de longitud creciente.
- `resultados/`: Métricas en CSV, metadatos del entorno (`entorno.json`) y gráfica comparativa.
