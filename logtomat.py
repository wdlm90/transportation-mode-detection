#!/usr/bin/env python
import os, shutil, sys
from time import sleep

# default options

training = True

argc = len(sys.argv)
argv = sys.argv

def exit_with_help(argv):
    print("""\
            Usage: {0} [options]

options (default 0):

0: training
1: test
""".format(argv[0]))
    exit(1)

if argc > 2:
    exit_with_help(sys.argv)
elif argc == 2:
    if int(argv[1]) == 1:
        training = False

if training:
    log_folder = 'data_raw_training'
    folder_mat = 'data_train_mat/'
else:
    log_folder = 'data_raw_testing'
    folder_mat = 'data_test_mat/'

# start = len(log_folder.split('/'))

if os.path.exists(folder_mat):
    shutil.rmtree(folder_mat)
os.mkdir(folder_mat)

for root, dirs, files in os.walk(log_folder):
    for f in files:
        filename = os.path.join(root, f)
        extension = os.path.splitext(filename)[1]
        if '~' not in filename and extension == '.log':
            label_directory = root.replace(log_folder,'')
            label = label_directory.split('/')[1].split('_')[0]
            
            pos = label_directory.split('/')[2].split('_')[0]
            out_file = folder_mat + '/' + label + '_' + pos + '_' + filename.replace('/','_')

            out_file_txt = out_file + '.txt'
            out_file_mat = out_file + '.mat'

            cmd = 'grep \'\(G:\|A:\|M:\)\' \"' + filename + '\" | sed \'s/A:/1/\' |sed \'s/G:/2/\'| sed \'s/M:/3/\' | sed \'s/DEV: EnrC2B //\' > \"' + out_file_txt + '\" ; octave --eval \"addpath(\'matlab_utils\');save_mat(\'' + out_file_txt + '\', \'' + out_file_mat + '\')\"'
#			print cmd
            cmd = cmd + '&'
            os.system(cmd)

os.system('/bin/rm -rf ' + folder_mat + '/*.txt')
