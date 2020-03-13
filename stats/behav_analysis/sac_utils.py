def vecvel(x,y,sampling_rate):
    """
    ----------------------------------------------------------------------
    vecvel(x,y,sampling_rate)
    ----------------------------------------------------------------------
    Goal of the function :
    Compute eye velocity
    ----------------------------------------------------------------------
    Input(s) :
    x: raw data, horizontal components of the time series
    y: raw data, vertical components of the time series
    samplign_rate: eye tracking sampling rate
    ----------------------------------------------------------------------
    Output(s) :
    vx: velocity, horizontal component
    vy: velocity, vertical component
    ----------------------------------------------------------------------
    Function created by Martin Rolfs
    adapted by Martin SZINTE (mail@martinszinte.net)
    ----------------------------------------------------------------------
    """
    import numpy as np

    n = x.size

    vx = np.zeros_like(x)
    vy = np.zeros_like(y)

    vx[2:n-3] = sampling_rate/6 * (x[4:-1] + x[3:-2] - x[1:-4] - x[0:-5])
    vx[1] = sampling_rate/2*(x[2] - x[0]);
    vx[n-2] = sampling_rate/2*(x[-1]-x[-3])

    vy[2:n-3] = sampling_rate/6 * (y[4:-1] + y[3:-2] - y[1:-4] - y[0:-5])
    vy[1] = sampling_rate/2*(y[2] - y[0]);
    vy[n-2] = sampling_rate/2*(y[-1]-y[-3])

    return vx,vy

def microsacc_merge(x,y,vx,vy,velocity_th,min_dur,merge_interval):
    """
    ----------------------------------------------------------------------
    microsacc_merge(x,y,vx,vy,velocity_th,min_duration,merge_interval)
    ----------------------------------------------------------------------
    Goal of the function :
    Detection of monocular candidates for microsaccades
    ----------------------------------------------------------------------
    Input(s) :
    x: raw data, horizontal components of the time series
    y: raw data, vertical components of the time series
    vx: velocity horizontal components of the time series
    vy: velocity vertical components of the time series
    velocity_th: velocity threshold
    min_dur: saccade minimum duration
    merge_interval: merge interval for subsequent saccade candidates
    ----------------------------------------------------------------------
    Output(s):
    out_val(0:num,0)   onset of saccade
    out_val(0:num,1)   end of saccade
    out_val(1:num,2)   peak velocity of saccade (vpeak)
    out_val(1:num,3)   saccade vector horizontal component
    out_val(1:num,4)   saccade vector vertical component
    out_val(1:num,5)   saccade horizontal amplitude whole sequence
    out_val(1:num,6)   saccade vertical amplitude whole sequence
    ----------------------------------------------------------------------
    Function created by Martin Rolfs
    adapted by Martin SZINTE (mail@martinszinte.net)
    ----------------------------------------------------------------------
    """
    import numpy as np
    import os


    # compute threshold
    msdx = np.sqrt(np.median(vx**2) - (np.median(vx))**2)
    msdy = np.sqrt(np.median(vy**2) - (np.median(vy))**2)

    if np.isnan(msdx):
        msdx = np.sqrt(np.mean(vx**2) - (np.mean(vx))**2)
        if msdx < np.nextafter(0,1):
            os.error('msdx < realmin')

    if np.isnan(msdy):
        msdy = np.sqrt(np.mean(vy**2) - (np.mean(vy))**2 )
        if msdy < np.nextafter(0,1):
            os.error('msdy < realmin')

    radiusx = velocity_th*msdx;
    radiusy = velocity_th*msdy;

    # compute test criterion: ellipse equation
    test = (vx/radiusx)**2 + (vy/radiusy)**2;
    indx = np.where(test>1)[0];

    # determine saccades
    N, nsac, dur, a, k = indx.shape[0], 0, 0, 0, 0

    while k < N-1:
        if indx[k+1]-indx[k]==1:
            dur += 1
        else:
            if dur >= min_dur:
                nsac += 1
                b = k
                if nsac == 1:
                    sac = np.array([indx[a],indx[b]])
                else:
                    sac = np.vstack((sac, np.array([indx[a],indx[b]])))
            a = k+1
            dur = 1

        k += 1

    # check for minimum duration
    if dur >= min_dur:
        nsac += 1;
        b = k;
        if nsac == 1:
            sac = np.array([indx[a],indx[b]])
        else:
            sac = np.vstack((sac, np.array([indx[a],indx[b]])))

    # merge saccades
    if nsac > 0:
        msac = np.copy(sac)
        s    = 0
        sss  = True
        nsac = 1
        while s < nsac-1:
            if sss == False:
                nsac += 1
                msac[nsac,:] = sac[s,:]
            if sac[s+1,0]-sac[s,1] <= merge_interval:
                msac[1] = sac[s+1,1]
                sss = True
            else:
                sss = False
            s += 1
        if sss == False:
            nsac += 1
            msac[nsac,:] = sac[s,:]
    else:
        msac = []
        nsac = 0

    # compute peak velocity, horizonal and vertical components

    msac = np.matrix(msac)
    out_val = np.matrix(np.zeros((msac.shape[0],7))*np.nan)

    if msac.shape[1]>0:
        for s in np.arange(0,msac.shape[0],1):

            # onset and offset
            out_val[s,0],a = msac[s,0], msac[s,0]
            out_val[s,1],b = msac[s,1], msac[s,1]

            # saccade peak velocity (vpeak)
            vpeak = np.max(np.sqrt(vx[a:b]**2 + vy[a:b]**2))
            out_val[s,2] = vpeak

            # saccade vector (dx,dy)
            dx = x[b]-x[a]
            dy = y[b]-y[a]
            out_val[s,3] = dx
            out_val[s,4] = dy

            # saccade amplitude (dX,dY)
            minx,  maxx = np.min(x[a:b]),np.max(x[a:b])
            minix, maxix = np.where(x == minx)[0][0], np.where(x == maxx)[0][0]
            miny,  maxy = np.min(y[a:b]),np.max(y[a:b])
            miniy, maxiy = np.where(y == miny)[0][0], np.where(y == maxy)[0][0]
            dX = np.sign(maxix-minix)*(maxx-minx);
            dY = np.sign(maxiy-miniy)*(maxy-miny);
            out_val[s,5] = dX
            out_val[s,6] = dY


    return out_val

