import re

from logger import *
from connect import *


class ListDriveClass:
    @staticmethod
    def list_drives(cmd):
        try:
            server_drive = connection.exec_command(cmd)
            if bool(server_drive[1]):
                return f"{server_drive[1][server_drive[1].find(cmd):]}'Do you mean lsblk '"
            else:
                list_drives = ['/dev/' + drive.split(' ')[0] for drive in server_drive[0].split('\n') if
                               drive.startswith('sd')]
                return list_drives
        except Exception as e:
            return e


def read_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def server_drives():
    server_drives_list = connection.exec_command('lsblk')
    list_drives = ['/dev/' + drive.split(' ')[0] for drive in server_drives_list[0].split('\n')
                   if drive.startswith('sd')]
    return list_drives


# command = read_json("../testcases/ListAllDrives.json")['command']
# storage_obj = ListDriveClass()
logger = get_logger("my_logger", arg1="fio_test")


# drives = storage_obj.list_drives(command)
# logger.info(drives)


class FirmwareVersions:
    def firmware_versions(self, drives_list):
        try:
            command_dict = {}
            for drive in drives_list:
                if drive not in server_drives():
                    return f"{command_dict}\n'{drive}' drive is not found in server"
                out = connection.exec_command(f'smartctl -a {drive}')[0]
                import re
                command_dict[drive] = re.sub(r'\s+', ' ',
                                             re.findall(r'Firmware Version:\s+\w+|Revision:\s+\w+', out)[0])
            return command_dict
        except Exception as e:
            return e


# firmware_obj = FirmwareVersions()
# drives = read_json("../testcases/FirmwareVersionsDrives.json")['Drives']
# firmware_versions = firmware_obj.firmware_versions(drives)
# logger.info(firmware_versions)


def partitions_list():
    try:
        partitions_drives = []
        boot_file = ''
        cmd_out = connection.exec_command('lsblk')[0].split('\n')
        for list_lines in cmd_out:
            list_lines1 = list_lines.split()
            if 'part' in list_lines1:
                if '/boot/efi' in list_lines1:
                    boot_file = list_lines1[0][2:]
                if bool(re.findall(r'sd\w+', list_lines)):
                    partitions_drives.append(list_lines1[0][2:])
        return ['/dev/' + drives for drives in partitions_drives if not drives[:-1] == boot_file[:-1]]
    except Exception as e:
        print(e)


# logger.info(partitions_list())


def partitions_space():
    try:
        # partitions_drives = []
        dict1 = {}
        boot_file = ''
        cmd_out = connection.exec_command('lsblk')[0].split('\n')
        for list_lines in cmd_out:
            list_lines1 = list_lines.split()
            if 'part' in list_lines1:
                if '/boot/efi' in list_lines1:
                    boot_file = '/dev/' + list_lines1[0][2:]
                if bool(re.findall(r'sd\w+', list_lines)):
                    dict1['/dev/' + list_lines1[0][2:]] = list_lines1[3]
        return {drives: j for drives, j in dict1.items() if not drives[:-1] == boot_file[:-1]}
    except Exception as e:
        print(e)


# logger.info(partitions_space())
def extended_partitions_space():
    # partitions_drives = []
    dict1 = {}
    cmd_out = connection.exec_command('fdisk -l')[0].split('\n')
    for i in cmd_out:
        if i.endswith('Extended'):
            dict1[i.split(' ')[0]] = i.split(' ')[-4]
    return dict1


# logger.info(logical_partitions_space())

def drives_space():
    try:
        drives_spaces = {}
        cmd_out = connection.exec_command('lsblk')[0].split('\n')
        for list_lines in cmd_out:
            list_lines1 = list_lines.split()
            if bool(list_lines1) and list_lines1[0].startswith('sd'):
                drives_spaces['/dev/' + list_lines1[0]] = list_lines1[3]
        return drives_spaces
    except Exception as e:
        print(e)


# logger.info(drives_space())


