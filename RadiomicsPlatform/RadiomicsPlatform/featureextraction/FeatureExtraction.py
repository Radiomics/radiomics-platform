from __future__ import print_function

import os
import numpy
import collections
import itertools
import operator
import SimpleITK as sitk

import radiomicsplatform.imagearrayprocessing
import radiomicsplatform.radiomicsfeatures
import pdb

class FeatureExtraction:

    def __init__(self, sitkImageNode, sitkLabelNode):
        self.sitkImageNode = sitkImageNode
        self.sitkLabelNode = sitkLabelNode
        
        self.Settings = {}
        self.RadiomicsFeatureVector = collections.OrderedDict()
        
        # Extract parameter values from image
        self.SetDimensions(self.sitkImageNode.GetSize())
        self.SetBasePixelSpacing(self.sitkImageNode.GetSpacing())
        
        # Set default Values for other parameters
        self.SetLabelLevels([1])
        self.SetBinWidth(25)
        self.SetResampledPixelSpacing(self.Settings["basepixelspacing"])
        self.SetSeriesDescription("UnknownSeries")
        self.SetStudyDate("UnknownStudy")
        self.SetPatientID("UnknownPatientID")
            
    def ExtractFeatures(self):
        # create Numpy Arrays 
        self.imageNodeArray = sitk.GetArrayFromImage(self.sitkImageNode) #radiomicsplatform.imagearrayprocessing.ImageToNumpyArray(self.Settings["imagefilepath"])
        self.labelNodeArray = sitk.GetArrayFromImage(self.sitkLabelNode) #radiomicsplatform.imagearrayprocessing.ImageToNumpyArray(self.Settings["labelfilepath"])
        
        # create a rectangular matrix with the dimensions of the tumor
        # center the tumor voxels in the matrix and set the non-tumor voxels to a pad value 
        self.matrix, self.matrixCoordinates = radiomicsplatform.imagearrayprocessing.PadTumorMaskToCube(self.imageNodeArray, self.labelNodeArray)

        # Feature Extraction   
        # Node Information       
        self.generalFeatures = radiomicsplatform.radiomicsfeatures.Radiomics_General(self.Settings)
        self.RadiomicsFeatureVector.update( self.generalFeatures.EvaluateFeatures() )         
        
        # First Order Statistics    
        self.firstOrderStatistics = radiomicsplatform.radiomicsfeatures.Radiomics_First_Order(self.matrix, self.matrixCoordinates, self.Settings["binwidth"], self.Settings["resampledpixelspacing"])
        self.RadiomicsFeatureVector.update( self.firstOrderStatistics.EvaluateFeatures() )
        # Variance and Standard Deviation in numpy are different from Matlab values
        
        # Shape Features
        self.shapeFeatures = radiomicsplatform.radiomicsfeatures.Radiomics_Shape(self.matrix, self.matrixCoordinates, self.Settings["resampledpixelspacing"])
        self.RadiomicsFeatureVector.update( self.shapeFeatures.EvaluateFeatures() )
        
        # Texture Features(GLCM)     
        self.textureFeaturesGLCM = radiomicsplatform.radiomicsfeatures.Radiomics_GLCM(self.matrix, self.matrixCoordinates, self.Settings["binwidth"])   
        self.RadiomicsFeatureVector.update( self.textureFeaturesGLCM.EvaluateFeatures() )
          
        # Texture Features(GLRL)  
        self.textureFeaturesGLRL = radiomicsplatform.radiomicsfeatures.Radiomics_RLGL(self.matrix, self.matrixCoordinates, self.Settings["binwidth"])
        self.RadiomicsFeatureVector.update( self.textureFeaturesGLRL.EvaluateFeatures() )
        # Recheck feature computations
        
        """
        # Texture Features(GLSZM) 
        self.textureFeaturesGLSZM = radiomicsplatform.radiomicsfeatures.TextureGLSZM(self.matrix, self.matrixCoordinates, self.targetVoxelArray)
        self.RadiomicsFeatureVector.update( self.textureFeaturesGLSZM.EvaluateFeatures() )
        """
               
        # Laplacian of a Gaussian Features(LoG)  
        self.laplacianOfGaussianFeatures = radiomicsplatform.radiomicsfeatures.Radiomics_LoG(self.sitkImageNode, self.sitkLabelNode, self.Settings["binwidth"], self.Settings["resampledpixelspacing"])
        self.RadiomicsFeatureVector.update( self.laplacianOfGaussianFeatures.EvaluateFeatures() )
        
        """
        # Wavelet Features  
        self.waveletFeatures = radiomicsplatform.radiomicsfeatures.WaveletFeatures(self.matrix, self.matrixCoordinates, self.targetVoxelArray)
        self.RadiomicsFeatureVector.update( self.waveletFeatures.EvaluateFeatures() )
        """
    
    def GetFeatureVector(self):
        return (self.RadiomicsFeatureVector)
        
    def SetDimensions(self, inputDimensions):
        # The dimensions of the image as a 3-tuple: (X,Y,Z)
        self.Settings["dimensions"] = inputDimensions
        
    def SetBasePixelSpacing(self, inputBasePixelSpacing):
        # The base pixel-spacing of the image as a 3-tuple: (X,Y,Z)
        self.Settings["basepixelspacing"] = inputBasePixelSpacing
        
    def SetLabelLevels(self, inputLevelsList):
        # A list of the target label values as strings in the label-map image i.e. [1] or [1,8]. 
        # TODO: Radiomics features will be computed separately for each label value.
        self.Settings["levels"] = inputLevelsList
        
    def SetBinWidth(self, inputBinWidth):
        # An integer representing the bin width (a range of pixel intensity values). Default is 25.
        # Prior to computing features, The voxel intensity values within the tumor region 
        # will be mapped to a bin index, with bin edges centered at 0.
        self.Settings["binwidth"] = int(inputBinWidth)

    def SetResampledPixelSpacing(self, inputResampledPixelSpacing):
        # A 3-tuple representing the final pixel-spacing to resample the image
        # prior to computing Radiomics features i.e. (1,1,1) or (3,3,3).
        self.Settings["resampledpixelspacing"] = inputResampledPixelSpacing
        #self.imageNode = Interpolate3D.interpolateScalarVolumeNode3D(selImageNode, outputPixelSpacing=Settings["resampledpixelspacing"])
        #self.labelNode = Interpolate3D.interpolateScalarVolumeNode3D(selLabelNode, outputPixelSpacing=Settings["resampledpixelspacing"])

    def SetSeriesDescription(self, inputSeriesDescription):
        # A string representing the series description for the image. 
        # Ideally, the series description is the basename of the image filepath.
        # i.e. "C://Dataset1//234056//07112015_Study1//Reconstructions//CT_Lung.nrrd"
        #   Series Description is "CT_Lung"
        self.Settings["seriesdescription"] = str(inputSeriesDescription)

    def SetStudyDate(self, inputStudyDate):
        # A string representing the study date for the image. 
        # Ideally, the study date is the basename of the directory two directories up from the image file.
        # i.e. "C://Dataset1//234056//07112015_Study1//Reconstructions//CT_Lung.nrrd"
        #   The study date is "07112015_Study1"
        self.Settings["studydate"] = str(inputStudyDate)

    def SetPatientID(self, inputPatientID):
        # A string representing the PatientID for the image. 
        # Ideally, the PatientID is the basename of the directory three directories up from the image file.
        # i.e. "C://Dataset1//234056//07112015_Study1//Reconstructions//CT_Lung.nrrd"
        #   The PatientID is "234056"
        self.Settings["patientid"] = str(inputPatientID)