def saccpar(sac):
    """
    ----------------------------------------------------------------------
    saccpar(sac)
    ----------------------------------------------------------------------
    Goal of the function :
    Arange data from microsaccade detection
    ----------------------------------------------------------------------
    Input(s) :
    sac: monocular microsaccades matrix (from microsacc_merge)
    ----------------------------------------------------------------------
    Output(s):
    out_val(0:num,0)   saccade onset
    out_val(0:num,1)   saccade offset
    out_val(1:num,2)   saccade duration
    out_val(1:num,3)   saccade velocity peak
    out_val(1:num,4)   saccade vector distance
    out_val(1:num,5)   saccade vector angle
    out_val(1:num,6)   saccade whole sequence amplitude
    out_val(1:num,7)   saccade whole sequence angle
    ----------------------------------------------------------------------
    Function created by Martin Rolfs
    adapted by Martin SZINTE (mail@martinszinte.net)
    ----------------------------------------------------------------------
    """
    import numpy as np

    if sac.shape[0] > 0:
        # 0. Saccade onset
        sac_onset = np.array(sac[:,0])

        # 1. Saccade offset
        sac_offset = np.array(sac[:,1])

        # 2. Saccade duration
        sac_dur = np.array(sac[:,1] - sac[:,0])

        # 3. Saccade peak velocity
        sac_pvel = np.array(sac[:,2])

        # 4. Saccade vector distance and angle
        sac_dist = np.sqrt(np.array(sac[:,3])**2 + np.array(sac[:,4])**2)

        # 5. Saccade vector angle
        sac_angd = np.arctan2(np.array(sac[:,4]),np.array(sac[:,3]))

        # 6. Saccade whole sequence amplitude
        sac_ampl = np.sqrt(np.array(sac[:,5])**2 + np.array(sac[:,6])**2)

        # 7. Saccade whole sequence amplitude
        sac_anga = np.arctan2(np.array(sac[:,6]),np.array(sac[:,5]))

        # make matrix
        out_val = np.matrix(np.hstack((sac_onset,sac_offset,sac_dur,sac_pvel,sac_dist,sac_angd,sac_ampl,sac_anga)))
    else:
        out_val = np.matrix([]);

    return out_val


