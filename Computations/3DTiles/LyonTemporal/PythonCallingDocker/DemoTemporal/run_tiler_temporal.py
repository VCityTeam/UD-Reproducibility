import os
import sys
import demo_workflow_temporal as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_tiler


if __name__ == '__main__':
    tiler = workflow.demo_tiler
    servers = workflow.demo_db_servers
    run_demo_tiler(tiler, servers)
