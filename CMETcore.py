import sys
import numpy as np
from netCDF4 import Dataset
import netCDF4 as nc
from scripts.test import plt_globMap

class modelObj:
    def __init__(self, **keywords):
        self.name = keywords.get("name", None)
        self.var  = keywords.get("var",  None)
        self.path = keywords.get("path", None)

class caseObj(modelObj):
    # create a new case object to run model evaluation.
    #  
    def __init__(self, **keywords):
        self.runType = keywords.get("runType",None)
        self.modelNames = keywords.get("")

def readNcFile(filepath, variablename): 
    nc_obj = Dataset(filepath)
    data   = np.array((nc_obj.variables[variablename][:]).data,dtype=float)
    try:
        data[data == nc_obj.variables[variablename].missing_value] = np.nan
    except AttributeError as e:
        print("Read nc-files: ", e)
    return data

if  __name__ == '__main__':
    print("This is CMETcore.py")
    # get the preset values from run shell 
    arr_argv   = sys.argv
    runType    = str(arr_argv[1])
    ls_models  = [iModel for iModel in arr_argv[2].split(",")] 
    variable   = str(arr_argv[3])
    ls_rangYr  = [int(iyear) for iyear in arr_argv[4].split(",")]
    month      = int(arr_argv[5])
    outType    = arr_argv[6]
    # --------------------------------
    print(outType)
    print(ls_rangYr)
    # --------------------------------
    # This part is used for testing the databases
    # -------------------------------------------
    # model         | variable  | path
    # -------------------------------------------
    # CESM2         |pr         | /mnt/d/ubuntu/traceMeGroup/testData/CESM2/pr_Ayear_CESM2_historical_r1i1p1f1_gn_198001-201012_cdo.nc
    # CNRM-ESM2-1   |pr         | /mnt/d/ubuntu/traceMeGroup/testData/CNRM-ESM2-1/pr_Ayear_CNRM-ESM2-1_historical_r1i1p1f2_gr_198001-201012_cdo.nc
    # IPSL-CM6A-LR  |pr         | /mnt/d/ubuntu/traceMeGroup/testData/IPSL-CM6A-LR/pr_Ayear_IPSL-CM6A-LR_historical_r1i1p1f1_gr_198001-201012_cdo.nc
    # -------------------------------------------
    # creat the model object, maybe 
    m1 = modelObj(name="CESM2",        var="pr", path="/mnt/d/ubuntu/traceMeGroup/testData/CESM2/pr_Ayear_CESM2_historical_r1i1p1f1_gn_198001-201012_cdo.nc")
    m2 = modelObj(name="CNRM-ESM2-1",  var="pr", path="/mnt/d/ubuntu/traceMeGroup/testData/CNRM-ESM2-1/pr_Ayear_CNRM-ESM2-1_historical_r1i1p1f2_gr_198001-201012_cdo.nc")
    m3 = modelObj(name="IPSL-CM6A-LR", var="pr", path="/mnt/d/ubuntu/traceMeGroup/testData/IPSL-CM6A-LR/pr_Ayear_IPSL-CM6A-LR_historical_r1i1p1f1_gr_198001-201012_cdo.nc")
    ls_modelObj = [m1, m2, m3]
    # -------------------------------------------
    figPath = "/mnt/d/ubuntu/traceMeGroup"
    data      = readNcFile(m1.path, m1.var)
    outFig    = figPath + "/figure_test.png"
    vMinMax   = [1.577924e-08,0.0002177286]
    titleName = "The global distribution of the dominant variable"
    unit      = "-"
    # colors    = ['#C0C0C0','#32CD32','#98FB98','#F08080','#FFFF00','#1E90FF']
    plt_globMap([180,360], data[0,:,:], outFig, vMinMax, titleName, unit, figSize=[14,9], mapProj="cyl", cmap="jet")