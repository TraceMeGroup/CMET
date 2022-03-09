import sys
import numpy as np
from netCDF4 import Dataset
import netCDF4 as nc
import importlib

class modelObj:
    def __init__(self, name, var, **keywords):
        self.name = name
        self.var  = var
        self.path = keywords.get("path", self.checkPath()) 
        self.test = keywords.get("test", self.checkPath())   
    def checkPath(self):
        return "NeedReadInDataset"

class caseObj:
    # create a new case object to run model evaluation.
    def __init__(self, modelObjs, runConf, **keywords):
        self.modelObjs  = modelObjs
        self.runConf    = runConf   # dict data type
        self.runType    = keywords.get("runType",    self.runConf['runType'])
        self.startYr    = keywords.get("startYr",    self.runConf['lsRangYr'][0])
        self.endYr      = keywords.get("endYr",      self.runConf['lsRangYr'][1])
        self.month      = keywords.get("month",      self.runConf['month'])
        self.outType    = keywords.get("outType",    self.runConf['outType'])
        self.modelNames = keywords.get("modelNames", self.initModelNames())

    def initModelNames(self):
        lsModelNames = [iModel.name for iModel in self.modelObjs]
        return lsModelNames

    def initModelInfo(self):
        pass
    def callPreProcesses(self):
        pass
    def runScript(self):
        # call the script to process the data
        print("runScript",self.outType)
        if self.outType == "all": 
            scriptName = "scripts.test"
            className  = "test"
        lib = importlib.import_module(scriptName)
        className = getattr(lib,nnn)
        objClass  = className()
        objClass.callTest()
        

def readNcFile(filepath, variablename): 
    nc_obj = Dataset(filepath)
    data   = np.array((nc_obj.variables[variablename][:]).data,dtype=float)
    try:
        data[data == nc_obj.variables[variablename].missing_value] = np.nan
    except AttributeError as e:
        print("Read nc-files: ", e)
    return data

def checkArgvs(arrArgv):
    # return dictArg
    dictArg = {}
    dictArg['lsModels'] = [iModel for iModel in arrArgv[2].split(",")]
    dictArg['var']      = str(arrArgv[3])
    dictArg['runConf']  = {}         
    dictArg['runConf']['runType']  = arrArgv[1]
    dictArg['runConf']['lsRangYr'] = [int(iYr) for iYr in arrArgv[4].split(",")]
    dictArg['runConf']['month']    = int(arrArgv[5])
    dictArg['runConf']['outType']  = str(arrArgv[6])
    return dictArg   

if  __name__ == '__main__':
    print("This is CMETcore.py")
    # 1. read the argvs:
    arrArgv = sys.argv               # get the preset values from run shell 
    dictArg = checkArgvs(arrArgv)    # runType; lsModels; var; lsRangYr; month; outType
    # 2. check the data, and found the path of data
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
    lsModelObjs = [m1, m2, m3]
    # 3. create the caseObj and process the data
    case = caseObj(modelObjs = lsModelObjs, runConf = dictArg['runConf']) 
    case.runScript()
    print(case.startYr)
    # -------------------------------------------
    # figPath = "/mnt/d/ubuntu/traceMeGroup"
    # data      = readNcFile(m1.path, m1.var)
    # outFig    = figPath + "/figure_test.png"
    # vMinMax   = [1.577924e-08,0.0002177286]
    # titleName = "The global distribution of the dominant variable"
    # unit      = "-"
    # colors    = ['#C0C0C0','#32CD32','#98FB98','#F08080','#FFFF00','#1E90FF']
    # plt_globMap([180,360], data[0,:,:], outFig, vMinMax, titleName, unit, figSize=[14,9], mapProj="cyl", cmap="jet")
    # 3. call for pre-processes
    # 4. creat the case object to call the script. 