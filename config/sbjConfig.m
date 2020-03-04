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

const.runNum            =   input(sprintf('\n\tRun number (1 to %d): ',length(const.cond_run_order)));
if isempty(const.runNum)
    error('Incorrect run number');
end
if const.runNum > length(const.cond_run_order)
    error('Cannot run more than %d runs',length(const.cond_run_order));
end

const.cond1_txt          =  'Loc';
const.cond2_txt          =  '';

if const.expStart == 0
    const.cond1         =   1;
    const.cond2         =   input(sprintf('\n\tSaccade (1), Pursuit (2) : '));
    if const.cond2 == 1, const.cond2_txt =  'Sacc';
    else const.cond2_txt =  'Purs'; end
else
    const.cond1     =   1;    
    
    if mod(const.sjctNum,2) == 1 % if subj number is odd, starts with pursuit
        const.cond_run_order = circshift(const.cond_run_order,1);
    end
    
    const.cond2     =   const.cond_run_order(const.runNum);
    if const.cond2 == 1 
        const.cond2_txt 	=  'Sacc';
    elseif const.cond2 == 2
        const.cond2_txt 	=  'Purs';
    end
end

fprintf(1,'\n\tTask: %s%s\n',const.cond1_txt,const.cond2_txt);

const.recEye        =   1;
if ~const.expStart
    const.sjctNum       =   99;
    const.sjct          =   'sub-0X';
end

end