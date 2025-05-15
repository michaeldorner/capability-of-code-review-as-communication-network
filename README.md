# The Capability of Code Review as Communication Network: Replication Package

[![GitHub](https://img.shields.io/github/license/michaeldorner/capability-of-code-review-as-communication-network)](./LICENSE)
[![GitHub Actions](https://github.com/michaeldorner/capability-of-code-review-as-communication-network/actions/workflows/test.yml/badge.svg)](https://img.shields.io/github/actions/workflow/status/michaeldorner/capability-of-code-review-as-communication-network/main.yml)
[![Codacy Badge](https://img.shields.io/codacy/grade/ef43d5d9b7c74ec0b211c03d91c448d8)](https://app.codacy.com/gh/michaeldorner/capability-of-code-review-as-communication-network/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://img.shields.io/codacy/coverage/ef43d5d9b7c74ec0b211c03d91c448d8)](https://app.codacy.com/gh/michaeldorner/information-diffusion-boundaries-in-code-review/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.8042256-blue)](https://doi.org/10.5281/zenodo.8042256)

Simulation code for the study ["The Capability of of Code Review as Communication Network"](https://arxiv.com)

## Introduction

The underlying idea of our *in-silico* experiment is, in principle, simple: We model different code review systems as communication networks and compute all minimal distances between all code review participants. The cardinality of reachable participants indicates how widely (RQ 1) information can spread, and distances between participants indicate how quickly (RQ~ 2) information can spread in code review. Since we used minimal paths and created the communication networks under best-case assumptions, the results describe the upper bound of information diffusion in code review.

Yet communication—and, by extension, information diffusion—is (1) inherently time-dependent and (2) not strictly bilateral, as code reviews often involve exchanges among more than two participants. As a result, traditional graphs are not well suited for modeling such interactions and tend to dramatically overestimate information diffusion [(Dorner et al. 2022)](https://dl.acm.org/doi/abs/10.1145/3544902.3546254). To address this, we use time-varying hypergraphs to model the communication network and to compute the shortest paths between all vertices. Hypergraphs generalize traditional graphs, allowing the use of standard algorithms such as Dijkstra’s for computing minimal-path distances. However, in time-varying hypergraphs, the distance between two vertices can be both topological (i.e., the fewest hops) and temporal (i.e., the shortest duration). This dual characterization enables us to answer RQ 2 by measuring both types of distance. Importantly, both topological and temporal distances yield the same set of reachable participants, which serves as the basis for answering RQ 1.

For more details on time-varying hypergraphs in general and modelling communication networks that emerges from code review with time-varying hypergraphs, have a look into [Dorner et al. 2022](https://dl.acm.org/doi/abs/10.1145/3544902.3546254) or our upcoming manuscript.

The extraction pipeline used to gather data from code review systems is maintained in a [separate repository](https://github.com/michaeldorner/code-review-to-communication-network). It supports both Gerrit-based (e.g., Android) and GitHub-based code review systems (e.g., Visual Studio Code and React). This separation ensures modularity and reusability of the data collection process. For implementation details and usage instructions, please refer to the dedicated extraction pipeline repository.

## Installation

The simulation requires Python 3.10 and higher. Due to the [significant performance improvements in Python 3.11](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-faster-cpython) and the heavy CPU workload in the simulation, Python 3.11 or higher is highly recommended!

The project depends on two external libraries: [`tqdm`](https://github.com/tqdm/tqdm) and [`pandas`](https://pandas.pydata.org). Install via

```bash
python3 -m pip install -r requirements.txt
```

For a faster initial loading of the communication network, you **can optionally** install `orjson` via pip:

```bash
python3 -m pip install orjson
```

If `orjson` is not installed, built-in [`json`](https://docs.python.org/3/library/json.html) encoder is used.

## Usage

To run the full simulation, use

```bash
python3 -m simulation.run
```

Please notice that depending on your hardware, the complete simulation may run several days and max out the CPU power. On a Apple MacBook M1 Max, it takes about three full days to complete. The simulations is highly parallelized which means: The more cores, the better/faster. We also recommend at least 64 GB of RAM and at least 12 GB available storage for storing the results.

The simulation provides options

- `--select <name 1> <name 2> ...` to select a subset of available code review networks
- `--vertex_dijkstra` to use a vertex-based implementation of Dijkstra's algorithm (which tends to be slower),
- `--num_processes` to limit the number of processes

For an overview of all options, use `python3 -m simulation.run --help`.

The code review communication networks are in the subfolder `data/networks`, the simulation results are stored in `data/minimal_paths`

## Tests

You can run all tests via

```bash
python -m unittest discover
```

The tests run also via [GitHub Actions](https://github.com/michaeldorner/capability-of-code-review-as-communication-network/actions). 

## Verification and Traceability

### Verification

To verify the your results with our [results](https://doi.org/10.5281/zenodo.7898863), compare the MD5 hashes of your results (for example, via `md5 ./data/minimal_distances/.*bz2` on macOS or `md5sum ./data/minimal_distances/.*bz2` on Linux) with the following MD5 hashes.

```
trivago.pickle.bz2 	 64c97c8ddb1e67cb70bfe297ad81c4ed
trivago.csv.bz2 	 a5e1a6d5230ac8c1888a711bd91f0420
spotify.pickle.bz2 	 c434b887fcf449dc7195cc428260b35c
spotify.csv.bz2 	 259532c46779df2702bcff0fa6c7932f
microsoft.pickle.bz2 	 f5b0beb747705fe3fcf4a84191bba937
microsoft.csv.bz2 	 08e93558473fb2b0a00de90e608901a3
```

We also provide a minimal unittest that compares the hashes from Zenodo. It requires `requests` (install via `pip3 install requests`) and a [Zenodo access token](https://zenodo.org/account/settings/applications/tokens/new/). Run the unit test with the following command:

```bash
export ZENODO_TOKEN=<insert token here>
python3 -m unittest tests/test_results.py
```

Please notice: This simulation uses [Pickle Protocol version 5](https://peps.python.org/pep-0574/). Future protocol versions may produce different hashes if the internals change. `.csv` files, however, must produce always the same hashes.

### Tracebility

To ensure traceability between the simulation results and the figures presented in the article, all simulation outputs are exported as `.csv` or `.tex` files. These files are then used directly for generating plots and figures included in the article using [Ti*k*Z](https://tikz.dev/dv-formats), reducing the possibility of manual errors or data mismatches. This approach maintains a clear, reproducible link between the raw simulation data and the final published results. For further details, see the `reports` folder.

## Visualization

Because of the large runtime of the simulation, we provide precomputed results of the simulation via [Zenodo](https://doi.org/10.5281/zenodo.7898863). You can download the results and place the `.pickle` and `.csv` files in the subfolder `data/minimal_paths`. Consider verify the `.pickle` and `.csv` files (see [Verification](#verification)).

To visualize the results and reproduce the tables and figures of the publication, see the Jupyter notebooks in the subfolder `notebooks/`.

## Credits

Thanks a lot

- [Andreas Bauer](https://github.com/andreas-bauer) for your valuable feedback in countless discussion.
- Students of the course *Software Testing* in 2023 for their extraordinary efforts on testing this project.

## License

Copyright © 2025 Michael Dorner

This work is licensed under [MIT license](LICENSE).
