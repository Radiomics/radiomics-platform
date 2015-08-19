# before running this, set PYTHONPATH to 
#  radiomics-platform/RadiomicsPlatform
from RadiomicsPlatform import RadiomicsPreProcessing
import os, sys

rootPath = None
# get the location of the data
try:
  pythonPath = os.environ['PYTHONPATH']
  # assume python path with Radiomics in it is it!
  for p in pythonPath.split(os.pathsep):
    print p
    if p.find('Radiomics')>=0:
      rootPath = p
      break
except:
  pass

if rootPath == None:
  print 'Failed to find root path'
  sys.exit(-1)

dataRoot = os.path.join(rootPath,'Testing','Data')

settings = {
  "imagefilepath" : os.path.join(dataRoot,'prostate_phantom.nrrd'),
  "labelfilepath" : os.path.join(dataRoot,'prostate_phantom_label.nrrd'),
  "resampledpixelspacing" : False,
  "basepixelspacing" : False}

rpp = RadiomicsPreProcessing(settings)

rpp.ComputeRadiomicsFeatures()
