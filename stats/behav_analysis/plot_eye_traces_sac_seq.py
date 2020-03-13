"""
-----------------------------------------------------------------------------------------
plot_eye_traces_sac_seq.py
-----------------------------------------------------------------------------------------
Goal of the script:
Plot horizontal and vertical eye trace of each run
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
python behav_analysis/plot_eye_traces_sac_seq.py sub-01 EyeMov
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
import cortex
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors as colors
deb = ipdb.set_trace

# Specific imports
# ----------------
from sac_utils import draw_bg_trial

# Get inputs
# ----------
subject = sys.argv[1]
task = sys.argv[2]

# Define analysis parameters
# --------------------------
with open('behavior_settings.json') as f:
	json_s = f.read()
	analysis_info = json.loads(json_s)

# General settings 
# ----------------
if platform.system() == 'Darwin':
	main_dir = analysis_info['main_dir_mac']
    
elif platform.system() == 'Windows':
	main_dir = analysis_info['main_dir_pc']
runs = np.arange(0,analysis_info['num_run'],1)
eye_mov_seq = analysis_info['eye_mov_seq']
seq_trs = analysis_info['seq_trs']
pursuits_tr = np.arange(0,seq_trs,2)
saccades_tr = np.arange(1,seq_trs,2)

# Load data
# ---------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
h5_filename = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
h5_file = h5py.File(h5_filename,'r')
folder_alias = 'eye_traces'
eye_data = np.array(h5_file['{folder_alias}/eye_data_runs_int_blink'.format(folder_alias = folder_alias)])
time_start_seq = np.array(h5_file['{folder_alias}/time_start_seq'.format(folder_alias = folder_alias)])
time_end_seq = np.array(h5_file['{folder_alias}/time_end_seq'.format(folder_alias = folder_alias)])

time_start_trial = np.array(h5_file['{folder_alias}/time_start_trial'.format(folder_alias = folder_alias)])
time_end_trial = np.array(h5_file['{folder_alias}/time_end_trial'.format(folder_alias = folder_alias)])
amp_sequence = np.array(h5_file['{folder_alias}/amp_sequence'.format(folder_alias = folder_alias)])

# Define colors
# -------------
cmap = 'hsv'
cmap_steps = 16
col_offset = 0#1/14.0
base = cortex.utils.get_cmap(cmap)
val = np.linspace(0, 1,cmap_steps+1,endpoint=False)
colmap = colors.LinearSegmentedColormap.from_list('my_colmap',base(val), N = cmap_steps)

pursuit_polar_ang = np.deg2rad(np.arange(0,360,22.5))
pursuit_ang_norm  = (pursuit_polar_ang + np.pi) / (np.pi * 2.0)
pursuit_ang_norm  = (np.fmod(pursuit_ang_norm + col_offset,1))*cmap_steps
pursuit_col_mat = colmap(pursuit_ang_norm.astype(int))
pursuit_col_mat[:,3]=0.2
saccade_polar_ang = np.deg2rad(np.arange(0,360,22.5)+180)
saccade_ang_norm  = (saccade_polar_ang + np.pi) / (np.pi * 2.0)
saccade_ang_norm  = (np.fmod(saccade_ang_norm + col_offset,1))*cmap_steps
saccade_col_mat = colmap(saccade_ang_norm.astype(int))
saccade_col_mat[:,3] = 0.8
polar_ang = np.deg2rad(np.arange(0,360,22.5))
trials_seq = saccades_tr

# Draw figure
# -----------
axis_width = 0.75
# eye trace analysis per run
for run in runs:
	run_eye_data_logic = eye_data[:,3] == run

	if run > 10:run_txt = '{}'.format(run+1)
	else:run_txt = '0{}'.format(run+1)

	# Define figure folder
	try: os.makedirs('{file_dir}/add/figures/run-{run_txt}'.format(file_dir = file_dir,run_txt = run_txt))
	except: pass

	
	for sequence in eye_mov_seq:

		trials = np.arange(0,trials_seq[sequence],1)
		seq_eye_data_logic = np.logical_and(eye_data[:,0] >= time_start_seq[sequence,run],\
		                                    eye_data[:,0] <= time_end_seq[sequence,run])

		dur_seq = time_end_seq[sequence,run]-time_start_seq[sequence,run]

		if sequence > 10:sequence_txt = '{}'.format(sequence+1)
		else:sequence_txt = '0{}'.format(sequence+1)
		
		ax1,ax2,ax3,cbar_axis = draw_bg_trial(analysis_info,True)
		
		for trial_num,trial_plot in enumerate(trials_seq):


			trial_eye_data_logic = np.logical_and( 	eye_data[:,0] >= time_start_trial[trial_plot,sequence,run],
													eye_data[:,0] <= time_end_trial[trial_plot,sequence,run])

			data_logic = np.logical_and.reduce(np.array((run_eye_data_logic,seq_eye_data_logic,trial_eye_data_logic)))


			time_prct = ((eye_data[data_logic][:,0]- time_start_seq[sequence,run])/dur_seq)
			plot_color = saccade_col_mat[trial_num,:]

			ax1.plot(time_prct,eye_data[data_logic,1],color = plot_color,linewidth = axis_width*1.5)
			ax2.plot(time_prct,eye_data[data_logic,2],color = plot_color,linewidth = axis_width*1.5)
			ax3.plot(eye_data[data_logic,1],eye_data[data_logic,2],color = plot_color,linewidth = axis_width*1.5)
			ax3.text(5, -10, 'Run {run_txt} - Seq {sequence_txt}'.format(run_txt = run+1, sequence_txt = sequence+1), horizontalalignment = 'left', verticalalignment = 'center', fontsize = 14)

		plt.savefig("{file_dir}/add/figures/run-{run_txt}/{sub}_task-{task}_run-{run_txt}_seq-{sequence_txt}_eyetraces.png".format(
													sub = subject,
													task = task,
													run_txt = run_txt,
													sequence_txt = sequence_txt,
													file_dir = file_dir),facecolor='w')