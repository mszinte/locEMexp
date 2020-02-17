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

const.eyemov_seq        =   [1,2,1,2,1,2,1,2,1];                                                % 1 = blank/fixation, 2 = eye movement (pursuit or saccade, depending on the run)
const.seq_num           =   numel(const.eyemov_seq);                                            % number of sequences per run

const.eyemov_step       =   32;                                                                 % eye movement steps (possible directions)
const.fix_step          =   16;                                                                 % fixation period step
const.eyemov_step_dur   =   const.TR_dur;                                                       % eye movement steps in seconds
const.eyemov_step_num   =   (round(const.eyemov_step_dur/scr.frame_duration));                  % eye movement step duration in screen frames
const.fix_step_dur      =   const.TR_dur;                                                       % fixation step duration in seconds
const.fix_step_num      =   (round(const.fix_step_dur/scr.frame_duration));                     % fixation step duration in screen frames


const.eyemov_ampVal     =   [2.5, 5, 7.5, 10];                                                  % eye movement amplitude in visual degrees
const.eyemov_amp        =   vaDeg2pix(const.eyemov_ampVal,scr);                                 % eye movement amplitude in pixel
const.eyemov_dir_step   =   22.5;                                                               % eye movement direction steps in degrees
const.eyemov_dir        =   0:const.eyemov_dir_step:360-const.eyemov_dir_step;                  % eye movement direction

const.pursuit_fix_dur   =   0.100;                                                              % first fixation duration in seconds
const.pursuit_fix_num   =   (round(const.pursuit_fix_dur/scr.frame_duration));                  % first fixation duration in screen frames
const.pursuit_dur       =   1.000;                                                              % eye movement total duration in seconds
const.pursuit_num       =   (round(const.pursuit_dur/scr.frame_duration));                      % eye movement total duration in screen frames
const.pursuit_speed_pps =   const.eyemov_amp/const.pursuit_dur;                                 % eye movement speed in pixel per second
const.pursuit_speed_ppf =   const.pursuit_speed_pps/scr.hz;                                     % eye movement speed in degree per screen frame
const.pursuit_end_dur   =   0.100;                                                              % return saccade duration in seconds
const.pursuit_end_num   =   (round(const.pursuit_end_dur/scr.frame_duration));                  % return saccade duration in screen frames

const.saccade_fix_dur   =   0.100;                                                              % first fixation duration in seconds
const.saccade_fix_num   =   (round(const.saccade_fix_dur/scr.frame_duration));                  % first fixation duration in screen frames
const.saccades_num      =   2;                                                                  % number of saccades per TR
if const.saccades_num == 1
    const.saccade_tot_dur   =   1.100;                                                          % eye movement total duration in seconds
elseif const.saccades_num == 2
    const.saccade_tot_dur   =   0.500;                                                          % eye movement total duration in seconds
end
const.saccade_tot_num   =   (round(const.saccade_tot_dur/scr.frame_duration));                  % eye movement total duration in screen frames

% define TR for scanner
if const.scanner
    const.TRs = 0;
    for seq = const.eyemov_seq
        if seq == 1
            TR_seq = const.fix_step;
        else
            TR_seq = const.eyemov_step;
        end
        const.TRs = const.TRs + TR_seq;
    end
    const.TRs = const.TRs;
    fprintf(1,'\n\tScanner parameters; %1.0f TRs, %1.2f seconds, %s\n',const.TRs,const.TR_dur,datestr(seconds((const.TRs*const.TR_dur)),'MM:SS'));
end

