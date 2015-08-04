#-----------------------------------------------------------------------------
set(MODULE_NAME Radiomics)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS 
  ${MODULE_NAME}.py

  SlicerDataHandlingLib/__init__  
  SlicerDataHandlingLib/InitializeDatabase
  SlicerDataHandlingLib/SaveDatabase
  SlicerDataHandlingLib/ValidateVolumes
  SlicerDataHandlingLib/PopulateRadiomicsTable
  
  RadiomicsToolsLib/__init__
  RadiomicsToolsLib/RadiomicsFeatureExtractionMatlab
  
  RadiomicsPlatform/__init__
  
  RadiomicsPlatform/RadiomicsPreProcessingLib/__init__
  RadiomicsPlatform/RadiomicsPreProcessingLib/RadiomicsPreProcessing
  RadiomicsPlatform/RadiomicsPreProcessingLib/Interpolate3D
  
  RadiomicsPlatform/RadiomicsImageArrayLib/__init__
  RadiomicsPlatform/RadiomicsImageArrayLib/BinImage
  RadiomicsPlatform/RadiomicsImageArrayLib/ImageToNumpyArray
  RadiomicsPlatform/RadiomicsImageArrayLib/PadTumorMaskToCube
  RadiomicsPlatform/RadiomicsImageArrayLib/PadCubicMatrix
  
  RadiomicsPlatform/RadiomicsFeaturesLib/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_General/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_General/Radiomics_General
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_General/Radiomics_General_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_First_Order/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_First_Order/Radiomics_First_Order
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_First_Order/Radiomics_First_Order_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_Shape/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_Shape/Radiomics_Shape
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_Shape/Radiomics_Shape_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLCM/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLCM/Radiomics_GLCM
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLCM/Radiomics_GLCM_Matrix
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLCM/Radiomics_GLCM_Coefficients
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLCM/Radiomics_GLCM_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_RLGL/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_RLGL/Radiomics_RLGL
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_RLGL/Radiomics_RLGL_Matrix
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_RLGL/Radiomics_RLGL_Coefficients
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_RLGL/Radiomics_RLGL_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLSZM/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLSZM/Radiomics_GLSZM
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLSZM/Radiomics_GLSZM_Matrix
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLSZM/Radiomics_GLSZM_Coefficients
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_GLSZM/Radiomics_GLSZM_Features
  
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_LoG/__init__
  RadiomicsPlatform/RadiomicsFeaturesLib/Radiomics_LoG/LoGFeatures
  )

set(MODULE_PYTHON_RESOURCES
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )
