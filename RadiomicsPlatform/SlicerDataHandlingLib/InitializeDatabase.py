import os
from datetime import datetime

def InitializeDatabase(pythonExtract, mainPatientDir, outputDirName, KeywordMatchSettings=False):
    """ 
    Initialize the log file (printfile) and radiomics data file (a csv file)
    """
    curr_time = datetime.now()
    curr_time = str(curr_time.strftime(('%Y%m%d-%H%M%S')))
    
    outputDirName = outputDirName + '_' + curr_time
    outputDir = os.path.join(mainPatientDir,outputDirName)
    if not os.path.exists(outputDir): 
        os.makedirs(outputDir)
    
    if pythonExtract:
        datafileName = curr_time + '_PythonRadiomicsFeatures.csv'
    else:
        datafileName = curr_time + '_MatlabRadiomicsFeatures.csv'  
      
    datafile = os.path.join(outputDir, datafileName)
    
    printfilename = curr_time + '_RadiomicsBatchExtract_log.txt'
    printfilePath = os.path.join(outputDir,printfilename)
    
    with open(printfilePath, 'a') as printfile:
        printfile.write("Radiomics Batch Extract" + "\n")
        printfile.write("\tSettings:" + "\n")
        printfile.write("\t\tmainPatientDir: " + str(mainPatientDir) + "\n")
        printfile.write("\t\toutputDir: " + str(outputDir) + "\n")
        
        if KeywordMatchSettings:
            printfile.write("\t\tKeywordMatchingSettings:  " + str(KeywordMatchSettings) + "\n")
    
    return outputDir, datafile, printfilePath