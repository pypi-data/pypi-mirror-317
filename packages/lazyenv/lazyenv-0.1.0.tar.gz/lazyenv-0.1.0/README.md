# ![LazyEnv Logo](https://raw.githubusercontent.com/Valmont-Coding/lazy-env/main/assets/logo.png) LazyEnv

![Python Version](https://img.shields.io/badge/python->=3.8-blue)
![License](https://img.shields.io/github/license/Valmont-Coding/lazy-env)
![PyPI Version](https://img.shields.io/pypi/v/lazyenv)

## 📚 Overview

LazyEnv is a Python library designed to simplify managing environment variables. It loads project-specific `.env` files and/or global enviroment variables and provides a convenient way to access these variables using dot notation.

## 🚀 Features

### Implemented
- Load project-specific `.env` files and/or global enviroment variables.
- Dot notation/IntelliSense access for environment variables. 
- Command-line interface (CLI) tool (`lazyenv init`) to initialize the dot-accessible variable file automatically.


### Planned
- Fuzzy search/lookup for environment variables if not using cli.
- Option to sync enviroment variables after changing them.

## 📦 Installation

```bash
pip install lazyenv
```

## 🛠️ Usage

### Dot Notation Access

To use dot notation access, initialize your environment variables using:

```bash
$ lazyenv init
```
Then, you can access environment variables in your Python script as follows:

```python
from lazyenv import env
print(env.API_KEY)
```

### Advanced CLI Usage
By default, the local .env file is searched for and loaded, but it is possible to change this behavior.

Include global enviroment variables:
```bash
$ lazyenv init --incl-global
```
The arguments can also be shortened and local variables can be excluded:
```bash
$ lazyenv init -g -l False
```

## 📚 Roadmap

- [x] Load `.env` files and/or global enviroment variables.
- [x] Dot notation access for environment variables.
- [ ] Fuzzy search/lookup functionality.
- [ ] Sync feature.

## 📌 Contributing

Contributions are welcome!

## 👥 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Inspired by the projects [python-dotenv](https://github.com/theskumar/python-dotenv) and [python-decouple](https://github.com/HBNetwork/python-decouple).

## 🤝 Contact

- GitHub: [@Valmont-Coding](https://github.com/Valmont-Coding)