function [const]=sbjConfig(const)
% ----------------------------------------------------------------------
% [const]=sbjConfig(const)
% ----------------------------------------------------------------------
% Goal of the function :
% Define subject configurations (initials, gender...)
% ----------------------------------------------------------------------
% Input(s) :
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Output(s):
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Function created by Martin SZINTE, modified by Vanessa C Morita
% Project :     locEMexp
% Version :     1.0
% ----------------------------------------------------------------------

if const.expStart
    const.sjctNum           =  input(sprintf('\n\tParticipant number: '));
    if isempty(const.sjctNum)
        error('Incorrect participant number');
    end
    if const.sjctNum > 9
        const.sjct          =  sprintf('sub-%i',const.sjctNum);
    else
        const.sjct          =  sprintf('sub-0%i',const.sjctNum);
    end
end

const.runNum            =   input(sprintf('\n\tRun number (1 to 10): '));
if isempty(const.runNum)
    error('Incorrect run number');
end
if const.runNum > 10
    error('Cannot run more than 10 runs');
end

if const.expStart == 0
    const.cond1         =   1;
else
    const.cond1         =   const.cond_run_order(const.runNum,1);
end
const.cond1_txt          =  'SaccPursFix';

fprintf(1,'\n\tTask: %s\n',const.cond1_txt);

const.recEye        =   1;
if ~const.expStart
    const.sjct          =   'sub-0X';
    const.recEye        =   1;
end

end