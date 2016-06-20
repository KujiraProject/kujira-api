import json
import re
import subprocess

from kujira import DISK_BP
from kujira.rest.lib.request_methods import send_get


@DISK_BP.route("")
def all_servers_raw():
    response = send_get('/server')
    json_list = []
    for json_obj in response:
        hostname = json_obj['hostname']
        if hostname != 'mng':
            server = {'hostname': hostname}
            disks = []
            available = 0
            size = 0
            process = subprocess.Popen("sudo salt '"+hostname+"' osd_disk.get_disk_osd_mapping --output json",
                                                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            bash_output = process.communicate()
            bash_output = json.loads(bash_output[0])
            if hostname in bash_output:
                part_dict = bash_output[hostname]
                for elem in part_dict:
                    elem_str = str(elem)
                    temp = re.search(r'\d+$', elem_str)
                    if elem_str.startswith('/dev/') and temp is None:
                        disks.append({elem_str: part_dict[elem]})
                        if 'available' in part_dict[elem]:
                            available += int(part_dict[elem]['available'][:-1])
                        if 'size' in part_dict[elem]:
                            size += int(part_dict[elem]['size'][:-1])
            server['size'] = str(size)+'M'
            server['disks_count'] = str(disks.__len__())
            server['available'] = str(available)+'M'
            server['disks'] = disks
            json_list.append(server)
    return json.dumps(json_list, indent=2)
