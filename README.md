# Español Técnico Controlado (ETC)

Una skill para agentes de IA que hace que el modelo escriba en **español de España controlado**: frases cortas, una acción por frase y un término por concepto.

Nace del consejo de Andrej Karpathy del 2 de octubre de 2026: pedir al modelo que explique en un inglés controlado de estilo ASD-STE100, para entender mejor lo que produce. Este proyecto hace lo mismo para el español.

## Qué incluye

| Archivo | Contenido |
| --- | --- |
| `skills/espanol-tecnico-controlado/SKILL.md` | La skill: modos, reglas esenciales y forma de trabajar |
| `skills/espanol-tecnico-controlado/references/reglas.md` | 20 reglas con ejemplos correctos e incorrectos |
| `skills/espanol-tecnico-controlado/references/diccionario.psv` | Diccionario inicial: sentido único por palabra y lista de sinónimos a evitar |
| `scripts/ete_check.py` | Verificador: avisa de palabras a evitar, frases largas y gerundios |
| `tests/test_ete.py` | Pruebas del verificador y del diccionario |

## Instalación

Copia la carpeta `skills/espanol-tecnico-controlado` al directorio de skills de tu agente. Por ejemplo, en Claude Code: `~/.claude/skills/`.

## Uso

Pide al agente, por ejemplo:

- «Explícamelo en español técnico controlado.»
- «Modo 80 %: explica el error en español controlado.»
- «Reescribe estas instrucciones en estilo ETC estricto.»

Para revisar un texto tú mismo:

```
python3 scripts/ete_check.py texto.md
python3 scripts/ete_check.py --validate
python3 tests/test_ete.py
```

## Cómo se relaciona con ASD-STE100

ASD-STE100 se compone de reglas de escritura y de un diccionario controlado. Cada palabra del diccionario tiene un solo sentido y una sola categoría gramatical, y el diccionario dice qué sinónimos no se usan. ETC copia esa **estructura**, no el contenido:

- Las reglas son originales y están adaptadas al español.
- El diccionario es original. No es una traducción del diccionario de ASD, cuyos derechos pertenecen a ASD.
- El proyecto no tiene relación con ASD ni con el grupo que mantiene ASD-STE100.

## Límites

- La versión 0.1 tiene unas 150 entradas. ASD-STE100 tiene unas 900 palabras aprobadas. Falta mucho vocabulario.
- Es un estilo controlado, no una norma certificada.
- El verificador es heurístico. Da falsos positivos, por ejemplo con nombres que coinciden con formas verbales.
- No sirve para textos creativos ni comerciales.

## Trabajos relacionados

- **Español Técnico Simplificado (ETS)**, de Ilaria Gobbi (Universidad de Bolonia, 2014): lenguaje controlado académico basado en ASD-STE100.
- **UNE-ISO 24495-1:2024**, *Lenguaje claro*: norma de principios y directrices para España.
- **ASD-STE100**: [asd-ste100.org](https://www.asd-ste100.org/).

## Cómo ampliar el diccionario

Añade una línea a `diccionario.psv` con cinco columnas: palabra, categoría, sentido único, palabras a evitar y un ejemplo. Después ejecuta `python3 tests/test_ete.py`. Las pruebas comprueban que el ejemplo cumple las reglas y que ninguna palabra aprobada está prohibida en otra entrada.

## Licencia

MIT. Mira `LICENSE`.
