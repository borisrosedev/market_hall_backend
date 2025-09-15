#!/usr/bin/env bash
set -euo pipefail

CYAN_COLOR="\033[1;36m"
NO_COLOR="\033[0m"

# Trouver la racine du projet = dossier parent de scripts/
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Se placer à la racine et préparer l'env
cd "${PROJECT_ROOT}"
export PYTHONPATH="${PROJECT_ROOT}"
export ALEMBIC_CONFIG="${PROJECT_ROOT}/alembic.ini"

echo -e "$CYAN_COLOR$(date +'%F %T') + wait for DB $NO_COLOR"
python -m app.backend_pre_start

# (Optionnel) autogénère une migration si aucune n'existe
if [ ! -d "${PROJECT_ROOT}/app/alembic/versions" ] || [ -z "$(ls -A "${PROJECT_ROOT}/app/alembic/versions" 2>/dev/null || true)" ]; then
  echo -e "$CYAN_COLOR$(date +'%F %T') + no migrations found → autogenerate initial migration $NO_COLOR"
  alembic revision --autogenerate -m "init schema"
fi

echo -e "$CYAN_COLOR$(date +'%F %T') + migrate $NO_COLOR"
alembic upgrade head

echo -e "$CYAN_COLOR$(date +'%F %T') + seed initial data $NO_COLOR"
python -m app.initial_data

echo -e "$CYAN_COLOR$(date +'%F %T') + done $NO_COLOR"
#exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
