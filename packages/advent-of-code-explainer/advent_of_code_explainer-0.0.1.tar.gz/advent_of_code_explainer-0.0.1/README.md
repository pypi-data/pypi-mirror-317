# [advent-of-code-explainer](https://github.com/Skenvy/advent-of-code-explainer)

> [!CAUTION]
> Very WIP PoC. The goal is to eventually be an app that can be used to answer / explain Advent of Code puzzles, but the primary utility for myself making this, is to experiment with setting up a deployment of a package that is then also used in a deployment of a pyscript-centric static site. As part of the PoC, to figure out and eventually understand how best to glue these two intents together (package, that can be used in a pyscript page), this wont yet resemble what it eventually should.

TODO SHORT DESCRIPTION
## Getting Started
[To install the latest from pypi](https://pypi.org/project/advent-of-code-explainer/);
```sh
pip install advent-of-code-explainer
```
## Usage
TODO LONG DESCRIPTION
### `example.function(~)`
`(a:string, b:int=2, c:string='a')`
```python
>>> import advent_of_code_explainer
>>> # What is this
>>> example.function('example input')
'ye'
```
## [Sphinx+MyST generated docs](https://skenvy.github.io/advent-of-code-explainer/)
## Developing
### The first time setup
```
git clone https://github.com/Skenvy/advent-of-code-explainer.git && cd advent-of-code-explainer/pkg && make setup
```
### Iterative development
* `make build` will test and build the wheel and force reinstall it into the local venv, to test the built distribution
## [Open Source Insights](https://deps.dev/pypi/advent-of-code-explainer)