def isincircle(x,y,xc,yc,rad):
    """
    ----------------------------------------------------------------------
    isincircle(x,y,xc,yc,rad)
    ----------------------------------------------------------------------
    Goal of the function :
    Check if coordinate in circle
    ----------------------------------------------------------------------
    Input(s) :
    x: x coordinate
    y: y coordinate
    xc: x coordinate of circle
    yc: y coordinate of circle
    rad: radius of circle
    ----------------------------------------------------------------------
    Output(s):
    incircle: (True) = yes, (False) = no
    ----------------------------------------------------------------------
    Function created by Martin Rolfs
    adapted by Martin SZINTE (mail@martinszinte.net)
    ----------------------------------------------------------------------
    """
    import numpy as np

    if np.sqrt((x-xc)**2 + (y-yc)**2) < rad:
        incircle = True
    else:
        incircle = False

    return incircle

def draw_bg_trial(analysis_info,draw_cbar = False):
    """
    ----------------------------------------------------------------------
    draw_bg_trial(analysis_info,draw_cbar = False)
    ----------------------------------------------------------------------
    Goal of the function :
    Draw eye traces figure background
    ----------------------------------------------------------------------
    Input(s) :
    analysis_info: analysis settings
    draw_cbar: draw color circle (True) or not (False)
    ----------------------------------------------------------------------
    Output(s):
    incircle: (True) = yes, (False) = no
    ----------------------------------------------------------------------
    Function created by Martin Rolfs
    adapted by Martin SZINTE (mail@martinszinte.net)
    ----------------------------------------------------------------------
    """
    import numpy as np
    import cortex
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.ticker import FormatStrFormatter
    import matplotlib.colors as colors
    import ipdb
    deb = ipdb.set_trace

    # Saccade analysis per run and sequence
    # Define figure
    title_font = {'loc':'left', 'fontsize':14, 'fontweight':'bold'}
    axis_label_font = {'fontsize':14}
    bg_col = (0.9, 0.9, 0.9)
    axis_width = 0.75
    line_width_corr = 1.5

    # Horizontal eye trace
    screen_val =  12.5
    ymin1,ymax1,y_tick_num1 = -screen_val,screen_val,11
    y_tick1 = np.linspace(ymin1,ymax1,y_tick_num1)
    xmin1,xmax1,x_tick_num1 = 0,1,5
    x_tick1 = np.linspace(xmin1,xmax1,x_tick_num1)

    # Vertical eye trace
    ymin2,ymax2,y_tick_num2 = -screen_val,screen_val,11
    y_tick2 = np.linspace(ymin2,ymax2,y_tick_num2)
    xmin2,xmax2,x_tick_num2 = 0,1,5
    x_tick2 = np.linspace(xmin2,xmax2,x_tick_num2)

    cmap = 'hsv'
    cmap_steps = 16
    col_offset = 0#1/14.0
    base = cortex.utils.get_cmap(cmap)
    val = np.linspace(0, 1,cmap_steps+1,endpoint=False)
    colmap = colors.LinearSegmentedColormap.from_list('my_colmap',base(val), N = cmap_steps)

    pursuit_polar_ang = np.deg2rad(np.arange(0,360,22.5))
    pursuit_ang_norm  = (pursuit_polar_ang + np.pi) / (np.pi * 2.0)
    pursuit_ang_norm  = (np.fmod(pursuit_ang_norm + col_offset,1))*cmap_steps

    pursuit_col_mat = colmap(pursuit_ang_norm.astype(int))
    pursuit_col_mat[:,3]=0.2

    saccade_polar_ang = np.deg2rad(np.arange(0,360,22.5)+180)
    saccade_ang_norm  = (saccade_polar_ang + np.pi) / (np.pi * 2.0)
    saccade_ang_norm  = (np.fmod(saccade_ang_norm + col_offset,1))*cmap_steps

    saccade_col_mat = colmap(saccade_ang_norm.astype(int))
    saccade_col_mat[:,3] = 0.8


    polar_ang = np.deg2rad(np.arange(0,360,22.5))

    fig = plt.figure(figsize = (15, 7))
    gridspec.GridSpec(2,8)

    # Horizontal eye trace
    ax1 = plt.subplot2grid((2,8),(0,0),rowspan= 1, colspan = 4)
    ax1.set_ylabel('Hor. coord. (dva)',axis_label_font,labelpad = 0)
    ax1.set_ylim(bottom = ymin1, top = ymax1)
    ax1.set_yticks(y_tick1)
    ax1.set_xlabel('Time (%)',axis_label_font,labelpad = 10)
    ax1.set_xlim(left = xmin1, right = xmax1)
    ax1.set_xticks(x_tick1)
    ax1.set_facecolor(bg_col)
    ax1.set_title('Horizontal eye position',**title_font)
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    for rad in analysis_info['rads']:
        ax1.plot(x_tick1,x_tick1*0+rad, color = [1,1,1], linewidth = axis_width*2)
        ax1.plot(x_tick1,x_tick1*0-rad, color = [1,1,1], linewidth = axis_width*2)

    # Vertical eye trace
    ax2 = plt.subplot2grid((2,8),(1,0),rowspan= 1, colspan = 4)
    ax2.set_ylabel('Ver. coord. (dva)',axis_label_font, labelpad = 0)
    ax2.set_ylim(bottom = ymin2, top = ymax2)
    ax2.set_yticks(y_tick2)
    ax2.set_xlabel('Time (%)',axis_label_font, labelpad = 10)
    ax2.set_xlim(left = xmin2, right = xmax2)
    ax2.set_xticks(x_tick2)
    ax2.set_facecolor(bg_col)
    ax2.set_title('Vertical eye position',**title_font)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    for rad in analysis_info['rads']:
        ax2.plot(x_tick2,x_tick2*0+rad, color = [1,1,1], linewidth = axis_width*2)
        ax2.plot(x_tick2,x_tick2*0-rad, color = [1,1,1], linewidth = axis_width*2)

    # Screen eye trace
    ax3 = plt.subplot2grid((2,8),(0,4),rowspan= 2, colspan = 4)
    ax3.set_xlabel('Horizontal coordinates (dva)', axis_label_font, labelpad = 10)
    ax3.set_ylabel('Vertical coordinates (dva)', axis_label_font, labelpad = 0)
    ax3.set_xlim(left = ymin1, right = ymax1)
    ax3.set_xticks(y_tick1)
    ax3.set_ylim(bottom = ymin2, top = ymax2)
    ax3.set_yticks(y_tick2)
    ax3.set_facecolor(bg_col)
    ax3.set_title('Screen view',**title_font)
    ax3.set_aspect('equal')

    theta = np.linspace(0, 2*np.pi, 100)
    for rad in analysis_info['rads']:
        ax3.plot(rad*np.cos(theta), rad*np.sin(theta),color = [1,1,1],linewidth = axis_width*3)

    plt.subplots_adjust(wspace = 1.4,hspace = 0.4)

    # color legend
    if draw_cbar == True:
        cbar_axis = fig.add_axes([0.47, 0.77, 0.8, 0.1], projection='polar')
        norm = colors.Normalize(0, 2*np.pi)
        t = np.linspace(0,2*np.pi,200,endpoint=True)
        r = [0,1]
        rg, tg = np.meshgrid(r,t)
        im = cbar_axis.pcolormesh(t, r, tg.T,norm= norm, cmap = colmap)
        cbar_axis.set_yticklabels([])
        cbar_axis.set_xticklabels([])
        cbar_axis.set_theta_zero_location("W",offset = -360/cmap_steps/2)
        cbar_axis.spines['polar'].set_visible(False)
    else:
        cbar_axis = []

    return ax1, ax2, ax3, cbar_axis

