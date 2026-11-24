"""Script de experimentación: genera datasets, mide tiempo de CPU, memoria pico y operaciones."""

from __future__ import annotations

import csv
import gc
import json
import os
import platform
import random
import subprocess
import sys
import time
import tracemalloc
from typing import Callable, Dict, List, Optional, Tuple

from algoritmos import lcs_dinamica, lcs_hirschberg, lcs_recursiva

TAMANOS = [6, 10, 14, 18, 120, 300, 600, 1100, 1600]
ALFABETO = ["A", "B", "C", "D", "E"]
SEMILLA = 4096
REPETICIONES = 3
TIMEOUT_VERS_A_SEG = 8.0


def generar_y_guardar_datos(carpeta: str = "datos") -> List[Tuple[int, str, str]]:
    """Genera las parejas de cadenas con semilla fija y las guarda en disco."""
    os.makedirs(carpeta, exist_ok=True)
    rng = random.Random(SEMILLA)
    parejas: List[Tuple[int, str, str]] = []

    for n in TAMANOS:
        cad_a = "".join(rng.choice(ALFABETO) for _ in range(n))
        cad_b = "".join(rng.choice(ALFABETO) for _ in range(n))
        parejas.append((n, cad_a, cad_b))

        ruta = os.path.join(carpeta, f"pareja_n{n}.txt")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(cad_a + "\n" + cad_b + "\n")

    return parejas


def medir_cpu_ms(funcion: Callable[[str, str], str], cad_a: str, cad_b: str) -> float:
    """Mide el tiempo de CPU en milisegundos usando la mediana de REPETICIONES."""
    # Calibración para evitar ruido en ejecuciones muy cortas
    t0 = time.perf_counter()
    funcion(cad_a, cad_b)
    duracion_una = time.perf_counter() - t0
    iteraciones = 1
    if duracion_una < 0.05:
        iteraciones = max(1, min(500, int(0.15 / max(duracion_una, 1e-6))))

    muestras = []
    for _ in range(REPETICIONES):
        gc.collect()
        gc.disable()
        inicio = time.process_time()
        for _ in range(iteraciones):
            funcion(cad_a, cad_b)
        fin = time.process_time()
        gc.enable()
        muestras.append(((fin - inicio) / iteraciones) * 1000.0)

    muestras.sort()
    return muestras[len(muestras) // 2]


def medir_memoria_kib(funcion: Callable[[str, str], str], cad_a: str, cad_b: str) -> float:
    """Mide el pico de memoria adicional asignada por Python (en KiB) con tracemalloc."""
    gc.collect()
    tracemalloc.start()
    funcion(cad_a, cad_b)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1024.0


def medir_version_a_aislada(cad_a: str, cad_b: str, timeout_seg: float) -> Optional[Dict[str, float]]:
    """Ejecuta la Versión A en un subproceso aislado para respetar el límite de tiempo."""
    codigo_hijo = f"""
import gc, json, sys, time, tracemalloc
sys.setrecursionlimit(10000)
from algoritmos import lcs_recursiva

cad_a = {cad_a!r}
cad_b = {cad_b!r}

# Calibración
t0 = time.perf_counter()
res = lcs_recursiva(cad_a, cad_b)
dur = time.perf_counter() - t0
iters = 1 if dur >= 0.05 else max(1, min(300, int(0.15 / max(dur, 1e-6))))

muestras = []
for _ in range({REPETICIONES}):
    gc.collect()
    gc.disable()
    ini = time.process_time()
    for _ in range(iters):
        lcs_recursiva(cad_a, cad_b)
    fin = time.process_time()
    gc.enable()
    muestras.append(((fin - ini) / iters) * 1000.0)
muestras.sort()
cpu_ms = muestras[len(muestras) // 2]

gc.collect()
tracemalloc.start()
lcs_recursiva(cad_a, cad_b)
_, pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

metricas = {{}}
lcs_recursiva(cad_a, cad_b, metricas=metricas)

print(json.dumps({{
    "cpu_ms": cpu_ms,
    "mem_kib": pico / 1024.0,
    "llamadas": metricas.get("llamadas", 0),
    "longitud": len(res),
}}))
"""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", codigo_hijo],
            capture_output=True,
            text=True,
            timeout=timeout_seg,
            check=True,
        )
        return json.loads(proc.stdout.strip())
    except subprocess.TimeoutExpired:
        return None


