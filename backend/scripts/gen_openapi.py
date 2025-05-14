import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import yaml
from main import app

def main():
    spec = app.openapi()
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
    os.makedirs(docs_dir, exist_ok=True)
    with open(os.path.join(docs_dir, "openapi.yaml"), "w") as f:
        yaml.dump(spec, f, sort_keys=False)

if __name__ == "__main__":
    main()