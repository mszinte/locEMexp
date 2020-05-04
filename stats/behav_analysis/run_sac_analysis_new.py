# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# To do
# -----
# 1. find way to select the first correct saccade
# 5. rotate all data per eccentricity to fit 2D non isometric gaussian on distibution of landing point
# 6. extract and plot with saccade metrics across all runs (saccade landing, saccade amplitude, saccade velocity peak, saccade accuracy, saccade precision)
# 6. apply anemo model to smooth pursuit eye traces rotated to main axis

# 1. run extract_eyetraces
# 2. run extract_saccades

# %%
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
# np.set_printoptions(threshold=sys.maxsize)

from sac_utils import draw_bg_trial

# Get inputs
# ----------
subject = 'sub-01'
task = 'LocSacc' # 'LocPurs'

# Define analysis parameters
# --------------------------
with open('../behavior_settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# Settings 
# --------
if platform.system() == 'Darwin':
    main_dir = analysis_info['main_dir_mac']
    
elif platform.system() == 'Windows':
    main_dir = analysis_info['main_dir_pc']
    
elif platform.system() == 'Linux':
    main_dir = analysis_info['main_dir_unix']
    
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
eye_traces_alias = 'eye_traces'
eye_data = np.array(h5_file['{folder_alias}/eye_data_runs'.format(folder_alias = eye_traces_alias)])
eye_data_int_blink = np.array(h5_file['{folder_alias}/eye_data_runs_int_blink'.format(folder_alias = eye_traces_alias)])
time_start_seq = np.array(h5_file['{folder_alias}/time_start_seq'.format(folder_alias = eye_traces_alias)])
time_end_seq = np.array(h5_file['{folder_alias}/time_end_seq'.format(folder_alias = eye_traces_alias)])

time_start_trial = np.array(h5_file['{folder_alias}/time_start_trial'.format(folder_alias = eye_traces_alias)])
time_end_trial = np.array(h5_file['{folder_alias}/time_end_trial'.format(folder_alias = eye_traces_alias)])
amp_sequence = np.array(h5_file['{folder_alias}/amp_sequence'.format(folder_alias = eye_traces_alias)])
saccades_alias = 'saccades'
saccades_output = np.array(h5_file['{folder_alias}/saccades_output'.format(folder_alias = saccades_alias)])


# %%
# figure settings
axis_width = 0.75
linewidth_sac = axis_width*4
screen_val =  12.5

for run in runs:
    run_eye_data_logic = eye_data[:,3] == run
    run_saccade_logic = saccades_output[:,0] == run
    if run > 10:run_txt = '{}'.format(run+1)
    else:run_txt = '0{}'.format(run+1)
    
    for sequence in sequences:
        trials = np.arange(0,trials_seq[sequence],1)
        seq_eye_data_logic = np.logical_and(eye_data[:,0] >= time_start_seq[sequence,run],                                            eye_data[:,0] <= time_end_seq[sequence,run])
        sequence_saccade_logic = saccades_output[:,1] == sequence

        if sequence > 10:sequence_txt = '{}'.format(sequence+1)
        else:sequence_txt = '0{}'.format(sequence+1)

        # make figure folder
        try: os.makedirs('{file_dir}/add/figures/run-{run_txt}/seq-{sequence_txt}/'.format(
                                file_dir = file_dir, run_txt = run_txt, sequence_txt = sequence_txt))
        except: pass

        for trial in trials:
            if trial > 10:trial_txt = '{}'.format(trial+1)
            else:trial_txt = '0{}'.format(trial+1)
            
            t_trial_start = time_start_trial[trial,sequence,run]
            t_trial_end = time_end_trial[trial,sequence,run]
            trial_eye_data_logic = np.logical_and(  eye_data[:,0] >= t_trial_start,                                                    eye_data[:,0] <= t_trial_end)
            trial_saccade_logic = saccades_output[:,2] == trial
            
            eye_data_logic = np.logical_and.reduce(np.array((run_eye_data_logic,seq_eye_data_logic,trial_eye_data_logic)))
            saccade_logic = np.logical_and.reduce(np.array((run_saccade_logic,sequence_saccade_logic,trial_saccade_logic)))
            
            # trial start and end
            # define trial start and trial end
            time_prct = ((eye_data[eye_data_logic][:,0]- t_trial_start)/(t_trial_end - t_trial_start))
            t, p, x, y = eye_data[eye_data_logic,0],time_prct,eye_data[eye_data_logic,1],eye_data[eye_data_logic,2]
            xnb, ynb = eye_data_int_blink[eye_data_logic,1],eye_data_int_blink[eye_data_logic,2]

            ax1,ax2,ax3 = draw_bg_trial()
            # plot whole trial
            ax1.plot(time_prct,x,color = [0.7,0.7,0.7],linewidth = axis_width)
            ax1.plot(time_prct,xnb,color = [0,0,0],linewidth = axis_width*1.5)
            ax2.plot(time_prct,y,color = [0.7,0.7,0.7],linewidth = axis_width)
            ax2.plot(time_prct,ynb,color = [0,0,0],linewidth = axis_width*1.5)
            ax3.plot(x,y,color = [0.7,0.7,0.7],linewidth = axis_width)
            ax3.plot(xnb,ynb,color = [0,0,0],linewidth = axis_width*1.5)
            ax3.text(7.5, -10, 'Run {run_plot} - Seq {seq_plot}'.format(run_plot = run+1, seq_plot = sequence+1), horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14)
            ax3.text(7.5, -11.5, 'Trial {trial_num}'.format(trial_num = trial+1), horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14)

            saccades_trial = saccades_output[saccade_logic]
            if np.isnan(saccades_trial[:,3][0]) == False:
                for saccade_num in saccades_trial[:,3]:
                    
                    saccade_num_logic = saccades_trial[:,3] == saccade_num
                    saccade_output = saccades_trial[saccade_num_logic,:]

                    sac_t_onset = saccade_output[0,8]
                    sac_t_offset = saccade_output[0,9]
                    sac_p_onset = saccade_output[0,10]
                    sac_p_offset = saccade_output[0,11]
                    blink_saccade = saccade_output[0,25]
                    
                    if blink_saccade == 0:
                    
                        x_sac = x[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                        y_sac = y[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                        t_sac = t[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                        p_sac = p[np.logical_and(t > sac_t_onset,t < sac_t_offset)]

                        ax1.fill([sac_p_onset,sac_p_offset,sac_p_offset,sac_p_onset],[screen_val,screen_val,-screen_val,-screen_val],color = [0.7,0.7,0.7])
                        ax1.plot(p_sac,x_sac,color = [0,0,0],linewidth = linewidth_sac)
                        ax2.fill([sac_p_onset,sac_p_offset,sac_p_offset,sac_p_onset],[screen_val,screen_val,-screen_val,-screen_val],color = [0.7,0.7,0.7])
                        ax2.plot(p_sac,y_sac,color = [0,0,0],linewidth = linewidth_sac)
                        ax3.plot(x_sac,y_sac,color = [0,0,0],linewidth = linewidth_sac)
                    
            plt.savefig("{file_dir}/add/figures/run-{run_txt}/seq-{sequence_txt}/{sub}_task-{task}_run-{run_txt}_seq-{sequence_txt}_trial-{trial_txt}_eyetrace.png".format(
                                                                sub = subject,task = task,
                                                                run_txt = run_txt,
                                                                sequence_txt = sequence_txt,
                                                                trial_txt = trial_txt,
                                                                file_dir = file_dir),facecolor='w')


# %%
blink_saccade


# %%

                
            
            data_logic = np.logical_and.reduce(np.array((run_data_logic,seq_data_logic,trial_data_logic)))
            
            
            
            
            
            for trial_sac in vals_trial[:,4]:
                trial_sac_logic = vals_trial[:,4] == trial_sac
                vals_trial_sac = vals_trial[trial_sac_logic,:]


                sac_t_onset = vals_trial_sac[0,9]
                sac_t_offset = vals_trial_sac[0,10]
                sac_p_onset = vals_trial_sac[0,11]
                sac_p_offset = vals_trial_sac[0,12]
                sac_acc = vals_trial_sac[0,22]
                
                x_sac = x[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                y_sac = y[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                t_sac = t[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
                p_sac = p[np.logical_and(t > sac_t_onset,t < sac_t_offset)]
            
                if sac_acc:
                    plot_color = saccade_col_mat[trial_num,:]
                    linewidth_sac = axis_width*4
                else:
                    plot_color = [0,0,0]
                    linewidth_sac = axis_width*1.5
            
                ax1.fill([sac_p_onset,sac_p_offset,sac_p_offset,sac_p_onset],[screen_val,screen_val,-screen_val,-screen_val],color = [0.7,0.7,0.7])
                ax1.plot(p_sac,x_sac,color = plot_color,linewidth = linewidth_sac)
                ax2.fill([sac_p_onset,sac_p_offset,sac_p_offset,sac_p_onset],[screen_val,screen_val,-screen_val,-screen_val],color = [0.7,0.7,0.7])
                ax2.plot(p_sac,y_sac,color = plot_color,linewidth = linewidth_sac)
                ax3.plot(x_sac,y_sac,color = plot_color,linewidth = linewidth_sac)
                plt.savefig("{file_dir}/add/figures/run-{run_plot_txt}/seq-{seq_plot_txt}/{sub}_task-{task}_run-{run_plot_txt}_seq-{seq_plot_txt}_trial-{trial_plot_txt}_saccades.png".format(
                                                                sub = subject,
                                                                task = task,
                                                                run_plot_txt = run_plot_txt,
                                                                seq_plot_txt = seq_plot_txt,
                                                                trial_plot_txt = trial_plot_txt,
                                                                file_dir = file_dir, 
                                                                run_plot = run_plot),facecolor='w')
        
# Save all
# --------
h5_file = "{file_dir}/add/{sub}_task-{task}_eyedata.h5".format(file_dir = file_dir, sub = subject, task = task)
folder_alias = 'saccades'
h5file = h5py.File(h5_file, "a")
try:h5file.create_group(folder_alias)
except:None

h5file.create_dataset(  '{folder_alias}/eye_data_runs'.format(folder_alias = folder_alias),
                        data = vals_all,dtype ='float32')       


# %%


