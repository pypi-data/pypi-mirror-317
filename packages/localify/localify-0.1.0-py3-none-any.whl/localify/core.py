import logging
from .translation import LocalifyString
from .loaders import load_translations, translations_loaded

# Logging level constants
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

# Current language
_current_language = 'en'

# Missing key configuration
_missing_key_behavior = 'key'  # 'default', 'key', 'log'
_default_missing_value = None

# Logger for the package
_logger = logging.getLogger('localify')
_logger.addHandler(logging.NullHandler())  # Avoids "No handler found" warnings

# Indicates if load_translations has been called with a custom path
_custom_load_translations_called = False

def set_language(lang):
    """
    Set the current language. If translations have not been loaded,
    it loads them from the default path.
    Args:
        lang (str): The language code to set (e.g., 'en', 'it').
    """
    global _current_language
    _current_language = lang

    # Se le traduzioni non sono state caricate, caricale dal percorso di default
    if not translations_loaded():
        load_translations()
def set_missing_key_behavior(behavior, default_value=None):
    """
    Configure how to handle missing translation keys.

    Args:
        behavior (str): Behavior when a key is missing ('default', 'key', 'log').
        default_value (str, optional): Default value to use when behavior is 'default'.
    """
    global _missing_key_behavior, _default_missing_value
    if behavior not in ('default', 'key', 'log'):
        raise ValueError("Behavior must be 'default', 'key', or 'log'.")
    _missing_key_behavior = behavior
    _default_missing_value = default_value

def enable_logging(level=WARNING):
    """
    Enable logging for the localify package.

    Args:
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logging_level = _map_logging_level(level)
    _logger.setLevel(logging_level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

def _map_logging_level(level):
    """
    Map localify logging levels to the logging module levels.

    Args:
        level (int): Logging level constant from localify.

    Returns:
        int: Corresponding logging module level.
    """
    level_mapping = {
        DEBUG: logging.DEBUG,
        INFO: logging.INFO,
        WARNING: logging.WARNING,
        ERROR: logging.ERROR,
        CRITICAL: logging.CRITICAL
    }
    return level_mapping.get(level, logging.WARNING)

def config(
    language=None,
    missing_key_behavior=None,
    default_missing_value=None,
    logging_level=None
):
    """
    Configure various settings of the package.

    Args:
        language (str, optional): Language code to set (e.g., 'en', 'it').
        missing_key_behavior (str, optional): Behavior for missing keys ('default', 'key', 'log').
        default_missing_value (str, optional): Default value for missing keys when behavior is 'default'.
        logging_level (int, optional): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    if language:
        set_language(language)
    if missing_key_behavior:
        set_missing_key_behavior(missing_key_behavior, default_missing_value)
    if logging_level is not None:
        enable_logging(level=logging_level)

def l(key):
    """
    Start a new localized string with the given key.

    Args:
        key (str): The translation key.

    Returns:
        LocalifyString: An instance to build the localized string.
    """
    return LocalifyString(
        key,
        _current_language,
        _missing_key_behavior,
        _default_missing_value,
        _logger
    )
