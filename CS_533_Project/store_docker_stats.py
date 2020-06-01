# https://github.com/mavlyutov/docker-stats/blob/master/docker_stats.py
import docker 
import json
import argparse
import logging
import time
from operator import itemgetter
import inspect

import os
import psutil

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logs/main.log', level=logging.INFO)

print("Running at nice value:", psutil.Process(os.getpid()).nice())
# psutil.Process(os.getpid()).nice(-20)
# print("Changed nice value to:", psutil.Process(os.getpid()).nice())

# sudo nice -n -20 python3 store_docker_stats.py

def normalize(dictionary):

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            normalize(value)

        item_dict = dict()
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "op" in item:
                    item_dict.update({item.pop("op"): item})
        if item_dict:
            dictionary[key] = item_dict

    return dictionary

# https://github.com/TomasTomecek/sen/blob/master/sen/util.py#L158
def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent



client = docker.APIClient(base_url='unix://var/run/docker.sock')
# client = docker.Client(base_url='unix://var/run/docker.sock')

while(1):

    # ids = map(itemgetter('Id'), client.containers(quiet=True))
    # container_info = map(itemgetter('Names'), client_on_.containers(quiet=True))
    info_on_container = client.containers()
    # print(client.containers())
    # print("\n\n\n")
    # time.sleep(3)
    # continue
    # print(containers)
    # print ("ids:", dir(ids))
    # print(inspect.getmembers(ids))
    # print(ids.names)
    container_names = [c['Names'][0].split('/')[1] for c in reversed(info_on_container)]
    # print ("container_names:", container_names)
    if container_names:
        try:
            stats = {container_name: client.stats(container_name, stream=0) for container_name in container_names}
        except Exception:
            continue
        # stats = args.normalize and normalize(stats) or stats
        # print (json.dumps(stats))


        container_cpu_usage = {}
        for container_name in container_names:
            # begin_time = time.time()
            try:
                container_cpu_usage[container_name] = calculate_cpu_percent(stats[container_name])
            except Exception:
                continue
            # print("\n\n\n cpu_usage:", calculate_cpu_percent(stats[container_name]))
            # print("end_time: ", time.time() - begin_time)
        # print("\n\n\n cpu_usage:", stats[ids[0]]['cpu_stats']['throttling_data'])
        # print("\n\n\n cpu_usage:", stats[ids[0]]['precpu_stats']['throttling_data'])
        logging.info(' == {{"LogType": "{}", "cpu_usage": "{}"}}'.format( 4, container_cpu_usage))
    # print("sleep started")
    # time.sleep(1)


# [
# {'Id': '0b643313ec38333ffcebeef90ee656ee88ba196118dd9165c55af181e645f1f6', 'Names': ['/docker_mnist_1'], 'Image': 'pytorch/pytorch', 'ImageID': 'sha256:a10c611c2731b3b07fad270deb787d836f658285f70fdaed86a9ba383ac6baab', 'Command': 'python main.py --configFileName config/app1_config.json', 'Created': 1590455406, 'Ports': [], 'Labels': {'com.nvidia.volumes.needed': 'nvidia_driver'}, 'State': 'running', 'Status': 'Up About a minute', 'HostConfig': {'NetworkMode': 'default'}, 'NetworkSettings': {'Networks': {'bridge': {'IPAMConfig': None, 'Links': None, 'Aliases': None, 'NetworkID': '2c9862043729ef77694462d0055c4aea9d558e9266047c566405b457b76720ea', 'EndpointID': '84cee57981f226b2d3d48a43696344dba7f34b5d941d1c6f520095635f14e6d8', 'Gateway': '172.17.0.1', 'IPAddress': '172.17.0.2', 'IPPrefixLen': 16, 'IPv6Gateway': '', 'GlobalIPv6Address': '', 'GlobalIPv6PrefixLen': 0, 'MacAddress': '02:42:ac:11:00:02', 'DriverOpts': None}}}, 'Mounts': [{'Type': 'bind', 'Source': '/home/abhijay/CS_533_Project', 'Destination': '/workspace', 'Mode': '', 'RW': True, 'Propagation': 'rprivate'}]}
# ]



