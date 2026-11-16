<<<<<<< HEAD
# Worked solutions of the M1 coursework 2026-27

<<<<<<< HEAD
One Python script per step, `step1.py` to `step4.py`, run with the seed 0 of the handout. Your
results for the network, the clusters and the maps can differ a little from these, since they also
depend on your code, on the versions of the libraries and on your machine; the other values should
agree to the figures shown. Each script prints the rows of the results table it
answers (`row 2.1a: 1`), saves its figures in `figures/` and its files in `outputs/`;
`results_table.xlsx` is the results table filled in with these values.

| File | What it is |
|---|---|
| `step1.py` | step 1: the learning set, the four features, the labels that contradict the physics, the inputs |
| `step2.py` | step 2: the linear classifier, its penalty, its weights, gradient descent and Nesterov's momentum |
| `step3.py` | step 3: the two networks (PyTorch), the labels they contradict, the suspects |
| `step4.py` | step 4: principal components, the maps, the clusters, the breakups of the catalogue |
| `common.py` | what the scripts share: the data, the inputs, the features, the score, the DMD rate, the table rows |
| `data/` | the two data files you received |
| `assignment.pdf` | the handout as you received it |
| `check_submission.py` | the self-check script as you received it |
| `outputs/` | the three CSV files the solution hands in, and the rows each script printed |
| `figures/` | the figures the scripts save |
| `requirements.txt` | the packages and versions the scripts ran with |
| `walkthrough.ipynb` | the answers question by question (goal, calculation, result); runs the four scripts in place, about six minutes |

## How to run

Python 3.10, 3.11 or 3.12 with the packages of `requirements.txt` (the pinned torch has no wheels for
later Python versions or for Intel Macs; PyTorch is used in step 3 only). From this folder:

    python3 step1.py      # about 10 s
    python3 step2.py      # about 2 min
    python3 step3.py      # about 3 min
    python3 step4.py      # about 2 min

Each script finds the data in `data/` and the helper beside it, and rewrites its files in
`outputs/` and `figures/`.
=======
> **Author:** Siah Yee Long

---

## Python Version & Compatibility

- **Target / Tested Version:** **Python 3.13** (specifically `3.13.16`)
- **Backward Compatibility:** **Python >= 3.12** (Python 3.12 and Python 3.13)
- **Compatibility Note on Python <= 3.11:**
  Several core dependencies in `requirements.txt` strictly require Python 3.12 or higher:
  - `numpy==2.5.4` (`>=3.12`)
  - `scipy==1.18.1` (`>=3.12`)
  - `contourpy==1.4.0` (`>=3.12`)
  - `networkx==3.7` (`>=3.12`)

  Therefore, the pinned environment **cannot** be installed on Python 3.11 or older without downgrading these packages. Python 3.13 is strongly recommended. (Note: `check_submission.py` standalone requires only Python >= 3.8, but full coursework execution depends on `requirements.txt`).

---

## Environment Setup

### Option 1: Automated Setup (Recommended)

From the repository root, source `setup_env.sh` in **bash** or **zsh**:

```bash
source setup_env.sh
```

*(Note: the script must be sourced with `source` or `.`, not executed as `./setup_env.sh`, so it can activate the virtual environment in your current shell).*

#### What `setup_env.sh` does:
1. **Detects Python 3.13** (with fallback to Python 3.12 if 3.13 is not in PATH).
2. **Creates/validates `.venv`**: If an existing `.venv` was built with an incompatible Python version, it is automatically rebuilt with the matching interpreter.
3. **Activates `.venv`** in the current shell.
4. **Installs dependencies** from `requirements.txt` along with `ipykernel`. Subsequent runs skip re-installation unless `requirements.txt` is modified (tracked via `.venv/lock.stamp`).
5. **Registers a Jupyter kernel** named `m1-coursework` (`Python (M1 Coursework)`) linked to `.venv/bin/python`.
6. **Verifies key packages** (`torch`, `numpy`, `scipy`, `pandas`, `scikit-learn`, `matplotlib`, `openpyxl`).

#### Specifying a Custom Python Interpreter:
If `python3.13` is installed at a specific path or non-standard location:

```bash
PYTHON=/path/to/python3.13 source setup_env.sh
```

---

### Option 2: Manual Setup

If you prefer setting up the virtual environment manually:

```bash
# 1. Create the virtual environment using Python 3.13 (or >= 3.12)
python3.13 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt ipykernel

# 4. Register the Jupyter kernel for notebooks
python -m ipykernel install --sys-prefix --name m1-coursework --display-name "Python 3.13 (M1 Coursework)"
```

---

## Jupyter Notebooks

When opening notebooks (e.g. `working/main.ipynb`) in VS Code, Cursor, or JupyterLab:
- Select the registered kernel: **Python 3.13 (M1 Coursework)** (or point directly to the interpreter at `.venv/bin/python`).

---

## Coursework Execution & Self-Check

### Running the step scripts:
```bash
python step1.py
python step2.py
python step3.py
python step4.py
```

### Submission validation:
To run the automated self-check against `results_table.xlsx` and generated outputs:

```bash
python check_submission.py <CRSid>
```
*(Replace `<CRSid>` with your Cambridge user ID, e.g. `sy507`).*
>>>>>>> 9f1afd3 (WIP completed up to step2 q1)
