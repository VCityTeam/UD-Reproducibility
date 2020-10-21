import os
import sys
import demo_workflow_temporal as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_lyon_metropole_dowload_and_sanitize


if __name__ == '__main__':
    run_demo_lyon_metropole_dowload_and_sanitize(workflow.demo_download)
