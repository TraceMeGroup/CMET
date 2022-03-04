# plot for global map
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm

class test:
    def __init__(self, ):

    def convertLon(data):
        nlat, nlon = 180, 360
        midInd     = 180
        data4plot  = np.full([nlat,nlon],np.nan) #drawData
        data4plot[:,:midInd] = data[:,midInd:]
        data4plot[:,midInd:] = data[:,:midInd]
        return data4plot

    def plt_globMap(nLatLon, data, outFig, vMinMax, titleName, unit, figSize=[14,9], mapProj="cyl", cmap="jet"): 
        latmin,latmax,lonmin,lonmax = -90,90,-180,180
        r_lat = np.arange(latmin,latmax)
        r_lon = np.arange(lonmin,lonmax)
        fig   = plt.figure(figsize=(figSize[0],figSize[1]))
        ax    = fig.add_axes([0.05,0.15,0.9,0.8])
        lim   = np.linspace(vMinMax[0],vMinMax[1],500)
        # m     = Basemap(projection = mapProj, resolution='l', ax=ax)
        m     = Basemap(projection = "robin", resolution='l',lat_0=0, lon_0=0, ax=ax) # cyl; robin 
        x, y  = m(*np.meshgrid(r_lon,r_lat))
        drawData = convertLon(data)
        ctf   = ax.contourf(x,y,drawData.squeeze(),lim,cmap="YlGnBu",zorder=1)#,extend="both")
        m.drawcoastlines(linewidth=0.4,zorder=3)
        # m.drawlsmask(land_color=(0, 0, 0, 0), ocean_color="lightgray",lakes=True, zorder=2)
        m.drawmapboundary(color='k', linewidth=1.0) #, fill_color=None, zorder=None, ax=None)
        position = fig.add_axes([0.17, 0.15, 0.67, 0.03]) # left,bottom,right,top
        cb = plt.colorbar(ctf, cax=position,orientation="horizontal",extend = 'none')
        font1 = {'size':40}
        cb.set_ticks(np.linspace(vMinMax[0],vMinMax[1],5),font1)
        # cb.set_ticks(font1)
        # cb.set_ticklabels(np.linspace(vMinMax[0],vMinMax[1],5))
        cb.ax.tick_params(labelsize=16) 
        cb.set_label(titleName+' ('+unit+")", fontsize=24, labelpad=10)
        plt.savefig(outFig) 