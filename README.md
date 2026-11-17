# Worked solutions of the M1 coursework 2026-27

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
