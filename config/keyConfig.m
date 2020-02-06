function [my_key]=keyConfig(const)
% ----------------------------------------------------------------------
% [my_key]=keyConfig(const)
% ----------------------------------------------------------------------
% Goal of the function :
% Unify key names and define structure containing each key names
% ----------------------------------------------------------------------
% Input(s) :
% const : struct containing constant configurations
% ----------------------------------------------------------------------
% Output(s):
% my_key : structure containing keyboard configurations
% ----------------------------------------------------------------------
% Function created by Martin SZINTE (martin.szinte@gmail.com)
% Last update : 17 / 01 / 2020
% Project :     locEMexp
% Version :     1.0
% ----------------------------------------------------------------------

KbName('UnifyKeyNames');

my_key.mri_trVal        =   't';                    % mri trigger letter
my_key.left1Val         =   'a';                    % left button 1 (Leftmost->Rightmost)
my_key.left2Val         =   'z';                    % left button 2 (Leftmost->Rightmost)
my_key.left3Val         =   'e';                    % left button 3 (Leftmost->Rightmost)
my_key.left4Val         =   'r';                    % left button 4 (Leftmost->Rightmost)
my_key.right1Val        =   'u';                    % right button 1 (Leftmost->Rightmost)
my_key.right2Val        =   'i';                    % right button 2 (Leftmost->Rightmost)
my_key.right3Val        =   'o';                    % right button 3 (Leftmost->Rightmost)
my_key.right4Val        =   'p';                    % right button 4 (Leftmost->Rightmost)
my_key.escapeVal        =   'escape';               % escape button
my_key.spaceVal         =   'space';                % space button

my_key.mri_tr           =   KbName(my_key.mri_trVal);
my_key.left1            =   KbName(my_key.left1Val);
my_key.left2            =   KbName(my_key.left2Val);
my_key.left3            =   KbName(my_key.left3Val);
my_key.left4            =   KbName(my_key.left4Val);
my_key.right1           =   KbName(my_key.right1Val);
my_key.right2           =   KbName(my_key.right2Val);
my_key.right3           =   KbName(my_key.right3Val);
my_key.right4           =   KbName(my_key.right4Val);
my_key.escape           =   KbName(my_key.escapeVal);
my_key.space            =   KbName(my_key.spaceVal);

my_key.keyboard_idx     =   GetKeyboardIndices;
for keyb = 1:size(my_key.keyboard_idx,2)
    KbQueueCreate(my_key.keyboard_idx(keyb));
    KbQueueFlush(my_key.keyboard_idx(keyb));
    KbQueueStart(my_key.keyboard_idx(keyb));
end

[~,keyCodeMat]   = KbQueueCheck(my_key.keyboard_idx(1));
my_key.keyCodeNum  = numel(keyCodeMat);

if const.room == 1
    
    % NI board acquisition settings
    warning off;
    daq.reset;
    my_key.ni_devices = daq.getDevices;
    my_key.ni_session = daq.createSession(my_key.ni_devices.Vendor.ID);
    my_key.ni_device_ID = 'Dev2';
    my_key.ni_measurement_type = 'InputOnly';
    my_key.button_press_val = 1;
    
    % button press settings
    my_key.port_button_left1    = [];                   my_key.idx_button_left1     = [];
    my_key.port_button_left2    = [];                   my_key.idx_button_left2     = [];
    my_key.port_button_left3    = [];                   my_key.idx_button_left3     = [];
    my_key.port_button_left4    = 'port0/line0';        my_key.idx_button_left4     = 1;
    
    if ~isempty(my_key.port_button_left1); my_key.channel_button_left1 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_left1,my_key.ni_measurement_type); end
    if ~isempty(my_key.port_button_left2); my_key.channel_button_left2 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_left2,my_key.ni_measurement_type); end    
    if ~isempty(my_key.port_button_left3); my_key.channel_button_left2 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_left3,my_key.ni_measurement_type); end
    if ~isempty(my_key.port_button_left4); my_key.channel_button_left4 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_left4,my_key.ni_measurement_type); end
    
    my_key.port_button_right1    = 'port0/line1';       my_key.idx_button_right1     =  2;
    my_key.port_button_right2    = [];                  my_key.idx_button_right2     =  [];
    my_key.port_button_right3    = [];                  my_key.idx_button_right3     =  [];
    my_key.port_button_right4    = [];                  my_key.idx_button_right4     =  [];
    
    if ~isempty(my_key.port_button_right1); my_key.channel_button_right1 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_right1,my_key.ni_measurement_type); end
    if ~isempty(my_key.port_button_right2); my_key.channel_button_right2 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_right2,my_key.ni_measurement_type); end
    if ~isempty(my_key.port_button_right3); my_key.channel_button_right3 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_right3,my_key.ni_measurement_type); end
    if ~isempty(my_key.port_button_right4); my_key.channel_button_right4 = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_button_right4,my_key.ni_measurement_type); end
    
    % MRI trigger settings
    fprintf(1,'\n\n\tDon''t forget to put MRI trigger in "Toggle" mode\n');
    my_key.port_mri_bands       = 'port1/line0';
    my_key.idx_mri_bands        = 3;
    
    if ~isempty(my_key.port_mri_bands); my_key.channel_mri_bands = my_key.ni_session.addDigitalChannel(my_key.ni_device_ID,my_key.port_mri_bands,my_key.ni_measurement_type);  end
    
    % first reading execution
    my_key.first_val = my_key.ni_session.inputSingleScan;
else
    my_key.first_val = [0, 0, 0];
end
    

end