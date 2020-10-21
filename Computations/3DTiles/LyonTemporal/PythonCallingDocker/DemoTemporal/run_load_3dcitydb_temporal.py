import os
import sys
import logging

import demo_workflow_temporal as workflow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_load_3dcitydb
        
if __name__ == '__main__':
    run_demo_load_3dcitydb(workflow.demo_load, workflow.demo_db_servers)
