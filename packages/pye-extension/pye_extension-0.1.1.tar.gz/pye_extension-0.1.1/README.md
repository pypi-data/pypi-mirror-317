# Universal Python Code Obfuscator & VM Loader

This repo proposes using an **obfuscation and encryption approach** for Python code.

## Understanding Python Bytecode Vulnerabilities

### Structural Transparency

* Preservation of function signatures and class hierarchies
* Retention of original control flow patterns
* Maintained symbol references and name bindings

### Decompilation Vulnerabilities

* Deterministic bytecode generation patterns
* Preserved type information and annotations
* Recoverable import hierarchies

## Why PyE?

Standard Python bytecode (.pyc files) is easily decompilable due to several inherent limitations:

* Multi-layered protection strategy
* Advanced encryption techniques
* Custom execution environment

## Inspiration 
Common Vulnerabilities in Open Source AI packages: 

* Easily bypassed safety checks
* Modifiable content filters
* Exposed prompt sanitization

### Critical Protection Needs

* Model interaction guardrails
* Input/output filtering logic
* Usage tracking mechanisms
* Security parameter preservation

## Installation & Usage

### Installation

`pip install pye-extension`

### Basic Usage

#### Compile your sensitive Python file:

`pyehandler compile your_script.py`

### Limitations

* While significantly more secure than .pyc, no protection is unbreakable. **DO NOTE THIS IS EXTREMELY IMPORTANT**
* Performance may be slower
* Debug information is limited in protected modules

## License
Proprietary - All Rights Reserved
Copyright (c) 2024 oha