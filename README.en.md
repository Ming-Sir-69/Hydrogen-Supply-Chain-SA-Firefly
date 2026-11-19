<picture>
  <source media="(prefers-color-scheme: dark)" srcset="readme-assets/cover-en-dark.png">
  <img src="readme-assets/cover-en-light.png" alt="Four hydrogen supply-chain cost models, twelve initial candidates and stochastic annealing search" width="100%">
</picture>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="实验数据.zip">Experiment archive</a> ·
  <a href="文件夹结构.txt">Structure notes</a> ·
  <a href="https://github.com/Ming-Sir-69">Author</a>
</p>

<p align="center">
  <img alt="Source license not specified" src="https://img.shields.io/badge/source%20license-not%20specified-F6C555?style=flat-square&labelColor=2E2A26">
  <a href="readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md"><img alt="Documentation license MIT" src="https://img.shields.io/badge/documentation%20license-MIT-F6C555?style=flat-square&labelColor=2E2A26"></a>
  <img alt="Python 3" src="https://img.shields.io/badge/python-3-6B655C?style=flat-square&labelColor=2E2A26">
  <img alt="NumPy required" src="https://img.shields.io/badge/dependency-NumPy-6B655C?style=flat-square&labelColor=2E2A26">
  <img alt="4 models" src="https://img.shields.io/badge/models-4-A8A196?style=flat-square&labelColor=2E2A26">
</p>

<p align="center">
  <a href="README.md">简体中文</a> · <b>English</b>
</p>

# Hydrogen Supply-Chain Cost Models: Simulated-Annealing Firefly Search

This project uses a discrete simulated-annealing firefly algorithm to search for low-cost combinations of hydrogen production and transport. Four production methods and three transport methods form 12 candidates. Four cost and subsidy models use the same search engine. The historical Excel archive was not regenerated with the hybrid algorithm and does not establish policy effects.

## Features

