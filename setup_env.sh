#!/usr/bin/env bash
# setup_env.sh -- virtual environment, dependencies, and Jupyter kernel for
# M1 Coursework (MPhil Data Intensive Science).
#
# Usage (from repository root):
#     source setup_env.sh
#
# Python interpreter:
#     Defaults to python3.13 (with backward compatibility fallback to python3.12).
#     Override with: PYTHON=/path/to/python source setup_env.sh
#
# A .venv built with an incompatible Python version is automatically rebuilt.
# Subsequent runs will skip package re-installation if requirements.txt has not changed.

# --- Sourcing check ---
# Virtual environments can only be activated in the caller's shell if the script is sourced.
if [ -n "${ZSH_VERSION:-}" ]; then
    case "$ZSH_EVAL_CONTEXT" in
        *:file) ;; # Sourced properly in zsh
        *) echo "setup_env.sh: Please run with 'source setup_env.sh' (or '. setup_env.sh') to activate the environment in your shell."; exit 1 ;;
    esac
elif [ -n "${BASH_VERSION:-}" ]; then
    if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
        echo "setup_env.sh: Please run with 'source setup_env.sh' (or '. setup_env.sh') to activate the environment in your shell."
        exit 1
    fi
fi

setup_env() {
    # Verify execution from repository root
    if [ ! -f requirements.txt ]; then
        echo "setup_env.sh: requirements.txt not found. Please run this script from the repository root."
        return 1
    fi

    # Determine Python interpreter to use
    local python="${PYTHON:-}"
    if [ -z "$python" ]; then
        if command -v python3.13 >/dev/null 2>&1; then
            python="python3.13"
        elif command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 13) else 1)' 2>/dev/null; then
            python="python3"
        elif command -v python3.12 >/dev/null 2>&1; then
            python="python3.12"
            echo "setup_env.sh: python3.13 not found in PATH; falling back to python3.12."
        elif command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3, 12) else 1)' 2>/dev/null; then
            python="python3"
            echo "setup_env.sh: python3.13 not found in PATH; using $(python3 --version)."
        else
            python="python3.13"
        fi
    fi

    if ! command -v "$python" >/dev/null 2>&1; then
        echo "setup_env.sh: '$python' not found in PATH."
        echo "Please install Python 3.13 (or >= 3.12) or set PYTHON=/path/to/python before running."
        return 1
    fi

    # Check Python version compatibility with requirements.txt
    local py_major py_minor want
    py_major=$("$python" -c 'import sys; print(sys.version_info[0])' 2>/dev/null)
    py_minor=$("$python" -c 'import sys; print(sys.version_info[1])' 2>/dev/null)
    want="${py_major}.${py_minor}"

    if [ "$py_major" -ne 3 ] || [ "$py_minor" -lt 12 ]; then
        echo "setup_env.sh: $("$python" --version) is not supported."
        echo "Dependencies in requirements.txt (e.g. numpy 2.5, scipy 1.18, contourpy 1.4, networkx 3.7) require Python >= 3.12."
        echo "Python 3.13 is recommended for this workspace."
        return 1
    fi

    # Manage virtual environment (.venv)
    if [ -d .venv ]; then
        local have
        have=$(.venv/bin/python -c 'import sys; print("%d.%d" % sys.version_info[:2])' 2>/dev/null)
        if [ "$have" != "$want" ]; then
            echo "setup_env.sh: Existing .venv is Python ${have:-unknown}, but desired interpreter is $want. Rebuilding .venv..."
            rm -rf .venv
        fi
    fi

    if [ ! -d .venv ]; then
        echo "setup_env.sh: creating .venv with $("$python" --version) at $(command -v "$python")"
        "$python" -m venv .venv || return 1
    fi

    # Activate virtual environment
    # shellcheck disable=SC1091
    . .venv/bin/activate || return 1

    # Install dependencies and Jupyter kernel
    if [ ! -f .venv/lock.stamp ] || [ requirements.txt -nt .venv/lock.stamp ]; then
        echo "setup_env.sh: installing dependencies from requirements.txt..."
        python -m pip install --upgrade pip >/dev/null 2>&1 || true
        python -m pip install --quiet --disable-pip-version-check -r requirements.txt ipykernel || return 1

        # Register Jupyter kernel so notebooks (e.g. working/main.ipynb) can use this environment
        python -m ipykernel install --sys-prefix --name m1-coursework --display-name "Python ${want} (M1 Coursework)" >/dev/null 2>&1 \
            || python -m ipykernel install --user --name m1-coursework --display-name "Python ${want} (M1 Coursework)" >/dev/null 2>&1 \
            || return 1
        echo "setup_env.sh: registered Jupyter kernel 'm1-coursework' -> $PWD/.venv/bin/python"

        touch .venv/lock.stamp
    fi

    # Load local environment variables if .env exists
    if [ -f .env ]; then
        set -a
        # shellcheck disable=SC1091
        . ./.env
        set +a
    fi

    # Verify installation of core coursework packages
    python -c "
import sys
import numpy as np
import scipy
import pandas as pd
import sklearn
import matplotlib
import torch
import openpyxl

print('setup_env.sh: environment verified successfully!')
print(f'  - Python:  {sys.version.split()[0]} ({sys.executable})')
print(f'  - PyTorch: {torch.__version__} (MPS available: {torch.backends.mps.is_available()})')
print(f'  - Core:    numpy {np.__version__}, scipy {scipy.__version__}, pandas {pd.__version__}, scikit-learn {sklearn.__version__}')
" || return 1
}

setup_env
