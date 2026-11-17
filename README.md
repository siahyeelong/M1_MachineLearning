# M1 Coursework for MPhil Data Intensive Science

> Siah Yee Long (sy507)

---

| File | What it is |
|---|---|
| `step1.py` | step 1: the learning set, the four features, the labels that contradict the physics, the inputs |
| `step2.py` | step 2: the linear classifier, its penalty, its weights, gradient descent and Nesterov's momentum |
| `step3.py` | step 3: the two networks (PyTorch), the labels they contradict, the suspects |
| `step4.py` | step 4: principal components, the maps, the clusters, the breakups of the catalogue |
| `common.py` | what the scripts share: the data, the inputs, the features, the score, the DMD rate, the table rows |
| `data/` | the two data files as received |
| `assignment.pdf` | the handout as received |
| `check_submission.py` | the self-check script as received |
| `outputs/` | the three CSV files the solution hands in, and the rows each script printed |
| `figures/` | the figures the scripts save |
| `requirements.txt` | the packages and versions the scripts ran with |
| `walkthrough.ipynb` | the answers question by question (goal, calculation, result); runs the four scripts in place, about six minutes |

## How to run

Using Python 3.12:
```bash
# 1. Create the virtual environment using Python 3.12
python3.12 -m venv .venv

# 2. Activate the environment
source .venv/bin/activate

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Performance

    python3 step1.py      # TODO: about 10 s
    python3 step2.py      # TODO: about 2 min
    python3 step3.py      # TODO: about 3 min
    python3 step4.py      # TODO: about 2 min

Each script finds the data in `data/` and the helper beside it, and rewrites its files in
`outputs/` and `figures/`.