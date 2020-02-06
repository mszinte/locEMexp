function [expDes]=designConfig(const)
% ----------------------------------------------------------------------
% [expDes]=designConfig(const)
% ----------------------------------------------------------------------
% Goal of the function :
% Define experimental design
% ----------------------------------------------------------------------
% Input(s) :
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Output(s):
% expDes : struct containg experimental design
% ----------------------------------------------------------------------
% Function created by Martin SZINTE, modified by Vanessa C Morita
% Project :     locEMexp
% Version :     1.0
% ----------------------------------------------------------------------

%% Experimental random variables

% Cond 1 : task (1 modality)
% =======
expDes.oneC             =   1;
expDes.txt_cond1        =   {'eyemov'};
% 01 = eye movement


% Var 1 : trial types (3 modalities)
% ======
expDes.oneV             =   [1;2;3];
expDes.txt_var1         =   {'pursuit','saccade','fixation'};
% 01 = smooth pursuit
% 02 = saccade
% 03 = fixation

% Var 2 : eye movement amplitude (5 modalities)
% ======
expDes.twoV             =   [1;2;3;4;5];
expDes.txt_var2         =   {'2.5 dva','5 dva','7.5 dva','10 dva','none'};
% 01 = 4 dva
% 02 = 6 dva
% 03 = 8 dva
% 04 = 10 dva
% 05 = none

% Var 3 : eye movement direction (3 modalities)
% ======
expDes.threeV           =   [01;02;03];
expDes.txt_var3         =   {'0 deg','180 deg','none'};
% 01 =   0.0 deg    
% 02 = 180.0 deg

% seq order
% ---------
if const.runNum == 1
    % create sequence order
    amp_sequence.eyemov_val = expDes.twoV(randperm(numel(expDes.twoV)-1));
    
    amp_sequence.val                        =     nan(size(const.eyemov_seq));
    amp_sequence.val(const.eyemov_seq==1)   =     numel(expDes.twoV);
    
    ampseq_rep  =    numel(const.eyemov_seq(const.eyemov_seq == 2))/numel(const.eyemov_ampVal);
    eyemov_rep  =    repmat(amp_sequence.eyemov_val,ampseq_rep,1);
    
    amp_sequence.val(const.eyemov_seq==2)   =     eyemov_rep;
    amp_sequence.val(const.eyemov_seq==3)   =     eyemov_rep;
    
    expDes.amp_sequence   =   amp_sequence.val;
    save(const.amp_sequence_file,'amp_sequence');
else
    load(const.amp_sequence_file);
    expDes.amp_sequence   =   amp_sequence.val;
end
%% Experimental configuration :
expDes.nb_cond          =   1;
expDes.nb_var           =   3;
expDes.nb_rand          =   0;
expDes.nb_list          =   0;

%% Experimental loop
rng('default');rng('shuffle');
runT                    =   const.runNum;

t_trial = 0;
for t_seq = 1:size(const.eyemov_seq,2)
    
    cond1 = const.cond1;
    rand_var2 =   expDes.amp_sequence(t_seq);
    
    if rand_var2 == 5
        seq_steps = const.blk_step;
    else
        seq_steps = const.eyemov_step;
    end
    
    for seq_step = 1:seq_steps
        if rand_var2 == 5
            rand_var1 = expDes.oneV(end);
            rand_var3 = expDes.threeV(end);
        else
            if const.eyemov_seq(t_seq) == 2
                rand_var1 = 1;
            elseif const.eyemov_seq(t_seq) == 3
                rand_var1 = 2;
            end
            rand_var3 = expDes.threeV(seq_step);
        end
    
        t_trial     =   t_trial + 1;
        
        expDes.expMat(t_trial,:)=   [   runT,           t_trial,        cond1,          rand_var1,      rand_var2,  ...
                                        rand_var3,      t_seq,          seq_step,       NaN,            NaN];
        % col 01:   Run number
        % col 02:   Trial number
        % col 03:   Task
        % col 04:   Eye mov type
        % col 05:   Eye mov amplitude
        % col 06:   Eye mov direction
        % col 07:   Sequence number
        % col 08:   Sequence trial (trial number within a sequence of one mov type)
        % col 09:   Trial onset time
        % col 10:   Trial offset time
    end
end
expDes.nb_trials = size(expDes.expMat,1);

end