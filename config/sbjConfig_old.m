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
% Project :     Localisers
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
    const.cond1             =   input(sprintf('\nChoose the task:\n\tSaccade X Pursuit (1), \n\tVisually guided X Endogenous (2), \n\tInhibition & Sequence (3) : \n'));
    while ~(const.cond1 == 1 || const.cond1 == 2 || const.cond1 == 3)
        sprintf('Error: Type either (1), (2) or (3)');
        const.cond1         =   input(sprintf('\nChoose the task:\n\tSaccade X Pursuit (1), \n\tVisually guided X Endogenous (2), \n\tInhibition & Sequence (3) : \n'));
    end
    
    if const.cond1 == 1
        const.cond2         =   input(sprintf('\nChoose the size of the trajectory :\n\t10 degrees (1), \n\t5 degrees (2), \n\t2.5 degrees (3) : \n'));
        while ~(const.cond2 == 1 || const.cond2 == 2 || const.cond2 == 3)
            sprintf('Error: Type either (1), (2) or (3)');
            const.cond2     =   input(sprintf('\nChoose the size of the trajectory :\n\t10 degrees (1), \n\t5 degrees (2), \n\t2.5 degrees (3) : \n'));
        end
        const.cond3         =   '';
        
    elseif const.cond1 == 2
        const.cond2         =   input(sprintf('\nChoose the direction of the trajectory :\n\tClockwise (1), \n\tCounter-clockwise (2) : \n'));
        while ~(const.cond2 == 1 || const.cond2 == 2)
            sprintf('Error: Type either (1) or (2)');
            const.cond2     =   input(sprintf('\nChoose the direction of the trajectory :\n\tClockwise (1), \n\tCounter-clockwise (2) : \n'));
        end
        
        const.cond3         =   input(sprintf('\nChoose the size of the occlusion :\n\t10 degrees (1), \n\t5 degrees (2), \n\t3 degrees (3) : \n'));
        while ~(const.cond3 == 1 || const.cond3 == 2 || const.cond3 == 3)
            sprintf('Error: Type either (1), (2) or (3)');
            const.cond3     =   input(sprintf('\nChoose the size of the occlusion :\n\t10 degrees (1), \n\t5 degrees (2), \n\t3 degrees (3) : \n'));
        end
        
    elseif const.cond1 == 3
        const.cond2         =   input(sprintf('\nChoose the size of the trajectory :\n\t15 degrees (1), \n\t10 degrees (2), \n\t5 degrees (3) : \n'));
        while ~(const.cond2 == 1 || const.cond2 == 2 || const.cond2 == 3)
            sprintf('Error: Type either (1) or (2)');
            const.cond2     =   input(sprintf('\nChoose the size of the trajectory :\n\t15 degrees (1), \n\t10 degrees (2), \n\t5 degrees (3) : \n'));
        end
        
        const.cond3         =   input(sprintf('\nChoose the size of the sequence (between 1 and 5)  : \n'));
        while ~(const.cond3 >= 1 && const.cond3 <= 5)
            sprintf('Error: Type a number between 1 and 5');
            const.cond3     =   input(sprintf('\nChoose the size of the sequence (between 1 and 5)  : \n'));
        end
    end
    
    
    
else
    % define order of tasks for the real experiment
    % TO-DO
    %     const.cond1         =   const.cond_run_order(const.runNum,1);
    %     const.cond2         =   const.cond_run_order(const.runNum,2);
end

switch const.cond1
    case 1
        const.cond1_txt =  'SaccPurs';
        switch const.cond2
            case 1
                const.cond2_txt =  '_10deg';
            case 2
                const.cond2_txt =  '_5deg';
            case 3
                const.cond2_txt =  '_2-5deg';
            otherwise
                const.cond2_txt =  '';
        end
        const.cond3_txt =  '';
        
    case 2
        const.cond1_txt =  'VisuEndo';
        switch const.cond2
            case 1
                const.cond2_txt =  '_Cw';
            case 2
                const.cond2_txt =  '_CCW';
            otherwise
                const.cond2_txt =  '';
        end
        switch const.cond3
            case 1
                const.cond3_txt =  '_Occl10deg';
            case 2
                const.cond3_txt =  '_Occl5deg';
            case 3
                const.cond3_txt =  '_Occl3deg'; % TO-DO define size of occlusion
            otherwise
                const.cond3_txt =  '';
        end
        
    case 3
        const.cond1_txt =  'InhiSequ';
        switch const.cond2
            case 1
                const.cond2_txt =  '_15deg';
            case 2
                const.cond2_txt =  '_10deg';
            case 3
                const.cond2_txt =  '_5deg';
            otherwise
                const.cond2_txt =  '';
        end
        const.cond3_txt =  ['_Seq', num2str(const.cond3)];
        
    otherwise
        const.cond1_txt =  '';
end

fprintf(1,'\n\tTask: %s%s%s\n', const.cond1_txt, const.cond2_txt, const.cond3_txt);

if const.expStart
    if const.tracker
        const.sjct_DomEye   =   'L';  % for all subjects
        const.recEye        =   1;
    else
        const.sjct_DomEye   =   'DM';
        const.recEye        =   1;
    end
    if const.runNum == 1
        const.sjctName      =   upper(strtrim(input(sprintf('\n\tParticipant identity: '),'s')));
        const.sjct_age      =   input(sprintf('\n\tParticipant age: '));
        if isempty(const.sjct_age)
            error('Incorrect participant age');
        end
        const.sjct_gender   =   upper(strtrim(input(sprintf('\n\tParticipant gender (M or F): '),'s')));
    end
else
    const.sjct          =   'sub-00X';
    const.sjct_age      =   '00';
    const.sjct_gender   =   'X';
    const.sjct_DomEye   =   'DM';
    const.recEye        =   1;
end

end