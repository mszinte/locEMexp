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
% fix order to sac + pur + sac + pur
% fix task name to SacLoc and PurLoc
% adapt the instruction image to these names

% First settings
% --------------
Screen('CloseAll');clear all;clear mex;clear functions;close all;home;AssertOpenGL;

% General settings
% ----------------
const.expName           =   'locEMexp';     % experiment name.
const.expStart          =   1;              % Start of a recording exp                          0 = NO  , 1 = YES
const.checkTrial        =   0;              % Print trial conditions (for debugging)            0 = NO  , 1 = YES
const.writeLogTxt       =   0;              % write a log file in addition to eyelink file      0 = NO  , 1 = YES
const.mkVideo           =   0;              % Make a video of a run (on mac not linux)          0 = NO  , 1 = YES

% External controls
% -----------------
const.tracker           =   1;              % run with eye tracker                              0 = NO  , 1 = YES
const.scanner           =   1;              % run in MRI scanner                                0 = NO  , 1 = YES
const.scannerTest       =   0;              % run with T returned at TR time                    0 = NO  , 1 = YES
const.room              =   1;              % run in MRI or eye-tracking room                   1 = MRI , 2 = eye-tracking

% Run order
% ---------
const.cond_run_order = [1;...               % run 01 - Sacc_run01      
                        2;...               % run 02 - Purs_run01      
                        1;...               % run 03 - Sacc_run02      
                        2];                 % run 04 - Purs_run02     

% Run number per condition
% ------------------------
const.cond_run_num   = [01;01;...
                        02;02];

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