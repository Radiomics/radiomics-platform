from __future__ import print_function
from __main__ import vtk, qt, ctk, slicer, os

import collections
import pdb

def FeatureExtractionMatlab(imageNode,labelNode,ImageFilePath,LabelFilePath,outputDir,IDCurrPatient,Levels,logfilePath=False):
    # Calculate Radiomics features for selected data
    imageModality = "CT"

    # Perform feature extraction
    if imageNode and labelNode:
      if Levels is not False: Levels = ','.join(map(str,Levels))
      
      radiomicsmatlabCLIparameters = {'ImageNode': imageNode, 'LabelNode': labelNode, 'ImageFileName': ImageFilePath, 'LabelFileName': LabelFilePath, 'Levels': Levels, 'OutputDir': outputDir, 'PatientID': str(IDCurrPatient), 'Modality': str(imageModality)}
      radiomicsmatlabCLIparameters['SeriesName'], radiomicsmatlabCLIparameters['StudyDate'] = GetNameStudyDate(imageNode, ImageFilePath)
      
      cliNode = slicer.cli.run(slicer.modules.radiomicsmatlab, None , radiomicsmatlabCLIparameters , wait_for_completion=True)
      if logfilePath:
        with open(logfilePath, 'a') as logfile:      
          logfile.write(cliNode.GetParameterAsString('OutputString') + "\n")
      
      featureVector = {} #figure out how to get feature vectors from matlab
      return featureVector
 
def GetNameStudyDate(img, imgpath):
  reconstructionsDir = os.path.dirname(imgpath)
  studyDateDir = os.path.dirname(reconstructionsDir)
  
  studyDate = ' '.join(os.path.basename(studyDateDir).split('_'))
  seriesName = img.GetName().replace(',','')
  
  return(seriesName, studyDate)