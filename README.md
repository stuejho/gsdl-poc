# GSDL

## Developer Requirements

- Python 3.12 or greater
- Poetry

## Developer Setup

Python and Poetry are both required for development. Python is used to
run code and tests. Poetry is used for dependency and package management.

### Conda/Mamba Environment

Create a Conda or Mamba environment using [environment.yml](/environment.yml).

`environment.yml` includes the following information:

- Environment name: `gsdl`
- Environment dependencies: Python and Poetry

These tools are available in many distributions, including the following:

- [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) provides a
  minimal installer for Conda.
- [Miniforge](https://github.com/conda-forge/miniforge) provides a minimal
  installer for Conda and Mamba.

[Miniforge](https://github.com/conda-forge/miniforge) 

#### Option 1: Create and activate an Environment with Conda

```shell
conda env create --file=environment.yml
conda activate gsdl
```

#### Option 2: Create and activate an Environment with Mamba

```shell
mamba env create --file=environment.yml
mamba activate gsdl
```

### Poetry

This project uses Poetry to manage package dependencies.

Install dependencies with the command below:

```shell
poetry install
```