class CreatePartition:

    def create_partition(self, drives_name, partitions_type, partition_number, last_sector):
        """

        :param drives_name:
        :param partitions_type:
        :param partition_number:
        :param last_sector:
        :return:
        """
        try:
            list1 = []
            results_list = []
            for drive_name in drives_name:
                if drive_name in server_drives():
                    target_drives_space = int(drives_space()[drive_name][:3])
                    if target_drives_space > (int(partition_number) * int(last_sector[1:-1])):
                        old_partition = partitions_list()
                        pre_partitions = re.findall(fr'{drive_name}\d', (' '.join(old_partition)))
                        list_pre_partitions = [int(pre_partitions[i][-1]) for i in range(len(pre_partitions))]
                        pri_pre_partitions = [i for i in list_pre_partitions if i < 5]
                        old_partition1 = extended_partitions_space()
                        extended_space = [int(j[:-1]) for i, j in old_partition1.items() if i[:-1] == drive_name]
                        extended_space = extended_space if bool(extended_space) else [0]
                        if partitions_type != 'l':
                            partition_elements = [i for i in range(1, 5) if i not in pri_pre_partitions]
                            pre_len = len(partition_elements)
                            sum_pre_partition_storage = sum([int(re.search(r'\d+', partitions_space()[drive]).
                                                                 group()) for drive in partitions_space().keys()
                                                             if (drive[:-1]) == drive_name])
                            if target_drives_space >= (int(sum_pre_partition_storage) + extended_space[0] +
                                                       (int(partition_number) * int(last_sector[1:-1])) + 1):
                                if 4 >= pre_len >= int(partition_number) and pre_len:
                                    partition_numbers = [partition_elements[i] for i in range(int(partition_number))]
                                    for Partition_num in partition_numbers:
                                        cmd_o = connection.exec_command(f'echo -e " n\n{partitions_type}\n{Partition_num}\n\n{last_sector}\nw\n" | fdisk {drive_name}')
                                        re_cmd = re.search(r"Created [\s\w']+", re.sub(',', '',
                                                                                       str(cmd_o)))
                                        list1.append(re_cmd.group()) if bool(re_cmd) else results_list.append(cmd_o)
                                    new_partitions = [i for i in partitions_list() if i not in old_partition]
                                    results_list.append([(list1[i] + " : " + new_partitions[i]) for i in
                                                         range(len(new_partitions))])
                                else:
                                    results_list.append(f'unavailable partitions :: remaining partitions are only '
                                                        f'{pre_len} you are given {partition_number}')
                            else:
                                results_list.append(f'drive {drive_name} has not enough space for creating partition, '
                                                    f'remaining space : '
                                                    f'{target_drives_space - (int(sum_pre_partition_storage) +
                                                                              extended_space[0])}G you are given : '
                                                    f'{(int(partition_number) * int(last_sector[1:-1]))}G')
                        else:
                            old_partition = old_partition1
                            if [i for i, j in old_partition.items() if i[:-1] == drive_name]:
                                logical_partitions = [i for i in list_pre_partitions if i > 4]
                                logical_partitions = logical_partitions if bool(logical_partitions) else [5]
                                sum_logical_partition = sum([int(j[:-1]) for i, j in partitions_space().items() for k in
                                                             logical_partitions if i == drive_name + str(k)])
                                extended_space = [int(j[:-1]) for i, j in old_partition.items() if i[:-1] == drive_name]
                                num_partitions = int(partition_number)
                                using_space = sum_logical_partition + (int(partition_number) * int(last_sector[1:-1]))
                                if extended_space[0] > using_space:
                                    for Partition_num in range(num_partitions):
                                        cmd_o = connection.exec_command(f'echo -e "n\n{partitions_type}'
                                                                        f'\n\n{last_sector}\nw\n" | fdisk {drive_name}')
                                        re_cmd = re.search(r"Created [\s\w']+", re.sub(',', '',
                                                                                       str(cmd_o)))
                                        results_list.append(re_cmd.group())
                                else:
                                    results_list.append(
                                        f'extended partition of {drive_name} not have enough space, you '
                                        f'have only {extended_space[0] - sum_logical_partition}G you '
                                        f'are given {int(last_sector[1:-1])}G')
                            else:
                                results_list.append(f" In drive {drive_name} , extended partition not available create"
                                                    f" one extended partition")
                    else:
                        results_list.append(f"drive {drive_name} has not enough space creating partitions, you have "
                                            f"only {target_drives_space}G you are given {(int(partition_number) *
                                                                                          int(last_sector[1:-1]))}G")
                else:
                    results_list.append(f"'{drive_name}' drive is not found in server."
                                        f" Available drives{server_drives()}")
            return results_list
        except Exception as e:
            return e


