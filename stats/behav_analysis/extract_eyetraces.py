"""
-----------------------------------------------------------------------------------------
extract_eyetraces.py
-----------------------------------------------------------------------------------------
Goal of the script:
Extract eye traces from edf file and arrange them well for later treatment
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject number (sub-01)
sys.argv[2]: task (EyeMov)
-----------------------------------------------------------------------------------------
Output(s):
h5 files with loads of data on eye traces across runs
-----------------------------------------------------------------------------------------
To run:
cd /Users/martin/Dropbox/Experiments/pMFexp/stats/
python behav_analysis/extract_eyetraces.py sub-01 EyeMov
-----------------------------------------------------------------------------------------
"""

# Stop warnings
# -------------
import warnings
warnings.filterwarnings("ignore")

# General imports
# ---------------
import os
import sys
import platform
import numpy as np
import ipdb
import json
import h5py
import scipy.io
deb = ipdb.set_trace

# Get inputs
# ----------
subject = sys.argv[1]
task = sys.argv[2]

# Define analysis parameters
# --------------------------
with open('behavior_settings.json') as f:
	json_s = f.read()
	analysis_info = json.loads(json_s)

# Get eyelink data
# ----------------
if platform.system() == 'Darwin':
	main_dir = analysis_info['main_dir_mac']
	edf2asc_dir = analysis_info['edf2asc_dir_mac']
	end_file = ''
    
elif platform.system() == 'Windows':
	main_dir = analysis_info['main_dir_pc']
	edf2asc_dir = analysis_info['edf2asc_dir_win']
	end_file ='.exe'
    

# Define file list
# ----------------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
list_filename = ['{sub}_task-{task}_run-01'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-02'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-03'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-04'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-05'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-06'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-07'.format(sub = subject, task = task),
			 	 '{sub}_task-{task}_run-08'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-09'.format(sub = subject, task = task),
				 '{sub}_task-{task}_run-10'.format(sub = subject, task = task)]


# Define experiments details
# --------------------------
num_run = analysis_info['num_run']
num_seq = analysis_info['num_seq']
seq_trs = analysis_info['seq_trs']
eye_mov_seq = analysis_info['eye_mov_seq']
rads = analysis_info['rads']
pursuits_tr = np.arange(0,seq_trs,2)
saccades_tr = np.arange(1,seq_trs,2)


# Exctract data
# -------------
eye_data_runs = [];
time_last_run_eye   =   0;
time_start_eye = np.zeros((1,num_run))
time_end_eye = np.zeros((1,num_run))
time_start_seq = np.zeros((num_seq,num_run))
time_end_seq = np.zeros((num_seq,num_run))
time_start_trial = np.zeros((seq_trs,num_seq,num_run))
time_end_trial = np.zeros((seq_trs,num_seq,num_run))
for t_run in np.arange(0,num_run,1):

	edf_filename = '{file_dir}/func/{filename}_eyeData'.format(file_dir = file_dir,filename = list_filename[t_run]);
	mat_filename = '{file_dir}/add/{filename}_matFile.mat'.format(file_dir = file_dir,filename = list_filename[t_run]);

	# get .msg and .dat file
	if not os.path.exists('{}.dat'.format(edf_filename)) or not os.path.exists('{}.msg'.format(edf_filename)):
		os.system('{edf2asc_dir}/edf2asc{end_file} {edf_filename}.edf -e -y'.format(edf2asc_dir = edf2asc_dir,
		                                                                            end_file = end_file,
		                                                                            edf_filename = edf_filename))
		os.rename('{}.asc'.format(edf_filename),'{}.msg'.format(edf_filename))

		os.system('{edf2asc_dir}/edf2asc{end_file} {edf_filename}.edf -s -miss -1.0 -y'.format( edf2asc_dir = edf2asc_dir,
		                                                                                        end_file = end_file,
		                                                                                        edf_filename = edf_filename))
		os.rename('{}.asc'.format(edf_filename),'{}.dat'.format(edf_filename))

	# get first and last time pf each run
	msgfid = open('{}.msg'.format(edf_filename))    
	first_last_time = False
	first_time = False
	last_time = False    
	seq_num = 0
	while not first_last_time:
		line_read = msgfid.readline()
		if not line_read == '':
			la = line_read.split()

		if len(la) > 6:
			if la[2] == 'sequence' and la[3]=='1' and la[4]=='started' and not first_time: 
				time_start_eye[0,t_run] = float(la[1])
				first_time = True
			    
			if la[2] == 'sequence' and la[3]=='9' and la[4]=='stopped' and not last_time: 
				time_end_eye[0,t_run] = float(la[1])
				last_time = True
			    
			if la[2] == 'sequence' and la[4]=='started':
				time_start_seq[seq_num,t_run] = float(la[1])
				trial_num = 0
			    
			if la[2] == 'sequence' and la[4]=='stopped':
				time_end_seq[seq_num,t_run] = float(la[1])
				seq_num += 1
			    
			if la[4] == 'trial' and la[6]=='onset':
				time_start_trial[trial_num,seq_num,t_run] = float(la[1])
			    
			if la[4] == 'trial' and la[6]=='offset':
				time_end_trial[trial_num,seq_num,t_run] = float(la[1])
				trial_num += 1                    
    
		if first_time == True and last_time == True:
			first_last_time = True
			msgfid.close();

            
	# load eye coord data
	eye_dat = np.genfromtxt('{}.dat'.format(edf_filename),usecols=(0, 1, 2))
	eye_data_run = eye_dat[np.logical_and(eye_dat[:,0]>=time_start_eye[0,t_run],eye_dat[:,0]<=time_end_eye[0,t_run])]

	# add run number
	eye_data_run = np.concatenate((eye_data_run,np.ones((eye_data_run.shape[0],1))*(t_run)),axis = 1)        
	# col 0 = time
	# col 2 = eye x coord
	# col 3 = eye y coord
	# col 4 = run number

	if t_run == 0:
		eye_data_runs = eye_data_run
	else:
		eye_data_runs = np.concatenate((eye_data_runs,eye_data_run), axis=0)

	# remove msg and dat
	os.remove('{}.msg'.format(edf_filename))
	os.remove('{}.dat'.format(edf_filename))

