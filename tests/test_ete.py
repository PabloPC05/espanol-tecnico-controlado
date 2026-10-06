import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import ete_check as ete  # noqa: E402

REGLAS = ROOT / "skills" / "espanol-tecnico-controlado" / "references" / "reglas.md"


class TestDiccionario(unittest.TestCase):
    def setUp(self):
        self.entries = ete.load_dictionary()
        self.patterns = ete.build_patterns(self.entries)

    def test_diccionario_valido(self):
        self.assertEqual(ete.validate(self.entries), [])

    def test_hay_entradas_suficientes(self):
        self.assertGreaterEqual(len(self.entries), 150)

    def test_ejemplos_correctos_de_las_reglas(self):
        lineas = [l[1:].strip() for l in REGLAS.read_text(encoding="utf-8").splitlines() if l.startswith("✔")]
        self.assertGreater(len(lineas), 10)
        for linea in lineas:
            with self.subTest(linea=linea):
                self.assertEqual(ete.check_text(linea, self.patterns), [])

    def test_detecta_texto_incorrecto(self):
        malo = ("Utilizar el fichero para almacenar los datos, comenzando posteriormente el proceso "
                "de verificación del cable cuando sea necesario que el usuario lo requiera.")
        tipos = {k for k, _ in ete.check_text(malo, self.patterns)}
        self.assertTrue({"evitar", "gerundio", "longitud"} <= tipos, tipos)

    def test_detecta_sinonimos_concretos(self):
        casos = {
            "Utiliza el fichero.": ["utiliz", "fichero"],
            "Verifica la contraseña.": ["verific"],
            "Es necesario que reinicies el equipo.": ["es necesario que"],
        }
        for texto, esperados in casos.items():
            with self.subTest(texto=texto):
                msgs = " ".join(m.lower() for _, m in ete.check_text(texto, self.patterns))
                for e in esperados:
                    self.assertIn(e, msgs)

    def test_texto_correcto_sin_avisos(self):
        bueno = ("Apaga el ordenador. Quita el cable. Si el error continúa, reinicia el dispositivo. "
                 "Comprueba que el archivo esté en la carpeta.")
        self.assertEqual(ete.check_text(bueno, self.patterns), [])

    def test_no_marca_cuando_ni_comando(self):
        self.assertEqual([k for k, _ in ete.check_text("Cuando termine, escribe el comando.", self.patterns)
                          if k == "gerundio"], [])

    def test_codigo_se_ignora(self):
        texto = "Ejecuta `utilizando` esto.\n```\nutilizando fichero almacenando\n```\n"
        self.assertEqual(ete.check_text(texto, self.patterns), [])


if __name__ == "__main__":
    unittest.main()
