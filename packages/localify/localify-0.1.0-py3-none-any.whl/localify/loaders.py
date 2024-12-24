import os
import json

try:
    import yaml
except ImportError:
    yaml = None

# Dictionary to hold translations
_translations = {}
_translations_loaded = False  # Indicates if translations have been loaded
_custom_load_translations_called = False  # Indicates if load_translations() was called with a custom path

def translations_loaded():
    """
    Check if translations have been loaded.

    Returns:
        bool: True if translations are loaded, False otherwise.
    """
    return _translations_loaded

def get_translations():
    """
    Get the loaded translations.

    Returns:
        dict: The translations dictionary.
    """
    return _translations

def load_translations(directory=None):
    """
    Load translations from the specified directory.

    Args:
        directory (str, optional): Path to the translations directory.
    """
    global _translations, _translations_loaded, _custom_load_translations_called
    _translations = {}
    _translations_loaded = False

    if directory is None:
        directory = os.path.join(os.getcwd(), 'locales')
    else:
        _custom_load_translations_called = True

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Translations directory '{directory}' does not exist.")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            lang_code, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == '.json':
                data = _load_json(file_path)
            elif ext in ['.yaml', '.yml']:
                if yaml is None:
                    raise ImportError("The 'pyyaml' module is not installed. Install it to use YAML files.")
                data = _load_yaml(file_path)
            else:
                continue  # Ignore unsupported files

            # Merge translations for the language
            if lang_code in _translations:
                _translations[lang_code].update(data)
            else:
                _translations[lang_code] = data

    _translations_loaded = True

def _load_json(file_path):
    """
    Load translations from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Translations loaded from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _load_yaml(file_path):
    """
    Load translations from a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Translations loaded from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