# Put nan for blink time
blinkNum = 0;
blink_start = False;
for tTime in np.arange(0,eye_data_runs.shape[0],1):
	
	if not blink_start:
		if eye_data_runs[tTime,1] == -1:
			
			blinkNum += 1
			timeBlinkOnset = eye_data_runs[tTime,0]
			blink_start = True
			if blinkNum == 1:
				blink_onset_offset = np.matrix([timeBlinkOnset,np.nan])
			else:
				blink_onset_offset = np.vstack((blink_onset_offset,[timeBlinkOnset,np.nan]))

	if blink_start:
		if eye_data_runs[tTime,1] != -1:
			timeBlinkOffset = eye_data_runs[tTime,0]
			blink_start = 0
			blink_onset_offset[blinkNum-1,1] = timeBlinkOffset

# nan record around detected blinks
eye_data_runs_nan_blink = np.copy(eye_data_runs)

for tBlink in np.arange(0,blinkNum,1):

	blink_onset_offset[tBlink,0] = blink_onset_offset[tBlink,0]
	blink_onset_offset[tBlink,1] = blink_onset_offset[tBlink,1]
	
	eye_data_runs_nan_blink[np.logical_and(eye_data_runs_nan_blink[:,0] >= blink_onset_offset[tBlink,0],eye_data_runs_nan_blink[:,0] <= blink_onset_offset[tBlink,1]),1] = np.nan
	eye_data_runs_nan_blink[np.logical_and(eye_data_runs_nan_blink[:,0] >= blink_onset_offset[tBlink,0],eye_data_runs_nan_blink[:,0] <= blink_onset_offset[tBlink,1]),2] = np.nan

# put eye coordinates in deg from center (flip y axis)
matfile = scipy.io.loadmat(mat_filename)
scr_sizeX = matfile['config']['scr'][0,0]['scr_sizeX'][0][0][0][0]
scr_sizeY = matfile['config']['scr'][0,0]['scr_sizeY'][0][0][0][0]
screen_size = np.array([scr_sizeX,scr_sizeY])
ppd = matfile['config']['const'][0,0]['ppd'][0][0][0][0]


eye_data_runs[:,1] = (eye_data_runs[:,1] - (screen_size[0]/2))/ppd;
eye_data_runs[:,2] = -1.0*((eye_data_runs[:,2] - (screen_size[1]/2))/ppd);
eye_data_runs_nan_blink[:,1] = (eye_data_runs_nan_blink[:,1] - (screen_size[0]/2))/ppd;
eye_data_runs_nan_blink[:,2] = -1.0*((eye_data_runs_nan_blink[:,2] - (screen_size[1]/2))/ppd);
amp_sequence = matfile['config']['expDes'][0,0]['amp_sequence'][0][0]


# Save all
# --------
h5_file = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
folder_alias = 'eye_traces'

try: os.system('rm {h5_file}'.format(h5_file = h5_file))
except: pass

h5file = h5py.File(h5_file, "a")
try:h5file.create_group(folder_alias)
except:None

h5file.create_dataset(  '{folder_alias}/eye_data_runs'.format(folder_alias = folder_alias),
                        data = eye_data_runs,dtype ='float32')
h5file.create_dataset(  '{folder_alias}/eye_data_runs_nan_blink'.format(folder_alias = folder_alias),
                        data = eye_data_runs_nan_blink,dtype ='float32')

h5file.create_dataset(  '{folder_alias}/time_start_eye'.format(folder_alias = folder_alias),
                        data = time_start_eye,dtype ='float32')
h5file.create_dataset(  '{folder_alias}/time_end_eye'.format(folder_alias = folder_alias),
                        data = time_end_eye,dtype ='float32')

h5file.create_dataset(  '{folder_alias}/time_start_seq'.format(folder_alias = folder_alias),
                        data = time_start_seq,dtype ='float32')
h5file.create_dataset(  '{folder_alias}/time_end_seq'.format(folder_alias = folder_alias),
                        data = time_end_seq,dtype ='float32')

h5file.create_dataset(  '{folder_alias}/time_start_trial'.format(folder_alias = folder_alias),
                        data = time_start_trial,dtype ='float32')
h5file.create_dataset(  '{folder_alias}/time_end_trial'.format(folder_alias = folder_alias),
                        data = time_end_trial,dtype ='float32')

h5file.create_dataset(  '{folder_alias}/amp_sequence'.format(folder_alias = folder_alias),
                        data = amp_sequence,dtype ='float32')

