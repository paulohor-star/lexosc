import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

CATALOGO = Path(__file__).resolve().parents[1] / 'data' / 'catalogo_inicial.json'

class CatalogoInicialTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.normas = json.loads(CATALOGO.read_text(encoding='utf-8'))

    def test_ids_unicos(self):
        ids = [n['id'] for n in self.normas]
        self.assertEqual(len(ids), len(set(ids)))

    def test_urls_https(self):
        for norma in self.normas:
            url = urlparse(norma['official_url'])
            self.assertEqual(url.scheme, 'https')
            self.assertIn(url.hostname, ['www.planalto.gov.br','www.tce.pr.gov.br'])

    def test_escopo_inicial(self):
        self.assertTrue(any(n['sphere'] == 'federal' for n in self.normas))
        self.assertTrue(any(n.get('uf') == 'PR' for n in self.normas))

if __name__ == '__main__':
    unittest.main()
