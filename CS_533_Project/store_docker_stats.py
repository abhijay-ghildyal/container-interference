# https://github.com/mavlyutov/docker-stats/blob/master/docker_stats.py
import docker 
import json
import argparse

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
# ids = args.all and map(itemgetter('Id'), client.containers(quiet=True)) or args.containers
ids=['docker_mnist_9']

stats = {c: client.stats(c, stream=0) for c in ids}
# stats = args.normalize and normalize(stats) or stats
print (json.dumps(stats))

print("\n\n\n cpu_usage:", calculate_cpu_percent(stats[ids[0]]))
print("\n\n\n cpu_usage:", stats[ids[0]]['cpu_stats']['throttling_data'])
print("\n\n\n cpu_usage:", stats[ids[0]]['precpu_stats']['throttling_data'])



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