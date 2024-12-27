# 忽略特定警告
import warnings
warnings.filterwarnings("ignore", "Wswiglal-redir-stdio")
import lal

from scipy import special as sy # need special functions for incomplete elliptic integrals of the first kind
import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # 加进度条
from pycbc import types, fft, waveform
from bilby.gw.conversion import redshift_to_luminosity_distance
from astropy import constants 

def lumDis(z):
    """
    in Mpc
    """
    return redshift_to_luminosity_distance(redshift=z)

class myconst:
    Mpc2M=3.08568*10**22 # Mpc转化为米，这里的2是to的意思
    Msun=constants.M_sun.value # 一个太阳质量，单位千克
    as2rad=0.0174532925/3600 #似乎有问题？应该是3.14/180/3600，现在除了。 rad:弧度，1rad=(pi/180)度(角度制)。as角秒，1度=60角分=3600角秒，又叫弧秒
    c=constants.c.value  #光速，单位米每秒
    G=constants.G.value

    
# 定义引力透镜函数
def gravitational_lens(Mass, beta, zs, zl):
    # the disance from the lens to the observer in meters
    DL = lumDis(zl)*myconst.Mpc2M/(1.+zl)/(1.+zl)  #DL等距离是角直径距离
    DS = lumDis(zs)*myconst.Mpc2M/(1.+zs)/(1.+zs) #distance改为lumDis(zs)
    DLS = DS-DL*(1.+zl)/(1.+zs)
    beta *= myconst.as2rad
    
    Mass = Mass*myconst.Msun # already in kilograms
    # Einstein angle
    thetaE = np.sqrt((myconst.G/myconst.c**2)*4*Mass*DLS/DS/DL)

    # angles
    theta_plus = (beta+np.sqrt(beta*beta+4*thetaE*thetaE))/2.0
    theta_minus = (beta-np.sqrt(beta*beta+4*thetaE*thetaE))/2.0

    # deflection angles
    alpha1 = np.absolute(-(myconst.G/myconst.c**2)*4*Mass/theta_plus/DL)
    alpha2 = np.absolute(-(myconst.G/myconst.c**2)*4*Mass/theta_minus/DL)

    # amplitude amplification factors

    # time delay
    DeltaT = 4*Mass*(1+zl)*((theta_plus**2-theta_minus**2) /
                                (2*thetaE**2)+np.log(-theta_plus/theta_minus))/myconst.c*(myconst.G/myconst.c**2)

    return (thetaE/myconst.as2rad, theta_plus/myconst.as2rad, theta_minus/myconst.as2rad,
            alpha1/myconst.as2rad, alpha2/myconst.as2rad, DeltaT)  #这里关于角度的部分除以那个量是为了将rad转化成as

def amp_factor(w,y,Mass,zl):
    if Mass>0:
        xm=(y+np.sqrt(y**2+4))/2
        phiy=(xm-y)**2/2-np.log(xm)
        pi=np.pi   
        w=w*8*pi*(myconst.G)*Mass*(1+zl)*myconst.Msun/(myconst.c**3)  #w=8*pi*G*M_Lz*f/c^3
        mp.mp.dps = 30
        FF=complex(mp.exp(pi*w/4+(1j*w/2)*(np.log(w/2)-2*phiy))*mp.gamma(1-1j*w/2)*mp.hyp1f1(1j*w/2, 1, 1j*w*y**2/2, maxterms=100000))
        return FF
    else:
        xm=(y+np.sqrt(y**2+4))/2
        phiy=(xm-y)**2/2-np.log(xm)
        pi=np.pi
        mp.mp.dps = 30
        FF=complex(mp.exp(pi*w/4+(1j*w/2)*(np.log(w/2)-2*phiy))*mp.gamma(1-1j*w/2)*mp.hyp1f1(1j*w/2, 1, 1j*w*y**2/2, maxterms=100000))
        return FF


def lensed_fd_waveform(mass1,mass2, delta_f, f_range, Mass, beta, zs, zl, lensed):
    kwds={'approximant':'IMRPhenomD','mass1':mass1,'mass2':mass2, 'distance':lumDis(zs), 'delta_f':delta_f,'f_lower':f_range[0],
         'f_final':f_range[1]}
    hp1, hc1=waveform.get_fd_waveform(**kwds)
    frequencies = hp1.sample_frequencies
    valid_indices = (frequencies >= f_range[0]) & (frequencies <= f_range[1])
    frequencies = frequencies[valid_indices]
    hp = hp1[valid_indices]
    hc = hc1[valid_indices]
    
    y=beta/gravitational_lens(Mass, beta, zs, zl)[0] # y=beta/theta_E

    if lensed=='lensed':
        Flist = [amp_factor(i,y,Mass,zl) for i in tqdm(frequencies)]
        waveform_hp=[hp[i] * Flist[i] for i in range(len(hp))]
        waveform_hc=[hc[i] * Flist[i] for i in range(len(hp))]
    else:
        waveform_hp=hp
        waveform_hc=hc
    
    return {"plus":(frequencies, waveform_hp), "cross":(frequencies, waveform_hc)}
