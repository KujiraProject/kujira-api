import Queue
import json
import re
import threading

import salt.client

from kujira import DISK_BP
from kujira.rest.lib.request_methods import send_get


@DISK_BP.route("")
def get_disks():
    """Request for getting info about all disks on ceph"""
    queue = Queue.Queue()
    get_disks_thread = threading.Thread(target=salt_osd_disks, args=[queue])
    get_disks_thread.start()
    response = send_get('/server')
    json_list = []
    disk_mapping = None
    for json_obj in response:
        hostname = json_obj['hostname']
        if hostname != 'mng':
            server = {'hostname': hostname}
            disks = []
            available = 0
            size = 0
            if disk_mapping is None:
                disk_mapping = queue.get()
            if hostname in disk_mapping:
                partition_dict = disk_mapping[hostname]
                for elem in partition_dict:
                    elem_str = str(elem)
                    temp = re.search(r'\d+$', elem_str)
                    if elem_str.startswith('/dev/') and temp is None:
                        disks.append({elem_str: partition_dict[elem]})
                        if 'available' in partition_dict[elem]:
                            available += int(partition_dict[elem]['available'][:-1])
                        if 'size' in partition_dict[elem]:
                            size += int(partition_dict[elem]['size'][:-1])
            server['size'] = str(size) + 'M'
            server['disks_count'] = str(disks.__len__())
            server['available'] = str(available) + 'M'
            server['disks'] = disks
            json_list.append(server)
    return json.dumps(json_list, indent=2)


def salt_osd_disks(queue):
    """OSD mapping thread method"""
    local = salt.client.LocalClient()
    bash_output = local.cmd('*', 'osd_disk.get_disk_osd_mapping')
    queue.put(bash_output)
