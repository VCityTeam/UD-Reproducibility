import os
import sys
import logging
import time
import demo_workflow_static as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_server

if __name__ == '__main__':
    run_demo_server(workflow.demo_db_server)