% compute pursuit coordinates
% 1 TR = 1 pursuit mov
for pursuit_amp = 1:size(const.eyemov_amp,2)
    pix_step = const.pursuit_speed_ppf(pursuit_amp);
    for pursuit_dir = 1:size(const.eyemov_dir,2)  
        idx1 = (pursuit_dir-1)*2 + 1;
        idx2 = (pursuit_dir-1)*2 + 2;
        % center -> perifery
        % fixation
        step1 = 1:const.pursuit_fix_num;
        const.pursuit_matX(step1,pursuit_amp,idx1) = scr.x_mid;
        const.pursuit_matY(step1,pursuit_amp,idx1) = scr.y_mid;
        
        % eye movement step
        step2 = (step1(end) + 1):(step1(end) + const.pursuit_num);
        for nbf = step2
            const.pursuit_matX(nbf,pursuit_amp,idx1) = const.pursuit_matX(nbf-1,pursuit_amp,idx1) + (cosd(const.eyemov_dir(pursuit_dir)) * pix_step);
            const.pursuit_matY(nbf,pursuit_amp,idx1) = const.pursuit_matY(nbf-1,pursuit_amp,idx1) + (-sind(const.eyemov_dir(pursuit_dir)) * pix_step);
        end
        
        % fixation
        step3 = (step2(end) + 1):(step2(end) + const.pursuit_end_num);
        for nbf = step3
            const.pursuit_matX(nbf,pursuit_amp,idx1) = const.pursuit_matX(nbf-1,pursuit_amp,idx1);
            const.pursuit_matY(nbf,pursuit_amp,idx1) = const.pursuit_matY(nbf-1,pursuit_amp,idx1);
        end
        
        % perifery -> center
        const.pursuit_matX(:,pursuit_amp,idx2) = flip(const.pursuit_matX(:,pursuit_amp,idx1));
        const.pursuit_matY(:,pursuit_amp,idx2) = flip(const.pursuit_matY(:,pursuit_amp,idx1));
    end
end

% compute saccade coordinates
if const.saccades_num == 2 % 1 TR = 2 saccades
    step1 = 1:const.saccade_fix_num;                                    % fixation on center
    step2 = (step1(end) + 1):(step1(end) + const.saccade_tot_num);      % saccade to perifery
    step3 = step2(end) + step1;                                         % fixation on perifery
    step4 = step2(end) + step2;                                         % saccade to center

    for saccade_amp = 1:size(const.eyemov_amp,2)
        for saccade_dir = 1:size(const.eyemov_dir,2)            
            const.saccade_matX(step1,saccade_amp,saccade_dir) = scr.x_mid;
            const.saccade_matY(step1,saccade_amp,saccade_dir) = scr.y_mid;

            const.saccade_matX(step2,saccade_amp,saccade_dir) = scr.x_mid + (cosd(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));
            const.saccade_matY(step2,saccade_amp,saccade_dir) = scr.y_mid + (-sind(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));

            const.saccade_matX(step3,saccade_amp,saccade_dir) = scr.x_mid + (cosd(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));
            const.saccade_matY(step3,saccade_amp,saccade_dir) = scr.y_mid + (-sind(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));

            const.saccade_matX(step4,saccade_amp,saccade_dir) = scr.x_mid;
            const.saccade_matY(step4,saccade_amp,saccade_dir) = scr.y_mid;        
        end
        const.saccade_matX(:,saccade_amp,17:32) = const.saccade_matX(:,saccade_amp,1:16);
        const.saccade_matY(:,saccade_amp,17:32) = const.saccade_matY(:,saccade_amp,1:16);
    end
    
    
elseif const.saccades_num == 1 % 1 TR = 1 saccade
    step1 = 1:const.saccade_fix_num;                                    % fixation on center
    step2 = (step1(end) + 1):(step1(end) + const.saccade_tot_num);      % saccade to perifery
   
    for saccade_amp = 1:size(const.eyemov_amp,2)
        for saccade_dir = 1:size(const.eyemov_dir,2)
            idx1 = (saccade_dir-1)*2 + 1;
            idx2 = (saccade_dir-1)*2 + 2;
            
            const.saccade_matX(step1,saccade_amp,idx1) = scr.x_mid;
            const.saccade_matY(step1,saccade_amp,idx1) = scr.y_mid;

            const.saccade_matX(step2,saccade_amp,idx1) = scr.x_mid + (cosd(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));
            const.saccade_matY(step2,saccade_amp,idx1) = scr.y_mid + (-sind(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));

            const.saccade_matX(step1,saccade_amp,idx2) = scr.x_mid + (cosd(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));
            const.saccade_matY(step1,saccade_amp,idx2) = scr.y_mid + (-sind(const.eyemov_dir(saccade_dir)) * const.eyemov_amp(saccade_amp));

            const.saccade_matX(step2,saccade_amp,idx2) = scr.x_mid;
            const.saccade_matY(step2,saccade_amp,idx2) = scr.y_mid;        
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