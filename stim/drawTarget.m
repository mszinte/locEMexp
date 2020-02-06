function drawTarget(scr,const,targetX,targetY)
% ----------------------------------------------------------------------
% drawTarget(scr,const,targetX,targetY)
% ----------------------------------------------------------------------
% Goal of the function :
% Draw bull's eye target
% ----------------------------------------------------------------------
% Input(s) :
% scr : struct containing screen configurations
% const : struct containing constant configurations
% targetX: target coordinate X
% targetY: target coordinate Y
% typeTarget: (1) in dot (2) bull's eye
% ----------------------------------------------------------------------
% Output(s):
% none
% ----------------------------------------------------------------------
% Function created by Martin SZINTE (martin.szinte@gmail.com)
% Last update : 20 / 01 / 2020
% Project :     pMFexp
% Version :     1.0
% ----------------------------------------------------------------------


Screen('DrawDots',scr.main,[targetX,targetY],const.fix_out_rim_rad*2, const.dot_color , [], 2);
Screen('DrawDots',scr.main,[targetX,targetY],const.fix_rim_rad*2, const.background_color, [], 2);
Screen('DrawDots',scr.main,[targetX,targetY],const.fix_rad*2, const.dot_color , [], 2);
    

end