- **Four objective functions**: cost without subsidy, direct financial subsidy, proportional cost sharing, and environmental cost with a green subsidy.
- **Discrete candidate search**: choices among Green, SMR, ATR and CCS, and among Pipeline, Truck and LiquefiedTruck; production and transport quantities remain fixed during the main search.
- **Temperature and stopping controls**: initial temperature from a typical uphill cost and a target acceptance probability, followed by cooling for at most 1000 iterations. The search stops early after 200 iterations without improvement.
- **Two entry types**: Python entries print the search directly; MATLAB entries call Python modules in the corresponding directory through `py.*`<sup>[[2]](#references)</sup>.
- **Historical experiment archive**: 209 XLSX files grouped from model0 through model3; their contents have not been independently rebuilt and checked with the current code.

| Model | Objective | Initial production (kg) | Pipeline distance (km) |
|---|---|---:|---:|
| [model0](model0/) | Production cost + transport cost | 1350 | 2500 |
| [model1](model1/) | model0 − direct financial subsidy | 450 | 2500 |
| [model2](model2/) | model0 × (1 − cost-sharing ratio) | 2250 | 2500 |
| [model3](model3/) | model0 + environmental cost − green subsidy | 1350 | 2400 |

## Quick start

Install Python 3 and NumPy<sup>[[1]](#references)</sup>. The repository has no dependency lockfile, automated test suite or continuous-integration configuration. Run all four Python entries from the repository root:

```sh
python3 -c 'import numpy'
for model in 0 1 2 3; do
  (cd "model${model}" && python3 -B "simulated_annealing_firefly_model${model}.py" --seed 7)
done
```

All four Python entries were exercised. Use `--seed` for a repeatable random sequence. Without it, the search trajectory can vary between runs.

To run one model, enter its directory and invoke its entry, for example:

```sh
cd model0
python3 -B simulated_annealing_firefly_model0.py --seed 7
```

## Usage

### Change model inputs

Each model directory has an `initialize_parameters.py` containing production quantity, transport distances, unit costs, environmental costs and subsidy parameters. Transport quantity is fixed at `3/5` of production quantity. Truck and liquefied-truck distances are `3/5` and `2.6/5` of pipeline distance. These values are embedded inputs; the repository includes neither their data sources nor calibration records.

`calculate_fitness_model*.py` defines the objective and `simulated_annealing_firefly_model*.py` runs the search. After changing inputs, run from the corresponding model directory so that modules with identical names are not loaded from another directory.

### MATLAB entries

Each model includes `matlab_script_model*.m` and `matlab_script_model*_modified.m`. Both script types hard-code a Windows Python 3.11 executable path. Before running, set the local interpreter with `pyenv` and check the current directory and Python module search path<sup>[[2]](#references)</sup>.

The modified scripts also write Excel files, generate statistical plots and assume that `../实验数据/<model>/` and `optimal_solutions/` output directories exist. The repository supplies only the compressed archive, not these expanded directories. MATLAB versions, toolbox dependencies and the modified output workflow were not verified in this review.

## Design

1. Each candidate contains production and transport methods with fixed quantities. Lower cost means a brighter firefly.
2. Each candidate chooses a random brighter peer with the same quantities from the previous population. Distance `d` is the fraction of differing method fields. Each differing field can copy the peer with probability `β₀ exp(−γd²)`. Without a brighter peer, attraction is skipped.
3. Each method field may mutate independently; production and transport quantities stay fixed.
4. A proposal that does not raise cost is accepted. An increase `Δ` is accepted with probability `exp(−Δ/T)`. Initial temperature uses the median positive cost increase from single-field changes; each iteration multiplies temperature by a factor below 1. The best solution is stored separately from the population.

See the references for firefly attraction and simulated annealing<sup>[[3]](#references)[[4]](#references)</sup>. This implementation adapts the ideas to categorical choices; it does not reproduce continuous position updates verbatim.

## Limitations

- The default population already contains all 12 combinations, so enumeration gives the exact minimum. For each of the four models, 10 random seeds recovered the enumerated minimum from a population with all optimal candidates removed. This is not a performance comparison with enumeration or a convergence claim for larger problems.
- In model3, transport environmental cost is multiplied by transport quantity without distance, inconsistent with the parameter comment's unit of CNY/kg/km.
- Cost, environmental-cost and subsidy parameters have no documented sources. The Excel archive has not been independently rebuilt and is not a verified research result.
- MATLAB scripts contain machine-specific paths and output-directory assumptions. Their compatibility was not verified in this environment. The legacy reporting loops repeat the final fitness after Python returns; they do not show the actual search trajectory.

## Development

The four models share `annealing_firefly.py` and retain their own cost functions and Python/MATLAB entry points. The repository has no distribution package or continuous integration. The committed `__pycache__/` files are historical caches, not source.

[Structure notes](文件夹结构.txt) describe the directories, and the [experiment archive](实验数据.zip) retains historical XLSX files. See the [personal documentation license](readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md) for the documentation licensing scope.

## Acknowledgements

- NumPy provides random-candidate generation and numerical interfaces<sup>[[1]](#references)</sup>.
- MathWorks documents Python-environment configuration in MATLAB<sup>[[2]](#references)</sup>.
- The cover illustration was generated with an image-generation model and processed by this project.

## References

1. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362. <https://doi.org/10.1038/s41586-020-2649-2>
2. MathWorks. *pyenv — Change default environment of Python interpreter*, R2026b. <https://www.mathworks.com/help/matlab/ref/pyenv.html>

3. Yang, X.-S. (2009). Firefly Algorithms for Multimodal Optimization. *Stochastic Algorithms: Foundations and Applications*, 169–178. Springer. <https://doi.org/10.1007/978-3-642-04944-6_14>
4. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by Simulated Annealing. *Science*, 220(4598), 671–680. <https://doi.org/10.1126/science.220.4598.671>

## Repository structure

| Path | Contents |
|---|---|
| `annealing_firefly.py` | Shared discrete search engine |
| `model0/` | Production and transport cost model without subsidy, with entries |
| `model1/` | Direct financial subsidy model and entries |
| `model2/` | Proportional cost-sharing model and entries |
| `model3/` | Environmental-cost and green-subsidy model and entries |
| `实验数据.zip` | 209 historical XLSX files and directory entries |
| `文件夹结构.txt` | Original directory notes |
| `readme-assets/` | Covers, themed headers, signature assets and documentation license |

---

Maintained by <picture><source media="(prefers-color-scheme: dark)" srcset="readme-assets/em-logo-dark.svg"><img src="readme-assets/em-logo-light.svg" alt="EM" height="13"></picture> <b>EricMingle69</b> · <a href="https://github.com/Ming-Sir-69">Ming-Sir-69</a><br>
The root provides no unified license for source code, existing data or third-party materials; reuse and redistribution rights require separate confirmation. The existing licensing scope for original wording in this documentation refresh is given in the [personal documentation license](readme-assets/PERSONAL-DOCUMENTATION-LICENSE.md).
