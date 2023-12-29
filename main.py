import shutil
import os
from filecmp import dircmp
import time
import sys

def sync_files(dcmp):
    file = open(log_file, 'a')
    for name in dcmp.left_only:
        source_path = os.path.join(dcmp.left, name)
        destination_path = os.path.join(dcmp.right, name)
        try:    
            shutil.copytree(source_path, destination_path)
            print("Folder %s copied from %s to %s" % (name, source_path, destination_path))
            file.write("\nFolder %s copied from %s to %s" % (name, source_path, destination_path))
        except NotADirectoryError:
            shutil.copy2(source_path, destination_path)
            print("File %s copied from %s to %s" % (name, source_path, destination_path))
            file.write("\nFile %s copied from %s to %s" % (name, source_path, destination_path))
    for name in dcmp.right_only:
        destination_path = os.path.join(dcmp.right, name)
        try:
            os.remove(destination_path)
            print("File %s deleted from %s because not found in %s" % (name, destination_path,
              dcmp.left))
            file.write('\nFile %s deleted from %s because not found in %s' % (name, destination_path,
              dcmp.left))
        except PermissionError:
            shutil.rmtree(destination_path)
            print('Folder %s deleted from %s because not found in %s' % (name, destination_path,
              dcmp.left))
            file.write('\nFolder %s deleted from %s because not found in %s' % (name, destination_path,
              dcmp.left))
    for name in dcmp.diff_files:
        source_path = os.path.join(dcmp.left, name)
        destination_path = os.path.join(dcmp.right, name)
        shutil.copyfile(source_path, destination_path)
        print("File %s updated in %s" % (name, dcmp.right))
        file.write("\nFile %s updated in %s" % (name, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        sync_files(sub_dcmp)
    
    file.close()
    sys.stdout.flush()

source_folder = input('Write the path to your source Folder:\n')
replica_folder = input('Write the path to your replica Folder:\n')
log_file = input('Write the path to your Log File:\n')
sync_interval = input('Write your synchronization interval in seconds for the folders:\n')

while True:
    try:
        dcmp = dircmp(source_folder, replica_folder)
        sync_files(dcmp)
        time.sleep(float(sync_interval))
    except KeyboardInterrupt:
        print("The Program is terminated manually!")
        raise SystemExit