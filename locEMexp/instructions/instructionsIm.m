function instructionsIm(scr,const,my_key,nameImage,exitFlag)
% ----------------------------------------------------------------------
% instructionsIm(scr,const,my_key,nameImage,exitFlag)
% ----------------------------------------------------------------------
% Goal of the function :
% Display instructions draw in .tif file.
% ----------------------------------------------------------------------
% Input(s) :
% scr : main window pointer.
% const : struct containing all the constant configurations.
% nameImage : name of the file image to display
% exitFlag : if = 1 (quit after 5sec)
% ----------------------------------------------------------------------
% Output(s):
% (none)
% ----------------------------------------------------------------------
% Function created by Martin SZINTE (martin.szinte@gmail.com)
% Project :     locEMexp
% Version :     3.0
% ----------------------------------------------------------------------

dirImageFile            =   'instructions/image/';
dirImage                =   [dirImageFile,nameImage,'.png'];
[imageToDraw,~,alpha]   =   imread(dirImage);
imageToDraw(:,:,4)      =   alpha;

t_handle                =   Screen('MakeTexture',scr.main,imageToDraw);
texrect                 =   Screen('Rect', t_handle);
push_button             =   0;


Screen('FillRect',scr.main,const.background_color);
Screen('DrawTexture',scr.main,t_handle,texrect,[0,0,scr.scr_sizeX,scr.scr_sizeY]);
Screen('Flip',scr.main);

t0                      =   GetSecs;
tEnd                    =   3;

while ~push_button    
    t1 = GetSecs;
    if exitFlag
        if t1 - t0 > tEnd
            push_button             =   1;
        end
    end
    
    keyPressed              =   0;
    keyCode                 =   zeros(1,my_key.keyCodeNum);
    
    for keyb = 1:size(my_key.keyboard_idx,2)
        [keyP, keyC]            =   KbQueueCheck(my_key.keyboard_idx(keyb));
        keyPressed              =   keyPressed+keyP;
        keyCode                 =   keyCode+keyC;
    end
    
    if const.room == 1
        input_return = my_key.ni_session.inputSingleScan;
        if input_return(my_key.idx_button_right1) == my_key.button_press_val
            keyPressed              = 1;
            keyCode(my_key.right1)  = 1;
        end
    end
    
    % main keyboard check
    if keyPressed
        if keyCode(my_key.space) || keyCode(my_key.right1)
            push_button             =   1;
        elseif keyCode(my_key.escape)
            overDone(const,my_key)
        end
    end
end

Screen('Close',t_handle);
end