"""
-----------------------------------------------------------------------------------------
plot_eye_traces_run.py
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
python behav_analysis/plot_eye_traces_run.py sub-01 EyeMov
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
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
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

# Platform settings 
# -----------------
if platform.system() == 'Darwin':
	main_dir = analysis_info['main_dir_mac']
    
elif platform.system() == 'Windows':
	main_dir = analysis_info['main_dir_pc']
runs = np.arange(0,analysis_info['num_run'],1)
rads = analysis_info['rads']

# Load data
# ---------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
h5_filename = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
h5_file = h5py.File(h5_filename,'r')
folder_alias = 'eye_traces'
eye_data = np.array(h5_file['{folder_alias}/eye_data_runs_int_blink'.format(folder_alias = folder_alias)])

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
	ax1,ax2,ax3,_ = draw_bg_trial(analysis_info)
	
	dur_run = (eye_data[run_eye_data_logic][-1,0]-eye_data[run_eye_data_logic][0,0])
	time_prct = (eye_data[run_eye_data_logic][:,0]- eye_data[run_eye_data_logic][0,0])/dur_run
	

	ax1.plot(time_prct,eye_data[run_eye_data_logic,1],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)
	ax2.plot(time_prct,eye_data[run_eye_data_logic,2],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)
	ax3.plot(eye_data[run_eye_data_logic,1],eye_data[run_eye_data_logic,2],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)
	ax3.text(8, -10, 'Run {run}'.format(run = run+1), horizontalalignment = 'left', verticalalignment = 'center', fontsize = 14)

	plt.savefig("{file_dir}/add/figures/run-{run_txt}/{sub}_task-{task}_run-{run_txt}_eyetraces.png".format(
															sub = subject,task = task,
															run_txt = run_txt,file_dir = file_dir),facecolor='w')
