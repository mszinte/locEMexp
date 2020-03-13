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


# Define experiments details
# --------------------------
num_run = analysis_info['num_run']
rads = analysis_info['rads']

# Load data
# ---------
file_dir = '{exp_dir}/data/{sub}'.format(exp_dir = main_dir, sub = subject)
h5_filename = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
h5_file = h5py.File(h5_filename,'r')
folder_alias = 'eye_traces'
eye_data_runs_no_blink = np.array(h5_file['{folder_alias}/eye_data_runs_no_blink'.format(folder_alias = folder_alias)])

# Draw figure
# -----------

# Define figure
title_font = {'loc':'left', 'fontsize':14, 'fontweight':'bold'}
axis_label_font = {'fontsize':14}
bg_col = (0.9, 0.9, 0.9)
axis_width = 0.75
line_width_corr = 1.5

# Horizontal eye trace settings
screen_val =  12.5
ymin1,ymax1,y_tick_num1 = -screen_val,screen_val,11
xmin1,xmax1,x_tick_num1 = 0,1,num_run+1
y_tick1 = np.linspace(ymin1,ymax1,y_tick_num1)
x_tick1 = np.linspace(xmin1,xmax1,x_tick_num1)

# Vertical eye trace settings
ymin2,ymax2,y_tick_num2 = -screen_val,screen_val,11
xmin2,xmax2,x_tick_num2 = 0,1,num_run+1
y_tick2 = np.linspace(ymin2,ymax2,y_tick_num2)
x_tick2 = np.linspace(xmin2,xmax2,x_tick_num2)

# eye trace analysis per run
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

	eye_data_logic = eye_data_runs_no_blink[:,3] == run_plot
	dur_run = (eye_data_runs_no_blink[eye_data_logic][-1,0]-eye_data_runs_no_blink[eye_data_logic][0,0])
	time_prct = (eye_data_runs_no_blink[eye_data_logic][:,0]- eye_data_runs_no_blink[eye_data_logic][0,0])/dur_run

	xmin1,xmax1,x_tick_num1 = 0,1,5
	xmin2,xmax2,x_tick_num2 = 0,1,5
	x_tick1 = np.linspace(xmin1,xmax1,x_tick_num1)
	x_tick2 = np.linspace(xmin2,xmax2,x_tick_num2)

	# Horizontal eye trace
	ax1 = plt.subplot2grid((2,8),(0,0),rowspan= 1, colspan = 4)
	ax1.set_ylabel('Hor. coord. (dva)',axis_label_font,labelpad = 0)
	ax1.set_ylim(bottom = ymin1, top = ymax1)
	ax1.set_yticks(y_tick1)
	ax1.set_xlabel('Time (%)',axis_label_font,labelpad = 10)
	ax1.set_xlim(left = xmin1, right = xmax1)
	ax1.set_xticks(x_tick1)
	ax1.set_facecolor(bg_col)
	ax1.set_title('Horizontal eye position',**title_font)
	ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
	for rad in rads:
	    ax1.plot(time_prct,time_prct*0+rad, color = [1,1,1], linewidth = axis_width*2)
	    ax1.plot(time_prct,time_prct*0-rad, color = [1,1,1], linewidth = axis_width*2)

	ax1.plot(time_prct,eye_data_runs_no_blink[eye_data_logic,1],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)

	# Vertical eye trace
	ax2 = plt.subplot2grid((2,8),(1,0),rowspan= 1, colspan = 4)
	ax2.set_ylabel('Ver. coord. (dva)',axis_label_font, labelpad = 0)
	ax2.set_ylim(bottom = ymin2, top = ymax2)
	ax2.set_yticks(y_tick2)
	ax2.set_xlabel('Time (%)',axis_label_font, labelpad = 10)
	ax2.set_xlim(left = xmin2, right = xmax2)
	ax2.set_xticks(x_tick2)
	ax2.set_facecolor(bg_col)
	ax2.set_title('Vertical eye position',**title_font)
	ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
	for rad in rads:
		ax2.plot(time_prct,time_prct*0+rad, color = [1,1,1], linewidth = axis_width*2)
		ax2.plot(time_prct,time_prct*0-rad, color = [1,1,1], linewidth = axis_width*2)

	ax2.plot(time_prct,eye_data_runs_no_blink[eye_data_logic,2],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)

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

	ax3.plot(eye_data_runs_no_blink[eye_data_logic,1],eye_data_runs_no_blink[eye_data_logic,2],color = [0.5,0.5,0.5],linewidth = axis_width*1.5)
	ax3.text(8, -10, 'Run {run_plot}'.format(run_plot = run_plot+1), horizontalalignment = 'left', verticalalignment = 'center', fontsize = 14)

	plt.subplots_adjust(wspace = 1.4,hspace = 0.4)

	plt.savefig("{file_dir}/add/figures/run-{run_plot_txt}/{sub}_task-{task}_run-{run_plot_txt}_eyetraces.png".format(
																sub = subject,
																task = task,
																run_plot_txt = run_plot_txt,
																file_dir = file_dir, 
																run_plot = run_plot),facecolor='w')