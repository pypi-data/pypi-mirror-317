# dsl_dict_analyser

A Python package for analysing dsl dictionaries. Dsl dictionary is a dict type for lingvo app.

## Installation

You can install the package using pip:

```bash
pip install dsl_dict_analyser
```
## Usage

```python

from dsl_dict_analyser import read
# Read the DSL dictionary file
dsl_dict = read("path/to/dsl_dict.txt")
# then your can read the dsl_dict
# like dsl_dict.cards
# or dsl_dict.name
```
## Changelog

### 0.0.1 (2024-12-11)
-  Initial release

### 0.0.2-4 (2024-12-11)
- add ci/cd
- fix some language dict bug.(deu dict name format error)

### 0.0.5 (2024-12-26)
- fix a p bug