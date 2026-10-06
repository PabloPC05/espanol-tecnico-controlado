---
name: espanol-tecnico-controlado
description: Escribe explicaciones, instrucciones y resúmenes en español de España con un estilo controlado y sin ambigüedades (frases cortas, una acción por frase, un término por concepto). Úsala cuando la persona pida «español controlado», «español técnico simplificado», «explícamelo en lenguaje claro y técnico», «modo 80 %», un equivalente en español de ASD-STE100, o cuando redactes procedimientos, mensajes de error, instrucciones entre agentes o prompts de sistema en español.
---

# Español Técnico Controlado (ETC)

Estilo de escritura controlado para español de España. Está inspirado en la idea de Andrej Karpathy (2 de octubre de 2026): pedir al modelo que explique en un inglés controlado, para que la persona entienda su salida con menos esfuerzo. Este estilo es un trabajo original y no es una traducción ni una versión oficial de ASD-STE100.

## Modos

- **80 % (por defecto):** aplica las reglas 1 a 10 de abajo. Permite el vocabulario habitual si no es ambiguo.
- **Estricto:** aplica las 20 reglas y usa solo palabras del diccionario para los sentidos que cubre. Úsalo si la persona dice «estricto» o «lo más controlado posible».

## Reglas esenciales

1. Escribe frases de procedimiento de 20 palabras o menos. Escribe frases descriptivas de 25 palabras o menos.
2. Pon una sola acción en cada frase.
3. Empieza las instrucciones con el verbo en imperativo de tú («Apaga el equipo.»).
4. Usa voz activa y di quién hace cada cosa.
5. Usa un solo nombre para cada cosa y mantenlo en todo el texto. No alternes «programa», «aplicación» y «herramienta».
6. Usa cada palabra con un solo sentido. Consulta `references/diccionario.psv`.
7. Evita el gerundio. Escribe dos frases o usa «y».
8. Pon la condición antes de la acción: «Si el error continúa, reinicia el equipo.»
9. Cambia los verbos de apoyo por un verbo directo: «realizar una comprobación» → «comprobar».
10. Evita metáforas, frases hechas e ironía.

Las reglas 11 a 20 están en `references/reglas.md`, con ejemplos correctos e incorrectos.

## Cómo trabajar

1. Escribe el texto pensando en una persona que lo lee una sola vez.
2. Si usas el modo estricto, consulta `references/diccionario.psv`. La columna «evitar» dice qué palabra sustituir.
3. Para textos largos o importantes, comprueba el resultado con el verificador:
   `python3 -I scripts/ete_check.py texto.md` (la ruta es la del repositorio).
4. Corrige los avisos que sean reales. El verificador es una ayuda heurística y da falsos positivos.

## Nombres técnicos

Puedes usar el nombre de una pieza, un programa, una orden o una marca aunque no esté en el diccionario. Escríbelo siempre igual. Si es poco conocido, defínelo una vez en una frase corta.

## Límites

- El diccionario es un núcleo inicial (versión 0.1). No cubre todo el español técnico.
- Un texto escrito con estas reglas es «estilo controlado», no un texto certificado.
- No lo uses para textos creativos, comerciales o literarios. Este estilo busca claridad, no belleza.
- Si un texto exige otra convención (jurídica, administrativa o de lectura fácil), sigue esa convención. La norma UNE-ISO 24495-1 sobre lenguaje claro es la referencia general en España.

## Si la persona quiere entender mejor

El mismo consejo de Karpathy propone formatos más fáciles de leer que el texto: un diagrama, una página HTML interactiva o un vídeo explicativo. Ofrécelos solo si la persona los pide o si el tema es muy visual. Todo el texto dentro de esos formatos también sigue este estilo.
