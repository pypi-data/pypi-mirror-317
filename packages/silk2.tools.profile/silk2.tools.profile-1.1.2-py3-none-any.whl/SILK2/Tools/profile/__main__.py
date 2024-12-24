import argparse as arg
import os
from .log_profile import get_algo_perf_page

def bmcompiler_parser():
    parser = arg.ArgumentParser(description     = "SILK2 Profile Tools",
                                formatter_class = arg.ArgumentDefaultsHelpFormatter,
                                prog            = "python -m SILK2.Tools.profile")
    required_group = parser.add_argument_group("required", "required parameters for compilation")
    required_group.add_argument("--logfile",
                                type    = str,
                                help    = "log file name")
    required_group.add_argument("--taskname",
                            type    = str,
                            help    = "task name")
    return parser
if __name__ == "__main__":
    parser = bmcompiler_parser()
    a = parser.parse_args()
    if a.logfile is None:
        print("usage: python -m SILK2.Tools.profile [-h] [--logfile LOGFILE] [--taskname TASKNAME]")
        exit(0)
    if a.taskname is None:
        print("usage: python -m SILK2.Tools.profile [-h] [--logfile LOGFILE] [--taskname TASKNAME]")
        exit(0)
        
    get_algo_perf_page(a.logfile, a.taskname)
