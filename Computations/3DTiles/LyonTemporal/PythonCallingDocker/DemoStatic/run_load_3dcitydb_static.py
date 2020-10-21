import os
import sys
import logging

import demo_workflow_static as workflow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_load_3dcitydb
        
if __name__ == '__main__':
    load = workflow.demo_load
    server = workflow.demo_db_server
    run_demo_load_3dcitydb(load, server)
