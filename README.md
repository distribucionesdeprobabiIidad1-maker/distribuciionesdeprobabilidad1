# Calculadora de distribuciones de probabilidad — instalador para repositorio nuevo

Este proyecto prepara una **copia propia y visible sin registro de salidas**.
Se basa en el repositorio original público `distribucionesdeprobabilidad1-maker/Calculadora-`.

## Pasos para subirlo

1. Creá un **repositorio público nuevo** en GitHub, por ejemplo `Calculadora-practica`.
2. **Descomprimí** el ZIP y subí estos archivos y carpetas a la rama `main` (no subas el ZIP cerrado):

   ```text
   README.md
   scripts/generar.py
   .github/workflows/publicar.yml
   ```

3. En **Settings → Actions → General → Workflow permissions**, permití **Read and write permissions** si el repositorio limita los permisos de los workflows (necesario para añadir los archivos al repositorio).
4. En **Settings → Pages → Build and deployment → Source**, seleccioná **GitHub Actions**.
5. En **Actions**, abrí **Preparar y publicar calculadora** y usá **Run workflow** si no se ejecutó automáticamente.
6. La ejecución añadirá automáticamente los **3 archivos originales adaptados** a tu nuevo repositorio:

   ```text
   index.html
   Distribuciones de probabilidad.html
   README.md
   ```

   También publicará la calculadora en `https://TU-USUARIO.github.io/TU-REPO/`.

No hace falta modificar archivos en el iPhone. Usá Safari para abrir esa URL nueva.

## Qué conserva

- Todos los cálculos estadísticos de las siete distribuciones del proyecto original.
- El mismo diseño y los gráficos, el temporizador y el sistema de PIN.

## Qué quita

- El registro de cambios de pestaña y de ventana, cierre de navegador o pérdidas de foco.
- El contador e historial de salidas.
- La advertencia al intentar abandonar la página.

La interfaz muestra **«Registro de salidas desactivado»**. Esta edición NO es una
herramienta de vigilancia de exámenes, y no debe presentarse como tal.

## Aclaración

El ZIP inicial contiene el generador y la automatización, **no** los dos HTML
originales completos, que se descargan del repositorio público durante la
primera ejecución. Al terminar el workflow, los tres archivos ya están en tu
nuevo repositorio y la calculadora publicada. La fuente original no se altera.

En equipos con Python 3 también podés ejecutar `python scripts/generar.py` para
crear localmente los dos HTML; no es necesario hacerlo para publicarlo con GitHub.
