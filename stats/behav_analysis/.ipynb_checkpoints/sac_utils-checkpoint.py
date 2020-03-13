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
