# In-NetRoadmap
This repository refers to the framework presented by "Da Teoria `a Implantação: Um Framework Metodológico para
In-Network Machine Learning em Redes Programáveis". It provides a CLI interface that researchers can use to easily train supported ML models, map them to the programmable switch pipeline and provision an experimental virtual environment.

## Pre-requisites
Because this project uses legacy ansible resources for an old vagrant box, it is required that the framework is installed under a **Python 3.9 virtual environment**. A recommended tool for creating legacy python venvs is [Pyenv](https://github.com/pyenv/pyenv). All of the framework's dependencies are handled by pip.

## Installation
The framework can be installed in development mode via pip. Dependencies are handled automatically.

```bash
git clone https://github.com/ifpb/in-netroadmap
cd in-netroadmap
pip install -e .
```
