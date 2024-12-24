![Localify Logo](assets/logo.png)

# Localify

Localify is a lightweight, easy-to-use internationalization (i18n) package for Python. It provides a simple and efficient way to manage translations for applications, supporting JSON and YAML formats.

---

## Features

- **Easy-to-use syntax**: Build localized strings with chainable methods.
- **Customizable missing key behavior**: Choose between showing the key, a default value, or logging a warning.
- **JSON and YAML support**: Load translations from both formats.
- **Dynamic configuration**: Adjust settings like language, logging levels, and missing key behavior on the fly.

---

## Installation

### From PyPI

To install Localify from PyPI:

```bash
pip install localify
```

### From Source
To Install the package locally:
1. Clone the repository:
```bash
git clone https://github.com/felicedev/localify.git
cd localify
```

2. Install in editable mode:
```bash
pip install -e .
```

---

## Usage

Here are some examples to help you get started with Localify.

### 1. Setting up translations

Make sure you have a `locales/` directory in your project root with JSON or YAML files for your translations.

**Example: `/locales/en.json`**

```json
{
    "hello": "Hello",
    "world": "World",
    "greeting": "Greetings"
}
```

**Example: `/locales/it.json`**

```json
{
    "hello": "Ciao",
    "world": "Mondo",
    "greeting": "Saluti"
}
```

### 2. Basic usage
```python
from localify import l, config

# Configure the package
config(
    language='en',  # Set the language
    missing_key_behavior='key',  # Show the key if a translation is missing
    logging_level=30  # Set logging to WARNING
)

# Create localized strings
message = l("hello").space().l("world").exclamation()
print(message)  # Output: Hello World!

# Switch to Italian
config(language='it')
print(l("hello").space().l("world").exclamation())  # Output: Ciao Mondo!
```
---

## Methods

The `l` function returns a `LocalifyString` object that lets you chain methods to build localized strings.

### Methods for Building Strings

| Method        | Description                                   | Example                               |
|---------------|-----------------------------------------------|---------------------------------------|
| `l(key)`      | Adds a localized translation for the given key. | `l("hello").space().l("world")`      |
| `space()`     | Adds a space.                                 | `l("hello").space()`                 |
| `colon()`     | Adds a colon `:`.                             | `l("key").colon()`                   |
| `comma()`     | Adds a comma `,`.                             | `l("key").comma()`                   |
| `period()`    | Adds a period `.`.                            | `l("key").period()`                  |
| `exclamation()` | Adds an exclamation mark `!`.               | `l("key").exclamation()`             |
| `question()`  | Adds a question mark `?`.                     | `l("key").question()`                |

### Configuration Methods

| Function                   | Description                                                   |
|----------------------------|---------------------------------------------------------------|
| `config()`                 | Configure language, logging, and missing key behavior.        |
| `set_language(lang)`       | Set the current language.                                     |
| `set_missing_key_behavior(behavior, default_value)` | Set how missing keys are handled (`'key'`, `'default'`, or `'log'`). |
| `enable_logging(level)`    | Enable logging with a specific level (`DEBUG`, `INFO`, etc.). |

---

## Missing Key Behavior

Localify allows you to configure how missing translation keys are handled. Use the `set_missing_key_behavior()` function or the `config()` function to customize this.

### Options

1. **`'key'` (Default)**: Show the missing key as-is.
2. **`'default'`**: Show a default value if provided.
3. **`'log'`**: Log a warning message and show the missing key.

### Example

```python
from localify import config, l

# Show a default value for missing keys
config(missing_key_behavior='default', default_missing_value='[NOT FOUND]')
print(l("missing_key"))  # Output: [NOT FOUND]

# Log a warning for missing keys
config(missing_key_behavior='log')
print(l("missing_key"))  # Output: missing_key (and logs a warning)
```

---

## Advanced Configuration

### Loading Custom Translations

You can load translations from a custom directory using `load_translations()`:

```python
from localify import load_translations, set_language, l

# Load translations from a custom directory
load_translations('path/to/custom_locales')
set_language('en')

print(l("custom_key"))  # Output depends on your custom translations
```

### Logging Configuration
Localify integrates with Python’s logging module. You can enable and configure logging as follows:

```python
from localify import enable_logging, DEBUG

# Enable debug logging
enable_logging(level=DEBUG)
```

---

## Roadmap

### Completed
- [x] JSON support for translations.
- [x] Chainable methods for building localized strings.
- [x] Dynamic configuration of language and behavior.
- [x] Basic logging integration.
- [x] Unit tests for core functionality.

### In Progress
- [ ] Support for YAML translation files.
- [ ] Enhanced error handling for missing translations.

### Planned
- [ ] Add support for `.po` and `.mo` translation files.
- [ ] Implement dynamic locale reloading without restarting the application.
- [ ] Create a CLI tool for managing translations.
- [ ] Translation validation tool to check for missing keys across locales.
- [ ] Add documentation generation for translation files.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


## Contributing

Contributions are welcome! Feel free to submit issues or pull requests on [GitHub](https://github.com/felicedev/localify/issues).
