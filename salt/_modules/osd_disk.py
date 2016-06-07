"""
Salt module to fetch osd and disks mappings.
To test module you have to:
1. synchronize modules: salt '*' saltutil.sync_modules
2. run function salt '*' osd_disk.get_disk_osd_mapping

"""

import json
import os
import re


def get_all():
    """Get all osd's in json format"""

    return json.loads(__salt__['cmd.run']('ceph osd tree -f json'))


def _grep(input_str, search_term):
    """Get line where pattern was found

    :param input_str: string text with new lines
    :param search_term: string to be found in line
    :returns first line containing search_term
    """

    for line in input_str:
        if re.search(search_term, line):
            return line


def _process_command(command):
    """Running command and split output by new line

    :param command: command to run by salt-minion
    """

    return __salt__['cmd.run'](command).split('\n')


def _set_values_for_ceph_data(disk_mapping, command_out_values_list):
    """Setting dictionary fields to values from grepped 'ceph-disk list'
     output line as list for ceph data

    :param disk_mapping: input dictionary object to set keys
    :param command_out_values_list: list of grepped line's strings
    """
    disk_mapping['type'] = 'osd'
    disk_mapping['status'] = \
        command_out_values_list[3][:-1]
    disk_mapping['cluster'] = \
        command_out_values_list[5][:-1]
    disk_mapping['osd_name'] = \
        command_out_values_list[6][:-1]
    disk_mapping['journal_device'] = \
        command_out_values_list[8]


def _set_values_for_ceph_journal(disk_mapping, command_out_values_list):
    """Setting dictionary fields to values from grepped 'ceph-disk list'
    output line as list for ceph journal

    :param disk_mapping: input dictionary object to set keys
    :param command_out_values_list: list of grepped line's strings
    """
    disk_mapping['type'] = 'journal'
    disk_mapping['osd_device'] = \
        command_out_values_list[4]


def _set_values_to_df_command_out(disk_mapping, command_out_values_list):
    """Setting dictionary fields to values from grepped 'ceph-disk list'
    output line as list for ceph journal

    :param disk_mapping: input dictionary object to set keys
    :param command_out_values_list: list of grepped line's strings
    """
    disk_mapping['size'] = command_out_values_list[1]
    disk_mapping['used'] = command_out_values_list[2]
    disk_mapping['available'] = command_out_values_list[3]
    disk_mapping['mounted'] = command_out_values_list[5]


def get_disk_osd_mapping():
    """Function to get disk's info data with osd mapping

    :returns object containing osd's information
    about disks and partitions, for example:
     "/dev/sdb2": {
     "type": "journal",
     "osd_device": "/dev/sdb1",
     "name": "sdb2",
     "disk_path_id": "pci-0000:00:0d.0-ata-3.0-part2"
     },
    "/dev/sdc": {
     "type": "operating-system",
     "name": "sdc",
     "disk_path_id": "pci-0000:00:0d.0-ata-4.0"
    },
    """

    ceph_disk_out_lines = _process_command('ceph-disk list')
    df_out_lines = _process_command('df -h')
    disks_by_path_out_lines = _process_command('ls -l /dev/disk/by-path/')

    disk_mapping = {}
    for current_disk in ceph_disk_out_lines:
        if not current_disk:
            continue
        current_disk_line = current_disk.split()
        # Getting disk name from the first position in output line
        disk_name = current_disk_line[0]
        disk_mapping[disk_name] = {}
        disk_mapping_by_name = disk_mapping[disk_name]

        # Checking if line contains partition not disk
        if len(current_disk_line) > 2:
            disk_path = os.path.basename(os.path.normpath(disk_name))
            disk_mapping_by_name['name'] = disk_path
            type_index = 1
            next_type_index_if_not_other = 2

            # Checking if disk's type is other
            # [:1] -> trimming the last comma from string
            if current_disk_line[type_index][:-1] == 'other':
                disk_mapping_by_name['type'] = 'operating-system'

            # Checking if disk's type is ceph data
            if current_disk_line[type_index] == 'ceph' \
                    and current_disk_line[next_type_index_if_not_other] \
                            [:-1] == 'data':
                _set_values_for_ceph_data(disk_mapping_by_name, \
                                          current_disk_line)

            # Checking if disk's type is ceph journal
            if current_disk_line[type_index] == 'ceph' \
                    and current_disk_line[next_type_index_if_not_other] \
                            [:-1] == 'journal':
                _set_values_for_ceph_journal(disk_mapping_by_name, \
                                             current_disk_line)

        disk_id_line = _grep(disks_by_path_out_lines, \
                             # Getting only disk name from path
                             os.path.basename(os.path.normpath(disk_name)))
        if disk_id_line:
            # Splitting line by whitespaces to list
            disk_id_line = disk_id_line.split()
            # disk_id_line[8] where 8 is index of disk path id
            # in 'ls -l /dev/disk/by-path/' command
            disk_mapping_by_name['disk_path_id'] = disk_id_line[8]

        df_line = _grep(df_out_lines, \
                        # Getting only disk name from path
                        os.path.basename(os.path.normpath(disk_name)))
        if df_line:
            # Splitting line by whitespaces to list
            df_line = df_line.split()
            _set_values_to_df_command_out(disk_mapping_by_name, df_line)

    return disk_mapping