# sample docker stats
# {
#   "docker_mnist_1": {
#     "read": "2020-05-17T06:41:01.97873211Z",
#     "preread": "2020-05-17T06:41:00.977144135Z",
#     "pids_stats": {
#       "current": 13
#     },
#     "blkio_stats": {
#       "io_service_bytes_recursive": [
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Read",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Write",
#           "value": 43241472
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Sync",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Async",
#           "value": 43241472
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Discard",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Total",
#           "value": 43241472
#         }
#       ],
#       "io_serviced_recursive": [
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Read",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Write",
#           "value": 66
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Sync",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Async",
#           "value": 66
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Discard",
#           "value": 0
#         },
#         {
#           "major": 8,
#           "minor": 0,
#           "op": "Total",
#           "value": 66
#         }
#       ],
#       "io_queue_recursive": [],
#       "io_service_time_recursive": [],
#       "io_wait_time_recursive": [],
#       "io_merged_recursive": [],
#       "io_time_recursive": [],
#       "sectors_recursive": []
#     },
#     "num_procs": 0,
#     "storage_stats": {},
#     "cpu_stats": {
#       "cpu_usage": {
#         "total_usage": 514911436067,
#         "percpu_usage": [
#           37510633334,
#           41804839435,
#           38020915865,
#           46760575798,
#           42864536817,
#           45317469766,
#           48929890874,
#           45491513045,
#           47098209107,
#           39265008826,
#           40099275500,
#           41748567700
#         ],
#         "usage_in_kernelmode": 26560000000,
#         "usage_in_usermode": 488420000000
#       },
#       "system_cpu_usage": 286737790000000,
#       "online_cpus": 12,
#       "throttling_data": {
#         "periods": 0,
#         "throttled_periods": 0,
#         "throttled_time": 0
#       }
#     },
#     "precpu_stats": {
#       "cpu_usage": {
#         "total_usage": 505774454571,
#         "percpu_usage": [
#           36684144450,
#           41074810961,
#           37373392073,
#           46060603404,
#           42110165013,
#           44560734461,
#           48127790229,
#           44726924595,
#           46419550291,
#           38531986909,
#           39227516411,
#           40876835774
#         ],
#         "usage_in_kernelmode": 26480000000,
#         "usage_in_usermode": 479330000000
#       },
#       "system_cpu_usage": 286725740000000,
#       "online_cpus": 12,
#       "throttling_data": {
#         "periods": 0,
#         "throttled_periods": 0,
#         "throttled_time": 0
#       }
#     },
#     "memory_stats": {
#       "usage": 421896192,
#       "max_usage": 757964800,
#       "stats": {
#         "active_anon": 369684480,
#         "active_file": 0,
#         "cache": 42848256,
#         "dirty": 135168,
#         "hierarchical_memory_limit": 9223372036854772000,
#         "hierarchical_memsw_limit": 0,
#         "inactive_anon": 0,
#         "inactive_file": 42848256,
#         "mapped_file": 0,
#         "pgfault": 20054727,
#         "pgmajfault": 0,
#         "pgpgin": 20061525,
#         "pgpgout": 19960559,
#         "rss": 369831936,
#         "rss_huge": 0,
#         "total_active_anon": 369684480,
#         "total_active_file": 0,
#         "total_cache": 42848256,
#         "total_dirty": 135168,
#         "total_inactive_anon": 0,
#         "total_inactive_file": 42848256,
#         "total_mapped_file": 0,
#         "total_pgfault": 20054727,
#         "total_pgmajfault": 0,
#         "total_pgpgin": 20061525,
#         "total_pgpgout": 19960559,
#         "total_rss": 369831936,
#         "total_rss_huge": 0,
#         "total_unevictable": 0,
#         "total_writeback": 0,
#         "unevictable": 0,
#         "writeback": 0
#       },
#       "limit": 16477753344
#     },
#     "name": "/docker_mnist_1",
#     "id": "532364623f6426f582280456db7c1f3a2eb702cd7d29a752747d1b9d7b25818d",
#     "networks": {
#       "eth0": {
#         "rx_bytes": 5255,
#         "rx_packets": 40,
#         "rx_errors": 0,
#         "rx_dropped": 0,
#         "tx_bytes": 0,
#         "tx_packets": 0,
#         "tx_errors": 0,
#         "tx_dropped": 0
#       }
#     }
#   }
# }