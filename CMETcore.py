import sys

print("This is CMETcore.py")
# get the preset values from run shell 
arr_argv   = sys.argv
runType    = str(arr_argv[1])
modelNames = arr_argv[2]
variable   = arr_argv[3]
rangeYear  = arr_argv[4]
month      = arr_argv[5]
outType    = arr_argv[6]
print(type(runType))
# --------------------------------
