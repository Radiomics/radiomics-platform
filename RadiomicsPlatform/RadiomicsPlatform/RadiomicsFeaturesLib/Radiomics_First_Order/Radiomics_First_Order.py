import numpy
import collections

import Radiomics_First_Order_Features

class Radiomics_First_Order:

    def __init__(self, matrix, matrixCoordinates, binwidth, pixelSpacing):
        self.matrix = matrix
        self.matrixCoordinates = matrixCoordinates
        self.targetVoxelArray = self.matrix[self.matrixCoordinates]
        
        self.binwidth = binwidth
        self.pixelSpacing = pixelSpacing

        self.InitializeFeatureVector()    
    
    def InitializeFeatureVector(self):
        self.prefix = "Stats_"
        self.radiomics_first_order_FeatureVector = collections.OrderedDict()
        self.radiomics_first_order_FeatureVector[self.prefix+"energy"] = "Radiomics_First_Order_Features.energyValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"totalenergy"] = "Radiomics_First_Order_Features.totalEnergyValue(self.targetVoxelArray, self.pixelSpacing)"
        self.radiomics_first_order_FeatureVector[self.prefix+"entropy"] = "Radiomics_First_Order_Features.entropyValue(self.targetVoxelArray, self.binwidth)" 
        self.radiomics_first_order_FeatureVector[self.prefix+"min"] = "Radiomics_First_Order_Features.minIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"max"] = "Radiomics_First_Order_Features.maxIntensity(self.targetVoxelArray)"  
        self.radiomics_first_order_FeatureVector[self.prefix+"mean"] = "Radiomics_First_Order_Features.meanIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"median"] = "Radiomics_First_Order_Features.medianIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"range"] = "Radiomics_First_Order_Features.rangeIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"md"] = "Radiomics_First_Order_Features.meanDeviation(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"rms"] = "Radiomics_First_Order_Features.rootMeanSquared(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"std"] = "Radiomics_First_Order_Features.standardDeviation(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"skewness"] = "Radiomics_First_Order_Features.skewnessValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"kurtosis"] = "Radiomics_First_Order_Features.kurtosisValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"var"] = "Radiomics_First_Order_Features.varianceValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"uniformity"] = "Radiomics_First_Order_Features.uniformityValue(self.targetVoxelArray, self.binwidth)"
      
    def EvaluateFeatures(self):
        for feature in self.radiomics_first_order_FeatureVector:
            try:
                self.radiomics_first_order_FeatureVector[feature] = eval(self.radiomics_first_order_FeatureVector[feature])
            except AttributeError:
                self.radiomics_first_order_FeatureVector[feature] = "Function Does Not Exist"
        return(self.radiomics_first_order_FeatureVector)
              
