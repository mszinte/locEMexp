%% General experiment launcher
%  =============================
% By     :  Vanessa C Morita
% Projet :  Localisers experiment
% With   :  Martin SZINTE & Anna MONTAGNINI & Guillaume MASSON
% Version:  1.0

% Version description
% ===================
% Experiment consists of a localiser
% - saccades vs pursuit vs fixation


% To do
% -----
% decide number of runs and change in sbjConfig.m line 35/36
% decide order of presentation of eye movements

% First settings
% --------------
Screen('CloseAll');clear all;clear mex;clear functions;close all;home;AssertOpenGL;

% General settings
% ----------------
const.expName           =   'locEMexp';     % experiment name.
const.expStart          =   0;              % Start of a recording exp                          0 = NO  , 1 = YES
const.checkTrial        =   0;              % Print trial conditions (for debugging)            0 = NO  , 1 = YES
const.writeLogTxt       =   1;              % write a log file in addition to eyelink file      0 = NO  , 1 = YES
const.mkVideo           =   0;              % Make a video of a run (on mac not linux)          0 = NO  , 1 = YES

% External controls
% -----------------
const.tracker           =   0;              % run with eye tracker                              0 = NO  , 1 = YES
const.scanner           =   0;              % run in MRI scanner                                0 = NO  , 1 = YES
const.scannerTest       =   1;              % run with T returned at TR time                    0 = NO  , 1 = YES
const.room              =   2;              % run in MRI or eye-tracking room                   1 = MRI , 2 = eye-tracking

% Run order
% ---------
const.cond_run_order = [1;1;...             % run 01 - SaccPursFix_run01      run 02 - SaccPursFix_run02
                        1;1;...             % run 03 - SaccPursFix_run03      run 04 - SaccPursFix_run04
                        1;1;...             % run 05 - SaccPursFix_run05      run 06 - SaccPursFix_run06
                        1;1;...             % run 07 - SaccPursFix_run07      run 08 - SaccPursFix_run08
                        1;1];               % run 09 - SaccPursFix_run09      run 10 - SaccPursFix_run10

% Run number per condition
% ------------------------
const.cond_run_num   = [01;02;...
                        03;04;...
                        05;06;...
                        07;08;...
                        09;10];

% Desired screen setting
% ----------------------
const.desiredFD         =   120;            % Desired refresh rate
%fprintf(1,'\n\n\tDon''t forget to change before testing\n');
const.desiredRes        =   [1920,1080];    % Desired resolution

% Path
% ----
dir                     =   (which('expLauncher'));
cd(dir(1:end-18));

% Add Matlab path
% ---------------
addpath('config','main','conversion','eyeTracking','instructions','trials','stim','stats');


% Subject configuration
% ---------------------
[const]                 =   sbjConfig(const);
                        
% Main run
% --------
main(const);










