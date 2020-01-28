function [const]=constConfig(scr,const)
% ----------------------------------------------------------------------
% [const]=constConfig(scr,const)
% ----------------------------------------------------------------------
% Goal of the function :
% Define all constant configurations
% ----------------------------------------------------------------------
% Input(s) :
% scr : struct containing screen configurations
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Output(s):
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Function created by Martin SZINTE, modified by Vanessa C Morita
% Project :     locEMexp
% Version :     1.0
% ----------------------------------------------------------------------

% Randomization
rng('default');
rng('shuffle');

%% Colors
const.white             =   [255,255,255];                                                      % white color
const.black             =   [0,0,0];                                                            % black color
const.gray              =   [128,128,128];                                                      % gray color
const.red               =   [200,0,0];                                                          % red
const.background_color  =   const.black;                                                        % background color
const.dot_color         =   const.white;                                                        % define fixation dot color

% Fixation circular aperture
const.fix_out_rim_radVal=   0.3;                                                                % radius of outer circle of fixation bull's eye
const.fix_rim_radVal    =   0.75*const.fix_out_rim_radVal;                                      % radius of intermediate circle of fixation bull's eye in degree
const.fix_radVal        =   0.25*const.fix_out_rim_radVal;                                      % radius of inner circle of fixation bull's eye in degrees
const.fix_out_rim_rad   =   vaDeg2pix(const.fix_out_rim_radVal,scr);                            % radius of outer circle of fixation bull's eye in pixels
const.fix_rim_rad       =   vaDeg2pix(const.fix_rim_radVal,scr);                                % radius of intermediate circle of fixation bull's eye in pixels
const.fix_rad           =   vaDeg2pix(const.fix_radVal,scr);                                    % radius of inner circle of fixation bull's eye in pixels


%% Time parameters
const.TR_dur            =   1.2;                                                                % repetition time
const.TR_num            =   (round(const.TR_dur/scr.frame_duration));                           % repetition time in screen frames
const.eyemov_seq        =   [1,2,1,2,1,2,1,2,1,3,3,3,3,1, ...                                   % 1 = blank, 2 = pursuit, 3 = saccade
                             1,2,1,2,1,2,1,2,1,3,3,3,3,1];                                      % - the number of 2's and 3's must be a multiple of length of const.eyemov_ampVal
const.seq_num           =   numel(const.eyemov_seq);                                            % number of sequences per run

const.eyemov_step       =   2;                                                                  % eye movement steps (possible directions)
const.blk_step          =   1;                                                                  % blank period step
const.eyemov_step_dur   =   const.TR_dur;                                                       % eye movement steps in seconds
const.eyemov_step_num   =   (round(const.eyemov_step_dur/scr.frame_duration));                  % eye movement step duration in screen frames
const.blk_step_dur      =   const.TR_dur;                                                       % blank step duration in seconds
const.blk_step_num      =   (round(const.blk_step_dur/scr.frame_duration));                     % blank step duration in screen frames


const.eyemov_ampVal     =   [2.5, 5, 7.5, 10];                                                  % eye movement amplitude in visual degrees
const.eyemov_amp        =   vaDeg2pix(const.eyemov_ampVal,scr);                                 % eye movement amplitude in pixel
const.eyemov_dir_step   =   180;                                                                % eye movement direction steps in degrees
const.eyemov_dir        =   0:const.eyemov_dir_step:360-const.eyemov_dir_step;                  % eye movement direction

const.pursuit_tot_dur   =   1.000;                                                              % eye movement total duration in seconds
const.pursuit_tot_num   =   (round(const.pursuit_tot_dur/scr.frame_duration));                  % eye movement total duration in screen frames
const.pursuit_ramp_dur  =   0.100;                                                              % eye movement ramp duration in seconds
const.pursuit_ramp_num  =   (round(const.pursuit_ramp_dur/scr.frame_duration));                 % eye movement ramp duration in screen frames
const.pursuit_dur       =   const.pursuit_tot_dur - const.pursuit_ramp_dur;                     % eye movement duration after ramp
const.pursuit_speed_pps =   const.eyemov_amp/const.pursuit_dur;                                 % eye movement speed in pixel per second
const.pursuit_speed_ppf =   const.pursuit_speed_pps/scr.hz;                                     % eye movement speed in degree per screen frame