def generar_graficas(filas: List[Dict[str, object]], carpeta: str = "resultados") -> Optional[str]:
    """Genera las gráficas comparativas en escala log-log usando matplotlib si está disponible."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Aviso: matplotlib no está instalado. Se omite la generación de gráficas.")
        return None

    ns_a, cpu_a, mem_a = [], [], []
    ns_all, cpu_b, cpu_c, mem_b, mem_c = [], [], [], [], []
    n_timeout = None

    for fila in filas:
        n = int(fila["n"])
        ns_all.append(n)
        cpu_b.append(float(fila["cpu_b_ms"]) / 1000.0)
        cpu_c.append(float(fila["cpu_c_ms"]) / 1000.0)
        mem_b.append(float(fila["mem_b_kib"]))
        mem_c.append(float(fila["mem_c_kib"]))

        if isinstance(fila["cpu_a_ms"], (int, float)):
            ns_a.append(n)
            cpu_a.append(float(fila["cpu_a_ms"]) / 1000.0)
            mem_a.append(float(fila["mem_a_kib"]))
        elif fila["cpu_a_ms"] == f">{TIMEOUT_VERS_A_SEG:.0f}s" and n_timeout is None:
            n_timeout = n

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3))

    # Gráfica 1: Tiempo de CPU
    if ns_a:
        ax1.loglog(ns_a, cpu_a, marker="x", linestyle=":", color="#C0392B", linewidth=1.8, label="Versión A (recursiva)")
    if n_timeout is not None:
        ax1.scatter([n_timeout], [TIMEOUT_VERS_A_SEG], marker="^", s=70, color="#C0392B", zorder=5)
        ax1.annotate(
            f"> {TIMEOUT_VERS_A_SEG:.0f} s",
            (n_timeout, TIMEOUT_VERS_A_SEG),
            textcoords="offset points",
            xytext=(6, -4),
            fontsize=8.5,
            color="#C0392B",
        )
    ax1.loglog(ns_all, cpu_b, marker="s", linestyle="-", color="#1F618D", linewidth=1.8, label="Versión B (Hirschberg)")
    ax1.loglog(ns_all, cpu_c, marker="o", linestyle="--", color="#1E8449", linewidth=1.8, label="Versión C (PD tabular)")
    ax1.set_title("Tiempo de CPU (escala log-log)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Longitud n de cada cadena")
    ax1.set_ylabel("Tiempo de CPU (s)")
    ax1.grid(True, which="both", linestyle="--", alpha=0.35)
    ax1.legend(fontsize=8.5)

    # Gráfica 2: Memoria pico
    if ns_a:
        ax2.loglog(ns_a, mem_a, marker="x", linestyle=":", color="#C0392B", linewidth=1.8, label="Versión A (recursiva)")
    ax2.loglog(ns_all, mem_b, marker="s", linestyle="-", color="#1F618D", linewidth=1.8, label="Versión B (Hirschberg)")
    ax2.loglog(ns_all, mem_c, marker="o", linestyle="--", color="#1E8449", linewidth=1.8, label="Versión C (PD tabular)")
    ax2.set_title("Pico de memoria adicional (escala log-log)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Longitud n de cada cadena")
    ax2.set_ylabel("Memoria pico (KiB)")
    ax2.grid(True, which="both", linestyle="--", alpha=0.35)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    ruta_img = os.path.join(carpeta, "grafica_comparativa.png")
    plt.savefig(ruta_img, dpi=180)
    plt.close(fig)
    return ruta_img


def ejecutar_benchmark() -> List[Dict[str, object]]:
    os.makedirs("resultados", exist_ok=True)
    parejas = generar_y_guardar_datos("datos")
    filas: List[Dict[str, object]] = []
    version_a_detenida = False

    entorno = {
        "python": platform.python_version(),
        "sistema": f"{platform.system()} {platform.release()}",
        "arquitectura": platform.machine(),
        "nucleos": os.cpu_count(),
        "tamanos": TAMANOS,
        "alfabeto": ALFABETO,
        "semilla": SEMILLA,
        "repeticiones": REPETICIONES,
        "timeout_a_seg": TIMEOUT_VERS_A_SEG,
    }
    with open(os.path.join("resultados", "entorno.json"), "w", encoding="utf-8") as f:
        json.dump(entorno, f, indent=2, ensure_ascii=False)

    print("\n=== RESULTADOS EXPERIMENTALES (Tiempo CPU y Memoria Pico) ===")
    cabecera = (
        f"{'n':>5} | {'CPU A (ms)':>11} | {'CPU B (ms)':>10} | {'CPU C (ms)':>10} | "
        f"{'Mem A (KiB)':>11} | {'Mem B (KiB)':>11} | {'Mem C (KiB)':>11}"
    )
    print(cabecera)
    print("-" * len(cabecera))

    for n, cad_a, cad_b in parejas:
        if not version_a_detenida:
            info_a = medir_version_a_aislada(cad_a, cad_b, TIMEOUT_VERS_A_SEG)
            if info_a is None:
                cpu_a_val: object = f">{TIMEOUT_VERS_A_SEG:.0f}s"
                mem_a_val: object = "-"
                llamadas_a_val: object = "-"
                version_a_detenida = True
            else:
                cpu_a_val = round(info_a["cpu_ms"], 4)
                mem_a_val = round(info_a["mem_kib"], 2)
                llamadas_a_val = int(info_a["llamadas"])
        else:
            cpu_a_val = "-"
            mem_a_val = "-"
            llamadas_a_val = "-"

        cpu_b = round(medir_cpu_ms(lcs_hirschberg, cad_a, cad_b), 4)
        mem_b = round(medir_memoria_kib(lcs_hirschberg, cad_a, cad_b), 2)
        met_b: Dict[str, int] = {}
        res_b = lcs_hirschberg(cad_a, cad_b, metricas=met_b)

        cpu_c = round(medir_cpu_ms(lcs_dinamica, cad_a, cad_b), 4)
        mem_c = round(medir_memoria_kib(lcs_dinamica, cad_a, cad_b), 2)
        met_c: Dict[str, int] = {}
        res_c = lcs_dinamica(cad_a, cad_b, metricas=met_c)

        assert len(res_b) == len(res_c), f"Desajuste de longitud LCS para n={n}"

        celdas_b = met_b.get("celdas", 0)
        celdas_c = met_c.get("celdas", 0)
        ratio_bc = round(celdas_b / celdas_c, 2) if celdas_c else 0.0

        print(
            f"{n:>5} | {str(cpu_a_val):>11} | {cpu_b:>10.4f} | {cpu_c:>10.4f} | "
            f"{str(mem_a_val):>11} | {mem_b:>11.2f} | {mem_c:>11.2f}"
        )

        filas.append(
            {
                "n": n,
                "cpu_a_ms": cpu_a_val,
                "cpu_b_ms": cpu_b,
                "cpu_c_ms": cpu_c,
                "mem_a_kib": mem_a_val,
                "mem_b_kib": mem_b,
                "mem_c_kib": mem_c,
                "llamadas_a": llamadas_a_val,
                "celdas_b": celdas_b,
                "celdas_c": celdas_c,
                "ratio_b_c": ratio_bc,
                "long_lcs": len(res_c),
            }
        )

    csv_path = os.path.join("resultados", "resultados.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)

    img_path = generar_graficas(filas, "resultados")
    print(f"\nDatos guardados en: {csv_path}")
    if img_path:
        print(f"Gráfica guardada en: {img_path}")

    return filas


if __name__ == "__main__":
    ejecutar_benchmark()
