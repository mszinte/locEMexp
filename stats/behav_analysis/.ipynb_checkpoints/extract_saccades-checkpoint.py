"""
-----------------------------------------------------------------------------------------
extract_saccades.py
-----------------------------------------------------------------------------------------
Goal of the script:
Extract saccade metrics
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject number (sub-01)
sys.argv[2]: task (EyeMov)
-----------------------------------------------------------------------------------------
Output(s):
h5 files with vals_all
vals_all[:,00]:	run number
vals_all[:,01]:	sequence number,
vals_all[:,02]:	trial number,
vals_all[:,03]:	saccade number detected (nan if no),
vals_all[:,04]:	saccade onset x coordinate (dva from screen center)
vals_all[:,05]:	saccade offset x coordinate (dva from screen center))
vals_all[:,06]:	saccade onset y coordinate (dva from screen center)
vals_all[:,07]:	saccade offset y coordinate (dva from screen center)),	
vals_all[:,08]:	saccade onset time trigger
vals_all[:,09]:	saccade offset time trigger
vals_all[:,10]:	saccade onset time relative to trial onset (proportion of the trial)
vals_all[:,11]:	saccade offset time relative to trial onset (proportion of the trial)
vals_all[:,12]:	saccade duration (ms)
vals_all[:,13]:	saccade velocity peak (dva/sec)
vals_all[:,14]:	saccade distance (dva)
vals_all[:,15]:	saccade amplitude (dva)
vals_all[:,16]:	saccade distance angle (degrees),
vals_all[:,17]:	saccade amplitude angle (degrees),
vals_all[:,18]:	saccade trial with correct fixation (start within boundary)
vals_all[:,19]:	saccade trial with correct saccade (end within boundary)
vals_all[:,20]:	saccade_task trial
vals_all[:,21]:	trial with missing time stamps
vals_all[:,22]:	saccade task with accurate saccade
vals_all[:,23]:	trial with no_saccade detected,
vals_all[:,24]:	microsaccade detected (<1 dva)
-----------------------------------------------------------------------------------------
To run:
cd /Users/martin/Dropbox/Experiments/pMFexp/stats/
python behav_analysis/extract_saccades.py sub-01 EyeMov
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
import json
import h5py
# import ipdb
# deb = ipdb.set_trace

# Specific imports
# ----------------
from sac_utils import vecvel, microsacc_merge, saccpar, isincircle

# Get inputs
# ----------
subject = sys.argv[1]
task = sys.argv[2]

# Define analysis parameters
# --------------------------
with open('behavior_settings.json') as f:
	json_s = f.read()
	analysis_info = json.loads(json_s)

# Platform settings 
# -----------------
if platform.system() == 'Darwin':
	main_dir = analysis_info['main_dir_mac']
    
elif platform.system() == 'Windows':
	main_dir = analysis_info['main_dir_pc']

runs = np.arange(0,analysis_info['num_run'],1)
sequences = np.arange(0,analysis_info['num_seq'],1)
trials_seq = analysis_info['trials_seq']
rads = analysis_info['rads']
polar_ang = np.deg2rad(np.arange(0,360,analysis_info['ang_steps']))
pursuits_tr = np.arange(0,analysis_info['seq_trs'],2)
saccades_tr = np.arange(1,analysis_info['seq_trs'],2)
seq_type = analysis_info['seq_type']

# Load data
# ---------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
h5_filename = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
h5_file = h5py.File(h5_filename,'r')
folder_alias = 'eye_traces'
eye_data_runs = np.array(h5_file['{folder_alias}/eye_data_runs'.format(folder_alias = folder_alias)])
time_start_seq = np.array(h5_file['{folder_alias}/time_start_seq'.format(folder_alias = folder_alias)])
time_end_seq = np.array(h5_file['{folder_alias}/time_end_seq'.format(folder_alias = folder_alias)])
time_start_trial = np.array(h5_file['{folder_alias}/time_start_trial'.format(folder_alias = folder_alias)])
time_end_trial = np.array(h5_file['{folder_alias}/time_end_trial'.format(folder_alias = folder_alias)])
amp_sequence = np.array(h5_file['{folder_alias}/amp_sequence'.format(folder_alias = folder_alias)])

# Get saccade model
# -----------------
sampling_rate = analysis_info['sampling_rate']
velocity_th = analysis_info['velocity_th']
min_dur = analysis_info['min_dur']
merge_interval = analysis_info['merge_interval']
tolerance_ratio = analysis_info['tolerance_ratio']

# Main loop
# ---------
mat = 0
for run in runs:
	# print('run: {}'.format(run))
	run_data_logic = eye_data_runs[:,3] == run

	for sequence in sequences:
		# print('sequence: {}'.format(sequence))
		trials = np.arange(0,trials_seq[sequence],1)
		seq_data_logic = np.logical_and(eye_data_runs[:,0] >= time_start_seq[sequence,run],\
										eye_data_runs[:,0] <= time_end_seq[sequence,run])

		trial_with_sac = 0
		for trial in trials:
			# print('trial: {}'.format(trial))
			trial_data_logic = np.logical_and(eye_data_runs[:,0] >= time_start_trial[trial,sequence,run],\
											  eye_data_runs[:,0] <= time_end_trial[trial,sequence,run])
			
			data_logic = np.logical_and.reduce(np.array((run_data_logic,seq_data_logic,trial_data_logic)))

			# fixation target position
			if amp_sequence[sequence] == 5:
				amp_sac = 0
				fix_pos_x, fix_pos_y = 0,0
				sac_pos_x,sac_pos_y = 0,0
			else:
				amp_sac = rads[int(amp_sequence[sequence])]
				fix_pos_x, fix_pos_y = np.round(np.cos(polar_ang[trial_with_sac])*amp_sac,decimals=3),\
								   	   np.round(np.sin(polar_ang[trial_with_sac])*amp_sac,decimals=3)
				sac_pos_x,sac_pos_y = 0,0

			# trial start and end
			# define trial start and trial end
			t_trial_start = time_start_trial[trial,sequence,run]
			t_trial_end = time_end_trial[trial,sequence,run]
			dur_trial = t_trial_end - t_trial_start
			time_prct = ((eye_data_runs[data_logic][:,0]- t_trial_start)/dur_trial)

			# Indicators
			saccade_task = 0	 #0 saccade task
			miss_time = 0        #1 missing data
			sac_accuracy = 0     #2 saccade accuracy (only fixation in right area)
			microsaccade = 0     #3 microsaccade
			no_saccade = 0       #4 no saccade detected

			# Saccade analysis parameters
			num_res = 25
			sac_fix_rad = tolerance_ratio*amp_sac

			#0 Saccade task
			if seq_type[sequence] == 1:
				if np.sum(saccades_tr==trial):
					saccade_task = 1
					trial_with_sac += 1

			#1 Missing data point
			if np.sum(np.diff(eye_data_runs[trial_data_logic,0])>1000/sampling_rate) > 0:
				miss_time = 1



			#2 saccade detection
			if not miss_time:
				t, p, x, y = eye_data_runs[trial_data_logic,0],time_prct,eye_data_runs[trial_data_logic,1],eye_data_runs[trial_data_logic,2]
				vx, vy = vecvel(x,y,sampling_rate)                
				sac = microsacc_merge(x,y,vx,vy,velocity_th,min_dur,merge_interval)
				ms = saccpar(sac)

				if np.isnan(ms[0,0]):
					#4 no saccade
					no_saccade = 1
					s1 = 0
					if mat == 0:
						vals_all = np.array([	run,			sequence,		trial,			np.nan,			np.nan,\
												np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
												np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
												np.nan,			np.nan,			np.nan,			fix_cor,		sac_cor,\
												saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])

						mat = 1
					else:
						vals_all = np.vstack((vals_all,np.array([	run,			sequence,		trial,			np.nan,			np.nan,\
																	np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
																	np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
																	np.nan,			np.nan,			np.nan,			fix_cor,		sac_cor,\
																	saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])))

				else:
					n_sac_tot = ms.shape[0]
					s1 = 0
					while s1 < n_sac_tot:
						sac_x_onset,	sac_x_offset	=	x[int(ms[s1,0])], 	x[int(ms[s1,1])]
						sac_y_onset,	sac_y_offset	=	y[int(ms[s1,0])], 	y[int(ms[s1,1])]
						sac_t_onset,	sac_t_offset	=	t[int(ms[s1,0])], 	t[int(ms[s1,1])]
						sac_p_onset,	sac_p_offset	=	p[int(ms[s1,0])], 	p[int(ms[s1,1])]
						sac_dur,		sac_vpeak		=	ms[s1,2],			ms[s1,3]
						sac_dist,		sac_amp			= 	ms[s1,4],			ms[s1,6]
						sac_dist_ang,	sac_amp_ang		= 	ms[s1,5],			ms[s1,7]

						fix_cor = isincircle(sac_x_onset,sac_y_onset,fix_pos_x,fix_pos_y,sac_fix_rad)
						sac_cor = isincircle(sac_x_offset,sac_y_offset,sac_pos_x,sac_pos_y,sac_fix_rad)

						if np.logical_and(fix_cor,sac_cor):sac_accuracy = 1;
						else:sac_accuracy = 0;

						#3 microsaccade
						if sac_amp <= 1.0:microsaccade = 1

						# extract metrics
						if mat == 0:
							vals_all = np.array([	run,			sequence,		trial,			s1,				sac_x_onset,\
													sac_x_offset,	sac_y_onset,	sac_y_offset,	sac_t_onset,	sac_t_offset,\
													sac_p_onset,	sac_p_offset,	sac_dur,		sac_vpeak,		sac_dist,\
													sac_amp,		sac_dist_ang,	sac_amp_ang,	fix_cor,		sac_cor,\
													saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])
							mat = 1
						else:
						    vals_all = np.vstack((vals_all,np.array([	run,			sequence,		trial,			s1,				sac_x_onset,\
																		sac_x_offset,	sac_y_onset,	sac_y_offset,	sac_t_onset,	sac_t_offset,\
																		sac_p_onset,	sac_p_offset,	sac_dur,		sac_vpeak,		sac_dist,\
																		sac_amp,		sac_dist_ang,	sac_amp_ang,	fix_cor,		sac_cor,\
																		saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])))
						s1 += 1
			else:
				if mat == 0:
					vals_all = np.array([	run,			sequence,		trial,			np.nan,			np.nan,\
											np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
											np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
											np.nan,			np.nan,			np.nan,			fix_cor,		sac_cor,\
											saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])
					mat = 1
				else:
					vals_all = np.vstack((vals_all,np.array([	run,			sequence,		trial,			np.nan,			np.nan,\
																np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
																np.nan,			np.nan,			np.nan,			np.nan,			np.nan,\
																np.nan,			np.nan,			np.nan,			fix_cor,		sac_cor,\
																saccade_task, 	miss_time,		sac_accuracy,	no_saccade,		microsaccade])))


# Save all
# --------
h5_file = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
folder_alias = 'saccades'
h5file = h5py.File(h5_file, "a")
try:h5file.create_group(folder_alias)
except:None

h5file.create_dataset(  '{folder_alias}/saccades_output'.format(folder_alias = folder_alias),
						data = vals_all,dtype ='float32')