const.saccade_tot_dur   =   0.400;                                                              % eye movement total duration in seconds
const.saccade_tot_num   =   (round(const.saccade_tot_dur/scr.frame_duration));                  % eye movement total duration in screen frames
const.saccade_fix_dur   =   0.300;                                                              % eye movement first fixation duration in seconds
const.saccade_fix_num   =   (round(const.saccade_fix_dur/scr.frame_duration));                  % eye movement first fixation duration in screen frames

const.end_dur           =   0.200;                                                              % return saccade duration in seconds
const.end_num           =   (round(const.end_dur/scr.frame_duration));                          % return saccade duration in screen frames

const.pursuit_trial_dur =   const.pursuit_tot_dur + const.end_dur;                              % trial duration in seconds
const.pursuit_trial_num =   (round(const.pursuit_trial_dur/scr.frame_duration));                % trial duration in screen frames
const.saccade_trial_dur =   const.saccade_fix_dur + const.saccade_tot_dur + const.end_dur;      % trial duration in seconds
const.saccade_trial_num =   (round(const.saccade_trial_dur/scr.frame_duration));                % trial duration in screen frames
const.saccade_trial_rep =   floor(const.TR_dur/const.saccade_trial_dur);                        % trial repetitions : calculates how many saccades fit within a TR; if don't want to repeate, change to 1

% define TR for scanner
if const.scanner
    const.TRs = 0;
    for seq = const.eyemov_seq
        if seq == 1
            TR_seq = const.blk_step;
        else
            TR_seq = const.eyemov_step;
        end
        const.TRs = const.TRs + TR_seq;
    end
    const.TRs = const.TRs;
    fprintf(1,'\n\tScanner parameters; %1.0f TRs, %1.2f seconds, %s\n',const.TRs,const.TR_dur,datestr(seconds((const.TRs*const.TR_dur)),'MM:SS'));
end

% compute pursuit coordinates
for pursuit_amp = 1:size(const.eyemov_amp,2)
    pix_ramp = (const.pursuit_ramp_num-1)*const.pursuit_speed_ppf(pursuit_amp);
    pix_step = const.pursuit_speed_ppf(pursuit_amp);
    for pursuit_dir = 1:size(const.eyemov_dir,2)
        for nbf = 1:const.pursuit_tot_num
            if nbf == 1
                % eye movement ramp
                const.pursuit_matX(nbf,pursuit_amp,pursuit_dir) = scr.x_mid + (cosd(const.eyemov_dir(pursuit_dir)-180) * pix_ramp);
                const.pursuit_matY(nbf,pursuit_amp,pursuit_dir) = scr.y_mid + (-sind(const.eyemov_dir(pursuit_dir)-180) * pix_ramp);
            else
                % eye movement step
                const.pursuit_matX(nbf,pursuit_amp,pursuit_dir) = const.pursuit_matX(nbf-1,pursuit_amp,pursuit_dir) + (cosd(const.eyemov_dir(pursuit_dir)) * pix_step);
                const.pursuit_matY(nbf,pursuit_amp,pursuit_dir) = const.pursuit_matY(nbf-1,pursuit_amp,pursuit_dir) + (-sind(const.eyemov_dir(pursuit_dir)) * pix_step);
            end
        end
    end
end

% compute saccade coordinates
step1 = 1:const.saccade_fix_num;                                    % fixation
step2 = (step1(end) + 1):(step1(end) + const.saccade_tot_num);      % saccade
step3 = (step2(end) + 1):(step2(end) + const.end_num);              % return saccade
total = numel(step1) + numel(step2) + numel(step3);

for saccade_amp = 1:size(const.eyemov_amp,2)
    for saccade_dir = 1:size(const.eyemov_dir,2)
        for k = 1:const.saccade_trial_rep
            const.saccade_matX(total*(k-1)+step1,saccade_amp,saccade_dir) = scr.x_mid;
            const.saccade_matY(total*(k-1)+step1,saccade_amp,saccade_dir) = scr.y_mid;

            const.saccade_matX(total*(k-1)+step2,saccade_amp,saccade_dir) = scr.x_mid + (cosd(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));
            const.saccade_matY(total*(k-1)+step2,saccade_amp,saccade_dir) = scr.y_mid + (-sind(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp)); 
            
            const.saccade_matX(total*(k-1)+step3,saccade_amp,saccade_dir) = scr.x_mid;  % change the signal to have a blank screen for return saccade instead of a fixation target
            const.saccade_matY(total*(k-1)+step3,saccade_amp,saccade_dir) = scr.y_mid;  % change the signal to have a blank screen for return saccade instead of a fixation target
        end
    end
