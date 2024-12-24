import os
import json
import unittest
import shutil
from localify import load_translations, set_language, l, set_missing_key_behavior

class TestLocalify(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crea una directory temporanea per le traduzioni
        cls.locales_path = os.path.join(os.path.dirname(__file__), 'temp_locales')
        os.makedirs(cls.locales_path, exist_ok=True)

        # File di traduzione EN
        en_translations = {
            "hello": "Hello",
            "world": "World"
        }
        with open(os.path.join(cls.locales_path, 'en.json'), 'w', encoding='utf-8') as f:
            json.dump(en_translations, f)

        # File di traduzione IT
        it_translations = {
            "hello": "Ciao",
            "world": "Mondo"
        }
        with open(os.path.join(cls.locales_path, 'it.json'), 'w', encoding='utf-8') as f:
            json.dump(it_translations, f)

        # Carica le traduzioni dalla directory temporanea
        load_translations(cls.locales_path)
        set_language('en')  # Imposta la lingua predefinita per i test

    @classmethod
    def tearDownClass(cls):
        # Rimuovi la directory temporanea
        if os.path.exists(cls.locales_path):
            shutil.rmtree(cls.locales_path)

    def setUp(self):
        # Reset delle configurazioni prima di ogni test
        set_language('en')
        set_missing_key_behavior('key')

    def test_basic_translation(self):
        message = l("hello").space().l("world").exclamation()
        self.assertEqual(str(message), "Hello World!")

    def test_switch_language(self):
        set_language('it')
        message = l("hello").space().l("world").exclamation()
        self.assertEqual(str(message), "Ciao Mondo!")

    def test_missing_key_default_behavior(self):
        message = l("nonexistent_key")
        self.assertEqual(str(message), "nonexistent_key")

    def test_missing_key_with_default_value(self):
        set_missing_key_behavior('default', default_value='[MISSING]')
        message = l("nonexistent_key")
        self.assertEqual(str(message), "[MISSING]")
