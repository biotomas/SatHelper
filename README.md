SatHelper
=========

This is a tool to improve the Boolean satisfiability (SAT) solver user's life.

It helps you model various problems as SAT.

See the examples to learn how to use it.

Install
=======

```bash
pip install .
```

Usage
=====

Simply use the public instance `sh` of the module.

```python
from SatHelper import sh

sh.declareVariable('A')
sh.printFormula()
```