#
# drives = read_json("../testcases/CreatePartition.json")['Drives']
# partitions_type = read_json("../testcases/CreatePartition.json")["partitions_type"]
# Partition_number = read_json("../testcases/CreatePartition.json")["Partition_number"]
# # first_sector = read_json("../testcases/CreatePartition.json")["First_sector"]
# last_sector = read_json("../testcases/CreatePartition.json")["last_sector"]
# logger.info(CreatePartition().create_partition(drives, partitions_type, Partition_number, last_sector))


def delete_partition():
    out = [connection.exec_command(f'echo -ne "d\n\nw\n" | fdisk {drive_name[:-1]}')[0] for drive_name in
           partitions_list()]
    return [re.search(r'\w+\s+\w+\s+\w+\s+\w+\s+deleted', i).group() for i in out]


# logger.info(delete_partition())


def create_file_system(drives):
    for drive in drives:
        cmd_out = connection.exec_command(f'echo -e "y\n\n" | mkfs.ext4 {drive}')
        return f"in drive {drive} {cmd_out[0].split('\n')[0]}" if bool(cmd_out[0]) else cmd_out[1]


# file_system_drives = read_json("../testcases/filesystem.json")['Drives']
# logger.info(create_file_system(file_system_drives))


def mount_drive(self, drive_name, mount_folder):
    return connection.exec_command(f'mount {drive_name} {mount_folder}')

    # def umount_drive(self,drive_name,mount_folder):
    #     return connection.exec_command(f'umount {drive_name} {mount_folder}')
def cpu_model():
    out = re.search(r'(Model name:)\s+([^\n]+)', connection.exec_command('lscpu')[0])
    return f'{out.group(1)} {out.group(2)}'


# logger.info(cpu_model())

def free_used():
    ram_out = connection.exec_command('free')[0].split('\n')
    list_ram = [re.split(r'\s+', i) for i in ram_out]
    return [(f"{list_ram[list_ram.index(elements)][elements.index(element)]} :"
             f"{list_ram[list_ram.index(elements) + 1][elements.index(element)]}") for elements in list_ram
            for element in elements if element == 'free' or element == 'used']


# logger.info(free_used())

def pci_controller():
    pci_out = connection.exec_command('lspci')[0].split('\n')
    return [(re.search(r'RAID bus controller:\s+[^\n]+', i)).group() for i in pci_out if
            bool(re.search(r'RAID bus controller:\s+[^\n]+', i))]


# logger.info(pci_controller())


# storage_obj = StorageLib()
# logger = get_logger("my_logger", arg1="fio_test")
# drives = storage_obj.list_drives('lsblk')
# logger.info(drives)

#

# list_partitions = storage_obj.list_partitions()
# logger.info(list_partitions)
# d_partitions = storage_obj.delete_partition('/dev/sdh')
# logger.info(d_partitions)
# create_file_system = storage_obj.create_file_system('/dev/sdh1')
# logger.info(create_file_system)
# mount_drive = storage_obj.mount_drive('/dev/sdg1','/mnt/baba')
# logger.info(mount_drive)
# umount_drive = storage_obj.umount_drive('/dev/sdh1','/mnt/vk')
# logger.info(umount_drive)
# cpu_model = storage_obj.cpu_model()
# logger.info(cpu_model)
# free_used_ram = storage_obj.free_used()
# logger.info(free_used_ram)
