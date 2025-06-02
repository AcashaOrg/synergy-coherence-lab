# Synergy Coherence Lab

[![CI](https://github.com/AcashaOrg/synergy-coherence-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/AcashaOrg/synergy-coherence-lab/actions/workflows/ci.yml)

Synergy Coherence Lab is a lightweight research repository exploring the concept of **synergy Φ (phi)**.  It hosts the `synergy_phi` Python package, example notebooks and documentation used for experimenting with metrics such as Integrated Information and dyadic synergy.
For a NotebookLM Audio Overview see: https://notebooklm.google.com/notebook/7051fac9-90c1-45fe-a53d-6db17bf6d724/audio

The repository includes:

- **`synergy_phi` package** – a minimal library with a command line interface.
- **Jupyter notebooks** – demonstrations like `synergy_coherence_analysis.ipynb` for computing HRV‑based metrics.
- **Documentation site** – generated with [MkDocs](https://www.mkdocs.org/).
- **`phi_Entry_001.md`** – a journal entry describing a mutual recognition protocol between AI systems.

## Quick Start

```bash
pip install .
synergy-phi
```

```python
from synergy_phi import hello
print(hello())
```

## Command Line Usage

After installation the `synergy-phi` command is available:

```bash
synergy-phi
```

## Repo Layout

- `src/synergy_phi/`: Library code
- `notebooks/`: Jupyter demo notebooks
- `examples/`: CLI examples
- `docs/`: MkDocs documentation
- `tests/`: Unit tests (pytest)
- `phi_Entry_001.md`: Research journal entry
