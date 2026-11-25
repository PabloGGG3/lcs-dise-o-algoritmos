import subprocess
import sys
from benchmark import ejecutar_benchmark


def main() -> None:
    print("Paso 1/2: Ejecutando pruebas unitarias...")
    res = subprocess.run([sys.executable, "-m", "unittest", "tests_lcs.py", "-v"], check=False)
    if res.returncode != 0:
        print("Error: las pruebas unitarias no han pasado.")
        sys.exit(res.returncode)

    print("\nPaso 2/2: Ejecutando experimentos de tiempo y memoria...")
    ejecutar_benchmark()
    print("\nProceso finalizado correctamente.")


if __name__ == "__main__":
    main()
