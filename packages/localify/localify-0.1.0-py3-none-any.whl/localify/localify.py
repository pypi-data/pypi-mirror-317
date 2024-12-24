import json
import os

# Dictionary for translations
_translations = {}

# Current language
_current_language = 'en'

def set_language(lang):
    global _current_language
    _current_language = lang

def load_translations(directory):
    global _translations
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            lang_code = os.path.splitext(filename)[0]
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                _translations[lang_code] = json.load(f)

class LocalifyString:
    def __init__(self, key=None):
        self.parts = []
        if key:
            self.add_key(key)

    def add_key(self, key):
        translated = _translations.get(_current_language, {}).get(key, key)
        self.parts.append(translated)
        return self  # Permette il chaining

    def __str__(self):
        return ''.join(self.parts)

    def __repr__(self):
        return str(self)

    def colon(self):
        self.parts.append(':')
        return self

    def space(self):
        self.parts.append(' ')
        return self

    def comma(self):
        self.parts.append(',')
        return self

    def period(self):
        self.parts.append('.')
        return self

    def exclamation(self):
        self.parts.append('!')
        return self

    def question(self):
        self.parts.append('?')
        return self

    def l(self, key):
        return self.add_key(key)

def l(key):
    return LocalifyString(key)
