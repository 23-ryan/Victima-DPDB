
import os
import argparse
import sys

# I need the user to provide an argument --native or --slurm to specify the execution mode

parser = argparse.ArgumentParser(
    description="Script creats experiments run in native or SLURM mode.")
parser.add_argument("--native", action="store_true",
                    help="Run in native mode.")
parser.add_argument("--slurm", action="store_true", help="Run in SLURM mode.")
parser.add_argument("path", help="Path to the file or directory.")
parser.add_argument("--excluded_nodes", nargs='?', default=None,
                    help="Comma-separated list of excluded nodes.")

args = parser.parse_args()

if args.native and args.slurm:
    print("Error: Cannot specify both --native and --slurm. Choose one execution mode.")
    exit(1)

slurm = False
native = False
if args.native:
    native = True
elif args.slurm:
    slurm = True
else:
    print("Error: Please specify either --native or --slurm to choose the execution mode.")
    exit(1)

trace_path = "/app/traces/"

traces = [("bfs", "bfs.sift"),
          ("cc", "cc.sift")]


# Docker command to run the binary inside the container
docker_command = "docker run --rm -v "+args.path + \
    ":/app/ docker.io/kanell21/artifact_evaluation:victima"

baseline = " -c /app/sniper/config/virtual_memory_configs/radix.cfg "
victima = " -c /app/sniper/config/virtual_memory_configs/victima.cfg "
victima_dpp_cbp = " -c /app/sniper/config/virtual_memory_configs/victima_dpp_dbp.cfg "
potm = " -c /app/sniper/config/virtual_memory_configs/potm.cfg "
virtu = " -c /app/sniper/config/virtual_memory_configs/virtualized.cfg "

configs = [

    ("victima_ptw_1MBL2", victima+" -g --perf_model/l2_cache/cache_size=1024 -g --perf_model/l2_cache/data_access_time=12 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=false"),
    ("victima_ptw_2MBL2", victima+" -g --perf_model/l2_cache/cache_size=2048 -g --perf_model/l2_cache/data_access_time=16 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=false"),
    ("victima_ptw_4MBL2", victima+" -g --perf_model/l2_cache/cache_size=4096 -g --perf_model/l2_cache/data_access_time=22 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=false"),
    ("victima_ptw_8MBL2", victima+" -g --perf_model/l2_cache/cache_size=8192 -g --perf_model/l2_cache/data_access_time=30 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=false"),


    ("victima_dpp_dbp_ptw_1MBL2", victima_dpp_cbp+" -g --perf_model/l2_cache/cache_size=1024 -g --perf_model/l2_cache/data_access_time=12 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=true"),
    ("victima_dpp_dbp_ptw_2MBL2", victima_dpp_dbp+" -g --perf_model/l2_cache/cache_size=2048 -g --perf_model/l2_cache/data_access_time=16 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=true"),
    ("victima_dpp_dbp_ptw_4MBL2", victima_dpp_cbp+" -g --perf_model/l2_cache/cache_size=4096 -g --perf_model/l2_cache/data_access_time=22 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=true"),
    ("victima_dpp_dbp_ptw_8MBL2", victima_dpp_cbp+" -g --perf_model/l2_cache/cache_size=8192 -g --perf_model/l2_cache/data_access_time=30 -g --perf_model/victima/victimize_on_ptw=true -g --perf_model/l2_cache/srrip/tlb_enabled=true -g --perf_model/victima/dead_page_dead_block_predictor=true")
]


sniper_parameters = "/app/sniper/run-sniper -s stop-by-icount:500000000 --genstats --power"

# # # Create the jobfile: a bash script that runs all the binaries with all the configurations
with open("/app/jobfile", "w") as jobfile:
    jobfile.write("#!/bin/bash\n")

    for (trace_name, trace) in traces:

        for (config_name, configuration_string) in configs:

            trace_command = "--traces={}".format(trace_path+trace)

            output_command = "-d /app/results/{}_{}".format(
                config_name, trace_name)

            if (slurm):
                # SLURM parameters are overprovisioned just in case the simulation takes longer than expected
                if args.excluded_nodes is not None:
                    execution_command = "sbatch --exclude="+args.excluded_nodes+"  -J {}_{} --output=./results/{}_{}.out --error=./results/{}_{}.err docker_wrapper.sh ".format(
                        config_name, trace_name, config_name, trace_name, config_name, trace_name)
                else:
                    execution_command = "sbatch   -J {}_{} --output=./results/{}_{}.out --error=./results/{}_{}.err docker_wrapper.sh ".format(
                        config_name, trace_name, config_name, trace_name, config_name, trace_name)
                command = execution_command + "\"" + docker_command + " " + sniper_parameters + \
                    " " + output_command+" "+configuration_string+" "+trace_command+"\""
            elif (native):
                command = docker_command + " " + sniper_parameters + " " + output_command+" " + \
                    configuration_string+" "+trace_command + \
                    " > ./results/"+config_name+"_"+trace_name+".out"
            # command = docker_command + " " + sniper_parameters + " " + output_command+" "+configuration_string+" "+trace_command

            jobfile.write(command)
            jobfile.write("\n")
