import numpy
import collections

class RadiomicsFirstOrder:

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
        self.radiomics_first_order_FeatureVector[self.prefix+"energy"] = "self.energyValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"totalenergy"] = "self.totalEnergyValue(self.targetVoxelArray, self.pixelSpacing)"
        self.radiomics_first_order_FeatureVector[self.prefix+"entropy"] = "self.entropyValue(self.targetVoxelArray, self.binwidth)"
        self.radiomics_first_order_FeatureVector[self.prefix+"min"] = "self.minIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"max"] = "self.maxIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"mean"] = "self.meanIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"median"] = "self.medianIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"range"] = "self.rangeIntensity(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"md"] = "self.meanDeviation(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"rms"] = "self.rootMeanSquared(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"std"] = "self.standardDeviation(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"skewness"] = "self.skewnessValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"kurtosis"] = "self.kurtosisValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"var"] = "self.varianceValue(self.targetVoxelArray)"
        self.radiomics_first_order_FeatureVector[self.prefix+"uniformity"] = "self.uniformityValue(self.targetVoxelArray, self.binwidth)"

    def EvaluateFeatures(self):
        for feature in self.radiomics_first_order_FeatureVector:
            try:
                self.radiomics_first_order_FeatureVector[feature] = eval(self.radiomics_first_order_FeatureVector[feature])
            except AttributeError:
                self.radiomics_first_order_FeatureVector[feature] = "Function Does Not Exist"
        return(self.radiomics_first_order_FeatureVector)

    def _moment(self, a, moment=1, axis=0):
      if moment == 1:
        return numpy.float64(0.0)
      else:
        mn = numpy.expand_dims(numpy.mean(a,axis), axis)
        s = numpy.power((a-mn), moment)
        return numpy.mean(s, axis)

    def energyValue(self, targetVoxelArray):
      shiftedParameterArray = targetVoxelArray + 2000
      return (numpy.sum(shiftedParameterArray**2))

    def totalEnergyValue(self, targetVoxelArray, pixelSpacing):
        shiftedParameterArray = targetVoxelArray + 2000
        cubicMMPerVoxel = reduce(lambda x,y: x*y , pixelSpacing)
        return(cubicMMPerVoxel*numpy.sum(shiftedParameterArray**2))

    def entropyValue(self, targetVoxelArray, binwidth):
        ##check for binning centered at 0
        bincount = numpy.ceil((numpy.max(targetVoxelArray) - numpy.min(targetVoxelArray))/float(binwidth))
        bins = numpy.histogram(targetVoxelArray, bins=bincount)[0]
        bins = bins/float(bins.sum())
        return (-1.0 * numpy.sum(bins*numpy.where(bins!=0,numpy.log2(bins),0)))

    def minIntensity(self, targetVoxelArray):
        return (numpy.min(targetVoxelArray))

    def maxIntensity(self, targetVoxelArray):
        return (numpy.max(targetVoxelArray))

    def meanIntensity(self, targetVoxelArray):
        return (numpy.mean(targetVoxelArray))

    def medianIntensity (self, targetVoxelArray):
        return (numpy.median(targetVoxelArray))

    def rangeIntensity (self, targetVoxelArray):
        return (numpy.max(targetVoxelArray) - numpy.min(targetVoxelArray))

    def meanDeviation(self, targetVoxelArray):
        return ( numpy.mean(numpy.absolute( (numpy.mean(targetVoxelArray) - targetVoxelArray) )) )

    def rootMeanSquared(self, targetVoxelArray):
        shiftedParameterArray = targetVoxelArray + 2000
        return ( numpy.sqrt((numpy.sum(shiftedParameterArray**2))/float(shiftedParameterArray.size)) )

    def standardDeviation(self, targetVoxelArray):
        return (numpy.std(targetVoxelArray))

    def skewnessValue(self, a, axis=0):
        m2 = _moment(a, 2, axis)
        m3 = _moment(a, 3, axis)

        zero = (m2 == 0)
        vals = numpy.where(zero, 0, m3 / m2**1.5)

        if vals.ndim == 0:
            return vals.item()

        return vals

    def kurtosisValue(self, a, axis=0):
        m2 = _moment(a,2,axis)
        m4 = _moment(a,4,axis)
        zero = (m2 == 0)

        olderr = numpy.seterr(all='ignore')

        try:
            vals = numpy.where(zero, 0, m4 / m2**2.0)
        finally:
            numpy.seterr(**olderr)
        if vals.ndim == 0:
            vals = vals.item()

        return vals

    def varianceValue(self, targetVoxelArray):
        return (numpy.std(targetVoxelArray)**2)

    def uniformityValue(self, targetVoxelArray, binwidth):
        bincount = numpy.ceil((numpy.max(targetVoxelArray) - numpy.min(targetVoxelArray))/float(binwidth))
        bins = numpy.histogram(targetVoxelArray, bins=bincount)[0]
        bins = bins/float(bins.sum())
        return (numpy.sum(bins**2))
