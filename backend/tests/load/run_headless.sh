set -euo pipefail

cd "$(dirname "$0")"
source ../../../backend/.venv/bin/activate

locust \
  -f locustfile.py \
  --headless \
  --config locust.conf \
  --csv loadtest-report

echo "Load test complete—reports in $(pwd)/loadtest-report_*.csv"