end

%% Eyelink calibration value
const.ppd               =   vaDeg2pix(1,scr);                                                  % get one pixel per degree
const.maxX              =   scr.scr_sizeX*0.5;                                                 % maximum horizontal amplitude of the screen
const.maxY              =   scr.scr_sizeY*0.5;                                                 % maximum vertical amplitude of the screen
const.calib_maxX     	=   const.maxX/2;
const.calib_maxY        =   const.maxY/2;
const.calib_center      =   [scr.scr_sizeX/2,scr.scr_sizeY/2];

const.calibCoord        =   round([ const.calib_center(1),                     const.calib_center(2),...                       % 01.  center center
                                    const.calib_center(1),                     const.calib_center(2)-const.calib_maxY,...      % 02.  center up
                                    const.calib_center(1),                     const.calib_center(2)+const.calib_maxY,...      % 03.  center down
                                    const.calib_center(1)-const.calib_maxX,    const.calib_center(2),....                      % 04.  left center
                                    const.calib_center(1)+const.calib_maxX,    const.calib_center(2),...                       % 05.  right center
                                    const.calib_center(1)-const.calib_maxX,    const.calib_center(2)-const.calib_maxY,....     % 06.  left up
                                    const.calib_center(1)+const.calib_maxX,    const.calib_center(2)-const.calib_maxY,...      % 07.  right up
                                    const.calib_center(1)-const.calib_maxX,    const.calib_center(2)+const.calib_maxY,....     % 08.  left down
                                    const.calib_center(1)+const.calib_maxX,    const.calib_center(2)+const.calib_maxY,...      % 09.  right down
                                    const.calib_center(1)-const.calib_maxX/2,  const.calib_center(2)-const.calib_maxY/2,....   % 10.  mid left mid up
                                    const.calib_center(1)+const.calib_maxX/2,  const.calib_center(2)-const.calib_maxY/2,....   % 11.  mid right mid up
                                    const.calib_center(1)-const.calib_maxX/2,  const.calib_center(2)+const.calib_maxY/2,....   % 12.  mid left mid down
                                    const.calib_center(1)+const.calib_maxX/2,  const.calib_center(2)+const.calib_maxY/2]);     % 13.  mid right mid down

const.valid_maxX        =   const.calib_maxX * 0.9;
const.valid_maxY        =   const.calib_maxY * 0.9;
const.valid_center      =   const.calib_center;

const.validCoord    	=   round([ const.valid_center(1),                     const.valid_center(2),...                       % 01.  center center
                                    const.valid_center(1),                     const.valid_center(2)-const.valid_maxY,...      % 02.  center up
                                    const.valid_center(1),                     const.valid_center(2)+const.valid_maxY,...      % 03.  center down
                                    const.valid_center(1)-const.valid_maxX,    const.valid_center(2),....                      % 04.  left center
                                    const.valid_center(1)+const.valid_maxX,    const.valid_center(2),...                       % 05.  right center
                                    const.valid_center(1)-const.valid_maxX,    const.valid_center(2)-const.valid_maxY,....     % 06.  left up
                                    const.valid_center(1)+const.valid_maxX,    const.valid_center(2)-const.valid_maxY,...      % 07.  right up
                                    const.valid_center(1)-const.valid_maxX,    const.valid_center(2)+const.valid_maxY,....     % 08.  left down
                                    const.valid_center(1)+const.valid_maxX,    const.valid_center(2)+const.valid_maxY,...      % 09.  right down
                                    const.valid_center(1)-const.valid_maxX/2,  const.valid_center(2)-const.valid_maxY/2,....   % 10.  mid left mid up
                                    const.valid_center(1)+const.valid_maxX/2,  const.valid_center(2)-const.valid_maxY/2,....   % 11.  mid right mid up
                                    const.valid_center(1)-const.valid_maxX/2,  const.valid_center(2)+const.valid_maxY/2,....   % 12.  mid left mid down
                                    const.valid_center(1)+const.valid_maxX/2,  const.valid_center(2)+const.valid_maxY/2]);     % 13.  mid right mid down

end