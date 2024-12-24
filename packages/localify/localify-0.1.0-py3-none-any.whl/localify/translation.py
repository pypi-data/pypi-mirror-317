class LocalifyString:
    """
    Class to build localized strings.

    Attributes:
        parts (list): List of string parts that make up the final string.
        language (str): Current language code.
        missing_behavior (str): Behavior when a key is missing.
        default_missing_value (str): Default value for missing keys.
        logger (logging.Logger): Logger instance for logging warnings.
    """

    def __init__(self, key=None, language='en', missing_behavior='key', default_missing_value=None, logger=None):
        self.parts = []
        self.language = language
        self.missing_behavior = missing_behavior
        self.default_missing_value = default_missing_value
        self.logger = logger
        if key:
            self.add_key(key)

    def add_key(self, key):
        """
        Add a translated key to the string.

        Args:
            key (str): The translation key to add.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        from .loaders import get_translations  # Delayed import to avoid circular dependencies
        translations = get_translations()
        lang_translations = translations.get(self.language, {})
        if key in lang_translations:
            translated = lang_translations[key]
        else:
            translated = self._handle_missing_key(key)
        self.parts.append(translated)
        return self  # Allows chaining

    def _handle_missing_key(self, key):
        """
        Handle missing translation keys based on the configured behavior.

        Args:
            key (str): The missing translation key.

        Returns:
            str: The string to use for the missing key.
        """
        if self.missing_behavior == 'default':
            return self.default_missing_value or ''
        elif self.missing_behavior == 'key':
            return key
        elif self.missing_behavior == 'log':
            if self.logger:
                self.logger.warning(f"Missing translation key '{key}' for language '{self.language}'.")
            return key
        else:
            # Fallback behavior
            return key

    def __str__(self):
        return ''.join(self.parts)

    def __repr__(self):
        return str(self)

    # Methods to add punctuation and spaces
    def colon(self):
        """
        Add a colon ':' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append(':')
        return self

    def space(self):
        """
        Add a space ' ' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append(' ')
        return self

    def comma(self):
        """
        Add a comma ',' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append(',')
        return self

    def period(self):
        """
        Add a period '.' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append('.')
        return self

    def exclamation(self):
        """
        Add an exclamation mark '!' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append('!')
        return self

    def question(self):
        """
        Add a question mark '?' to the string.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        self.parts.append('?')
        return self

    # Method to add another translated key
    def l(self, key):
        """
        Add another translated key to the string.

        Args:
            key (str): The translation key to add.

        Returns:
            LocalifyString: The instance itself for chaining.
        """
        return self.add_key(key)
