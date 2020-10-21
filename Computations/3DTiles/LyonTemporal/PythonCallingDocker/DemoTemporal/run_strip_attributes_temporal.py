import os
import sys
import demo_workflow_temporal as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_strip_attributes


if __name__ == '__main__':
    run_demo_strip_attributes(workflow.demo_strip)

