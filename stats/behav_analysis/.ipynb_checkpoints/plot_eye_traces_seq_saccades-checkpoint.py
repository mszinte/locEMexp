"""
-----------------------------------------------------------------------------------------
plot_eye_traces_seq_saccades.py
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
python behav_analysis/plot_eye_traces_seq_saccades.py sub-01 EyeMov
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
num_run = analysis_info['num_run']
seq_trs = analysis_info['seq_trs']
eye_mov_seq = analysis_info['eye_mov_seq']
rads = analysis_info['rads']
pursuits_tr = np.arange(0,seq_trs,2)
saccades_tr = np.arange(1,seq_trs,2)


# Load data
# ---------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
h5_filename = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
h5_file = h5py.File(h5_filename,'r')
folder_alias = 'eye_traces'
eye_data_runs_no_blink = np.array(h5_file['{folder_alias}/eye_data_runs_no_blink'.format(folder_alias = folder_alias)])
eye_data_runs = np.array(h5_file['{folder_alias}/eye_data_runs'.format(folder_alias = folder_alias)])
time_start_seq = np.array(h5_file['{folder_alias}/time_start_seq'.format(folder_alias = folder_alias)])
time_end_seq = np.array(h5_file['{folder_alias}/time_end_seq'.format(folder_alias = folder_alias)])

time_start_trial = np.array(h5_file['{folder_alias}/time_start_trial'.format(folder_alias = folder_alias)])
time_end_trial = np.array(h5_file['{folder_alias}/time_end_trial'.format(folder_alias = folder_alias)])
amp_sequence = np.array(h5_file['{folder_alias}/amp_sequence'.format(folder_alias = folder_alias)])

# Figure settings
# ---------------
# Define figure
title_font = {'loc':'left', 'fontsize':14, 'fontweight':'bold'}
axis_label_font = {'fontsize':14}
bg_col = (0.9, 0.9, 0.9)
axis_width = 0.75
line_width_corr = 1.5

# Horizontal eye trace
screen_val = 12.5
ymin1,ymax1,y_tick_num1 = -screen_val,screen_val,11
xmin1,xmax1,x_tick_num1 = 0,1,5
y_tick1 = np.linspace(ymin1,ymax1,y_tick_num1)
x_tick1 = np.linspace(xmin1,xmax1,x_tick_num1)

# Vertical eye trace
ymin2,ymax2,y_tick_num2 = -screen_val,screen_val,11
xmin2,xmax2,x_tick_num2 = 0,1,num_run+1
y_tick2 = np.linspace(ymin2,ymax2,y_tick_num2)
x_tick2 = np.linspace(xmin2,xmax2,x_tick_num2)

# Define colors
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

try: os.makedirs('{file_dir}/add/figures/'.format(file_dir = file_dir))
except: pass

# main loop
for run_plot in np.arange(0,num_run,1):

	# define run name
	if run_plot > 10:
		run_plot_txt = '{}'.format(run_plot+1)
	else:
		run_plot_txt = '0{}'.format(run_plot+1)

	# Define figure folder
	try: os.makedirs('{file_dir}/add/figures/run-{run_plot_txt}'.format(file_dir = file_dir,run_plot_txt = run_plot_txt))
	except: pass

	fig = plt.figure(figsize = (15, 7))
	gridspec.GridSpec(2,8)
	run_data_logic = eye_data_runs_no_blink[:,3] == run_plot

	for seq_plot in eye_mov_seq:

		# define seq name
		if seq_plot > 10:
			seq_plot_txt = '{}'.format(seq_plot+1)
		else:
			seq_plot_txt = '0{}'.format(seq_plot+1)

		seq_data_logic = np.logical_and(eye_data_runs_no_blink[:,0] >= time_start_seq[seq_plot,run_plot],
										eye_data_runs_no_blink[:,0] <= time_end_seq[seq_plot,run_plot])

		dur_seq = time_end_seq[seq_plot,run_plot]-time_start_seq[seq_plot,run_plot]
        
		# Horizontal eye trace
		ax1 = plt.subplot2grid((2,8),(0,0),rowspan= 1, colspan = 4)
		ax1.set_ylabel('Hor. coord. (dva)',axis_label_font,labelpad = 0)
		ax1.set_ylim(bottom = ymin1, top = ymax1)
		ax1.set_yticks(y_tick1)
		ax1.set_xlabel('Time (%)',axis_label_font,labelpad = 10)
		ax1.set_xlim(left = xmin1, right = xmax1)
		ax1.set_xticks(x_tick1)
		ax1.set_facecolor(bg_col)
		ax1.set_title('Saccades: Horizontal eye position',**title_font)
		ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))

		for rad in rads:
			ax1.plot(x_tick1,x_tick1*0+rad, color = [1,1,1], linewidth = axis_width*2)
			ax1.plot(x_tick1,x_tick1*0-rad, color = [1,1,1], linewidth = axis_width*2)

		# Vertical eye trace
		ax2 = plt.subplot2grid((2,8),(1,0),rowspan= 1, colspan = 4)
		ax2.set_ylabel('Ver. coord. (dva)',axis_label_font, labelpad = 0)
		ax2.set_ylim(bottom = ymin2, top = ymax2)
		ax2.set_yticks(y_tick2)
		ax2.set_xlabel('Time (%)',axis_label_font, labelpad = 10)
		ax2.set_xlim(left = xmin2, right = xmax2)
		ax2.set_xticks(x_tick2)
		ax2.set_facecolor(bg_col)
		ax2.set_title('Saccades: Vertical eye position',**title_font)
		ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
		for rad in rads:
			ax2.plot(x_tick2,x_tick2*0+rad, color = [1,1,1], linewidth = axis_width*2)
			ax2.plot(x_tick2,x_tick2*0-rad, color = [1,1,1], linewidth = axis_width*2)

		# Screen eye trace
		ax3 = plt.subplot2grid((2,8),(0,4),rowspan= 2, colspan = 4)
		ax3.set_xlabel('Horizontal coordinates (dva)', axis_label_font, labelpad = 10)
		ax3.set_ylabel('Vertical coordinates (dva)', axis_label_font, labelpad = 0)
		ax3.set_xlim(left = ymin1, right = ymax1)
		ax3.set_xticks(y_tick1)
		ax3.set_ylim(bottom = ymin2, top = ymax2)
		ax3.set_yticks(y_tick2)
		ax3.set_facecolor(bg_col)
		ax3.set_title('Screen view',**title_font)
		ax3.set_aspect('equal')

		theta = np.linspace(0, 2*np.pi, 100)
		for rad in rads:
			ax3.plot(rad*np.cos(theta), rad*np.sin(theta),color = [1,1,1],linewidth = axis_width*3)

		ax3.text(5, -10, 'Run {run_plot} - Seq {seq_plot}'.format(run_plot = run_plot+1, seq_plot = seq_plot+1), horizontalalignment = 'left', verticalalignment = 'center', fontsize = 14)
    
		for trial_num,trial_plot in enumerate(trials_seq):
			trial_data_logic = np.logical_and( eye_data_runs_no_blink[:,0] >= time_start_trial[trial_plot,seq_plot,run_plot],
												eye_data_runs_no_blink[:,0] <= time_end_trial[trial_plot,seq_plot,run_plot])

			data_logic = np.logical_and.reduce(np.array((run_data_logic,seq_data_logic,trial_data_logic)))

			time_prct = ((eye_data_runs_no_blink[data_logic][:,0]- time_start_seq[seq_plot,run_plot])/dur_seq)

			plot_color = saccade_col_mat[trial_num,:]

			ax1.plot(time_prct,eye_data_runs_no_blink[data_logic,1],color = plot_color,linewidth = axis_width*1.5)
			ax2.plot(time_prct,eye_data_runs_no_blink[data_logic,2],color = plot_color,linewidth = axis_width*1.5)
			ax3.plot(eye_data_runs_no_blink[data_logic,1],eye_data_runs_no_blink[data_logic,2],color = plot_color,linewidth = axis_width*1.5)

		plt.subplots_adjust(wspace = 1.4,hspace = 0.4)

		# color legend
		cbar_axis = fig.add_axes([0.47, 0.77, 0.8, 0.1], projection='polar')
		norm = colors.Normalize(0, 2*np.pi)
		t = np.linspace(0,2*np.pi,200,endpoint=True)
		r = [0,1]
		rg, tg = np.meshgrid(r,t)
		im = cbar_axis.pcolormesh(t, r, tg.T,norm= norm, cmap = colmap)
		cbar_axis.set_yticklabels([])
		cbar_axis.set_xticklabels([])
		cbar_axis.set_theta_zero_location("W",offset = -360/cmap_steps/2)
		cbar_axis.spines['polar'].set_visible(False)

		plt.savefig("{file_dir}/add/figures/run-{run_plot_txt}/{sub}_task-{task}_run-{run_plot_txt}_seq-{seq_plot_txt}_saccades.png".format(
													sub = subject,
													task = task,
													run_plot_txt = run_plot_txt,
													seq_plot_txt = seq_plot_txt,
													file_dir = file_dir, 
													run_plot = run_plot),facecolor='w')