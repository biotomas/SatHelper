SatHelper
=========

This is a tool to improve the Boolean satisfiability (SAT) and MaxSAT solver user's life.

It helps you model various problems as SAT and MaxSAT.

See the examples in the 'examples' folder to learn how to use it.


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

In order to use the `solveSat` and `solveMaxSat` methods you need to
download a SAT and MaxSAT solver and place it in the folder from where
you execute the python script.

For SAT solving we recommend [Glucose](https://www.labri.fr/perso/lsimon/glucose/).
Download it, compile it, and rename it to `glucose`

For MaxSAT solving we recommend Open-WBO. You can get it from the
[MaxSAT Competition homepage](https://maxsat-evaluations.github.io/2021/mse21-solver-src/complete/open-wbo-res.zip).
Download it, compile it, and rename it to `open-wbo`

Other SAT and MaxSAT solver that follow the standard input and output format should work as well.

