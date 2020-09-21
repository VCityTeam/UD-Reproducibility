import os
import sys
import demo_workflow_static as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run_demo_lyon_metropole_dowload_and_sanitize \
    import run_demo_lyon_metropole_dowload_and_sanitize


if __name__ == '__main__':
    run_demo_lyon_metropole_dowload_and_sanitize(workflow.demo_download)
