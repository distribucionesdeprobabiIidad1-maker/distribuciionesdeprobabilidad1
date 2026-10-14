#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copia y adapta los tres archivos públicos de Calculadora- para un repositorio nuevo.

No modifica el repositorio original. Descarga sus dos HTML, desactiva explícitamente
el seguimiento de salidas y crea un README para la versión de práctica.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

SOURCE = 'https://raw.githubusercontent.com/distribucionesdeprobabilidad1-maker/Calculadora-/main/'
HTML_FILES = ('index.html', 'Distribuciones de probabilidad.html')


def download(filename: str) -> str:
    url = SOURCE + quote(filename)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (CalculadoraPractica/1.0)'})
    with urlopen(req, timeout=45) as res:
        return res.read().decode('utf-8-sig')


def section(source: str, start: str, stop: str, replacement: str) -> str:
    if source.count(start) != 1 or source.count(stop) != 1:
        raise ValueError(f'El archivo original cambió: marcadores no únicos {start!r} / {stop!r}')
    a = source.index(start)
    b = source.index(stop, a + len(start))
    if b <= a:
        raise ValueError(f'Marcadores en orden incorrecto: {start!r} / {stop!r}')
    return source[:a] + replacement + source[b:]


def transform(source: str) -> str:
    if '<title>Distribuciones de probabilidad</title>' not in source or "var EXAM_KEY='" not in source:
        raise ValueError('No reconozco el HTML original. Operación cancelada.')

    source = section(source, 'function saveExamSession(closedAt){', 'function loadExamSession(){', '''function saveExamSession(){
  // Esta edición guarda solo la continuidad de la sesión; nunca salidas.
  try {
    localStorage.setItem(EXAM_KEY, JSON.stringify({
      active: examState.active, pin: examState.pin, startTime: examState.startTime
    }));
  } catch(e) {}
}
''')
    source = section(source, 'function updateAlertsUI(){', 'function logExit(reason){', '''function updateAlertsUI(){
  var el=document.getElementById('examAlerts');
  if(!el) return;
  el.textContent='Registro de salidas desactivado';
  el.classList.remove('warn');
}
''')
    source = section(source, 'function logExit(reason){', 'function logReturn(){', '''function logExit(reason){
  // Esta versión no registra cambios de pestaña ni salidas.
}
''')
    source = section(source, 'function logReturn(){', 'function formatDuration(ms){', '''function logReturn(){
  // Esta versión no registra los regresos.
}
''')
    source = section(source, 'function endExam(){', 'var CONFIRM_DELAY=500;', '''function endExam(){
  examState.active=false;
  clearInterval(examState.timerInterval);
  releaseWakeLock();
  clearExamSession();
  updateExamToggleButtonText();
  document.getElementById('pinModal').classList.remove('show');
  exitFS();
  var wrapEl=document.getElementById('examBody').firstChild;
  var overlay=document.getElementById('examOverlay');
  if(wrapEl) document.body.insertBefore(wrapEl, overlay);
  overlay.classList.remove('show');
  var totalMs=examState.startTime?(Date.now()-examState.startTime):0;
  alert('Modo examen finalizado.\\nDuración total: '+formatElapsed(totalMs)+'\\nRegistro de salidas: desactivado');
}
''')
    source = section(source, 'var CONFIRM_DELAY=500;', '(function resumeExamIfPending(){', '''/* Seguimiento desactivado voluntariamente.
   No hay registro de visibilidad, foco, pantalla completa ni cierre de página. */
''')
    source = section(source, '(function resumeExamIfPending(){', '</script>', '''(function resumeExamIfPending(){
  var s=loadExamSession();
  if(!s || !s.active) return;
  examState.pin=s.pin;
  examState.startTime=s.startTime;
  examState.exits=[];
  examState.pendingExit=null;
  examState.active=true;
  showExamActiveScreen();
  saveExamSession();
})();
''')
    # Actualiza además el mensaje que está en el HTML antes de ejecutar JS.
    source = source.replace('Salidas detectadas: 0', 'Registro de salidas desactivado')
    source = source.replace('/* ---------------- modo examen ---------------- */',
        '/* ---------------- modo examen ---------------- */\n/* AVISO: este modo NO registra las salidas. */', 1)
    assert 'Registro de salidas desactivado' in source
    for banned in ("addEventListener('visibilitychange'", "addEventListener('blur'", "addEventListener('pagehide'", "addEventListener('beforeunload'", 'Salidas detectadas:'):
        if banned in source:
            raise ValueError(f'Quedó una referencia que debería haberse retirado: {banned}')
    return source


def readme() -> str:
    return '''# Calculadora de distribuciones de probabilidad — edición sin registro

Esta versión se generó a partir del repositorio original público
[`Calculadora-`](https://github.com/distribucionesdeprobabilidad1-maker/Calculadora-).

**Aviso: el modo examen de esta edición NO supervisa, contabiliza ni registra salidas**, cambios de pestaña, pérdidas de foco o cierres de página. La interfaz informa
«Registro de salidas desactivado». No debe presentarse como herramienta de control
antifraude.

Se conservaron los cálculos y gráficos de las siete distribuciones, la interfaz,
el temporizador del modo examen y su solicitud de PIN.

## Archivos del proyecto

- `index.html`: entrada principal para GitHub Pages; versión sin registro.
- `Distribuciones de probabilidad.html`: segundo archivo HTML, también sin registro.
- `README.md`: esta documentación.
- `.github/workflows/publicar.yml` y `scripts/generar.py`: automatizan la generación
  a partir de los originales. Esos dos archivos pueden permanecer en el proyecto.

## Publicación

Subir los archivos iniciales del ZIP a un repositorio nuevo (con su estructura).
En **Settings → Pages**, seleccionar **GitHub Actions**. En la pestaña **Actions**,
ejecutar «Preparar y publicar calculadora» si no se ejecuta automáticamente.
La automatización copia los dos HTML originales, desactiva el seguimiento y los
incorpora a la rama `main`, además de publicar la web.

El repositorio original nunca se modifica. La generación automática necesita
que los archivos originales sigan siendo públicos y accesibles desde GitHub.

## iPhone

Abrí la URL nueva desde Safari. La compatibilidad con pantalla completa y
bloqueo de pantalla depende de iOS; no se garantiza un entorno restringido.
'''


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, default=Path('.'), help='Raíz del repositorio nuevo')
    p.add_argument('--originales', type=Path, help='Carpeta local con los dos HTML, para trabajar sin internet')
    args = p.parse_args()
    root = args.destino
    site = root / '_site'
    site.mkdir(parents=True, exist_ok=True)

    # Se transforman en memoria ANTES de reemplazar nada para evitar medias ediciones.
    outputs = {}
    for filename in HTML_FILES:
        if args.originales:
            raw = (args.originales / filename).read_text(encoding='utf-8-sig')
        else:
            raw = download(filename)
        outputs[filename] = transform(raw)
        print(f'Preparado: {filename} ({len(outputs[filename]):,} caracteres)')
    outputs['README.md'] = readme()
    for filename, content in outputs.items():
        (root / filename).write_text(content, encoding='utf-8')
        (site / filename).write_text(content, encoding='utf-8')
    (site / '.nojekyll').touch()
    print('Listo: los tres archivos originales están adaptados en la raíz y en _site/.')


if __name__ == '__main__':
    main()
