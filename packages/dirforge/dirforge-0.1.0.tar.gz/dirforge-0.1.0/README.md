# DirForge 🌳

[![PyPI version](https://badge.fury.io/py/DirForge.svg)](https://badge.fury.io/py/DirForge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DirForge is a powerful Python utility that automatically creates directory structures and files from tree-like text representations. Perfect for quickly scaffolding projects, replicating project structures, or setting up standardized directory layouts.

## 🚀 Features

- Create entire directory structures from text-based tree representations
- Accurately handles nested directories and files
- Preserves file extensions and special filenames (like `__init__.py`)
- Supports standard tree visualization symbols (├, └, │)
- Clean and intuitive command-line interface
- Zero external dependenciesM 

## 📦 Installation

```bash
pip install DirForge
```

## 🎯 Usage

1. Create a text file (e.g., `tree.txt`) with your desired directory structure:

```
my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
└── requirements.txt
```

2. Run DirForge:

```bash
DirForge tree.txt
```

That's it! Your directory structure will be created automatically.

## 🛠️ Technical Details

DirForge uses a depth-first approach to parse and create directory structures:

- Calculates directory depth using indentation and tree symbols
- Maintains a path stack to track the current position in the directory hierarchy
- Handles both files and directories intelligently based on file extensions
- Creates parent directories automatically when needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for quick project scaffolding
- Built with love for the Python community