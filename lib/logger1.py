# def create_partition(self, drive_name):
#     out = connection.exec_command(f'echo -e "n\n\n\n\n\nw\n" | fdisk {drive_name}')
#     print(out)
#     return out
#
#
#
# def list_partitions(self):
#     partitions_drives = []
#     out = connection.exec_command('lsblk').split('\n')
#     for list_lines in out:
#         list_lines1 = list_lines.split()
#         if 'part' in list_lines1:
#             partitions_drives.append(list_lines1[0][2:])
#     print(partitions_drives)
#     return partitions_drives
#
#
# def create_file_system(self, drive_name):
#     out = connection.exec_command(f'echo -e "y\n\n" | mkfs.ext4 {drive_name}')
#     print(out)
#     return out
#
#
# def mount_drive(self, drive_name, mount_folder):
#     return connection.exec_command(f'mount {drive_name} {mount_folder}')
#
#
# def umount_drive(self, drive_name, mount_folder):
#     return connection.exec_command(f'umount {drive_name} {mount_folder}')
#
#
# def cpu_model(self):
#     out = connection.exec_command('lscpu')
#     out = re.search(r'(Model name:)\s+([^\n]+)', out)
#     print(f'{out.group(1)} {out.group(2)}')
#     return f'{out.group(1)} {out.group(2)}'
#
#
#
#
# def pci_controller(self):
#     pci_out = connection.exec_command('lspci').split('\n')
#     for i in pci_out:
#         out = re.search(r'RAID bus controller:\s+[^\n]+', i)
#         if bool(out) == True:
#             return out.group()