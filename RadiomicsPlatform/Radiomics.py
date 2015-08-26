from __main__ import vtk, qt, ctk, slicer, os

import csv
import numpy
import pdb
import unittest
import collections
import itertools
import math
import string
import operator

import radiomicsplatform
import matlabbridge
import datahandling

import pdb

#
# Radiomics
#

class Radiomics:
  def __init__(self, parent):
    parent.title = "RadiomicsPlatform"
    parent.categories = ["Radiomics"]
    parent.dependencies = []
    parent.contributors = ["Vivek Narayan (Dana Farber), Hugo Aerts (Dana Farber), Jayendar Jagadeesan(BWH)"]
    parent.helpText = """
    """
    parent.acknowledgementText = """
    """
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    """
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['Radiomics'] = self.runTest
    """
  def runTest(self):
    tester = RadiomicsTest()
    tester.runTest()

#
# qRadiomicsWidget
#

class RadiomicsWidget:
  def __init__(self, parent = None): 
    try:
      #Load Test Cases
      imageFile = 'C:\\Users\\Vivek Narayan\\Desktop\\Breast DCE-MRI\\TestPatient1\\StudyDate1\\Reconstructions\\Pre.nrrd'
      labelFile = 'C:\\Users\\Vivek Narayan\\Desktop\\Breast DCE-MRI\\TestPatient1\\StudyDate1\\Segmentations\\Pre_labelMap.nrrd'
      properties = {}
      properties['labelmap'] = True
      imageLoad = list(slicer.util.loadVolume(imageFile, returnNode=True))
      labelLoad = list(slicer.util.loadVolume(labelFile, properties, returnNode=True))   
    except:
      pass
    
    self.selImageNode = None  # Currently selected image node for feature extraction
    self.selLabelNode = None  # Currently selected label node for feature extraction
    self.fileDialog = None
    
    # Data of database
    self.mainPatientdir = ''
    self.DBpatientNames = []
    self.DatabaseHierarchyDict = collections.OrderedDict()
    
    self.outputDir = None
    self.outputDirName  = "_RadiomicsData"
    
    self.datafile = None
    self.datafileName   = ''
    
    # Feature Data
    self.FeatureVectors = []
    self.AdvancedSettings = {}
 
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.input1Selector.setMRMLScene(slicer.mrmlScene)
      self.input2Selector.setMRMLScene(slicer.mrmlScene)
      self.parent.show()

  def setup(self):

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "Radiomics Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    # self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)
    reloadCollapsibleButton.collapsed = True
    #---------------------------------------------------------
    
    #
    # Compute Radiomics area
    #
    self.computeRadiomicsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.computeRadiomicsCollapsibleButton.text = "Slicer Radiomics Platform"
    self.layout.addWidget(self.computeRadiomicsCollapsibleButton)
    self.computeRadiomicsFormLayout = qt.QFormLayout(self.computeRadiomicsCollapsibleButton)

    # 
    # Universal Advanced Settings Collapsible Button
    #
    
    self.AdvancedSettingsCollapsibleButton = ctk.ctkCollapsibleButton()
    self.AdvancedSettingsCollapsibleButton.text = "Advanced Settings"
    self.AdvancedSettingsCollapsibleButtonLayout = qt.QHBoxLayout()
    self.AdvancedSettingsCollapsibleButton.setLayout(qt.QHBoxLayout())    
    self.computeRadiomicsFormLayout.addWidget(self.AdvancedSettingsCollapsibleButton)
    self.AdvancedSettingsCollapsibleButton.collapsed = True
    
    self.AdvancedSettingsFrame = qt.QFrame(self.AdvancedSettingsCollapsibleButton)
    self.AdvancedSettingsFrameLayout = qt.QFormLayout()
    self.AdvancedSettingsFrame.setLayout(self.AdvancedSettingsFrameLayout)
    self.AdvancedSettingsCollapsibleButton.layout().addWidget(self.AdvancedSettingsFrame)
    
    # Label Values 
    self.inputLabelValues = qt.QLabel("Label Values:", self.AdvancedSettingsFrame)
    self.inputLabelValuesField = qt.QLineEdit("1",self.AdvancedSettingsFrame)
    self.AdvancedSettingsFrameLayout.addRow(self.inputLabelValues, self.inputLabelValuesField )
    
    # Interpolation Settings
    self.settingsRadioButtonFrame = qt.QFrame(self.AdvancedSettingsFrame)
    self.settingsRadioButtonFrame.setLayout(qt.QHBoxLayout())
    self.interpolationsGroup = qt.QButtonGroup(self.settingsRadioButtonFrame)
    self.ipRawButton = qt.QRadioButton("Raw")
    self.ip1x1x1Button = qt.QRadioButton("(1,1,1)")
    self.ip2x2x2Button = qt.QRadioButton("(2,2,2)")
    self.ip3x3x3Button = qt.QRadioButton("(3,3,3)")
    self.ipRawButton.checked = True
    self.interpolationsGroup.addButton(self.ipRawButton)
    self.interpolationsGroup.addButton(self.ip1x1x1Button)
    self.interpolationsGroup.addButton(self.ip2x2x2Button)
    self.interpolationsGroup.addButton(self.ip3x3x3Button)
    self.settingsRadioButtonFrame.layout().addWidget(self.ipRawButton)
    self.settingsRadioButtonFrame.layout().addWidget(self.ip1x1x1Button)
    self.settingsRadioButtonFrame.layout().addWidget(self.ip2x2x2Button)
    self.settingsRadioButtonFrame.layout().addWidget(self.ip3x3x3Button)
    self.interpHeader = qt.QLabel("Interpolation:")
    self.AdvancedSettingsFrameLayout.addRow(self.interpHeader,self.settingsRadioButtonFrame)
    
    # Bin Width
    self.inputBinWidth = qt.QLabel("Bin Width:", self.AdvancedSettingsFrame)
    self.inputBinWidthField = qt.QLineEdit("25",self.AdvancedSettingsFrame)
    self.AdvancedSettingsFrameLayout.addRow(self.inputBinWidth, self.inputBinWidthField )
    
    # Modality Radio Buttons Frame
    self.ModalityRadioButtonFrame = qt.QFrame(self.AdvancedSettingsFrame)
    self.ModalityRadioButtonFrame.setLayout(qt.QHBoxLayout())
    self.ModalityFileFormatGroup = qt.QButtonGroup(self.ModalityRadioButtonFrame)
    self.CTButton = qt.QRadioButton("CT")
    self.CTButton.checked = True
    self.MRIButton = qt.QRadioButton("MRI")
    self.PETButton = qt.QRadioButton("PET")
    self.ModalityFileFormatGroup.addButton(self.CTButton)
    self.ModalityFileFormatGroup.addButton(self.MRIButton)
    self.ModalityFileFormatGroup.addButton(self.PETButton)
    self.ModalityRadioButtonFrame.layout().addWidget(self.CTButton)
    self.ModalityRadioButtonFrame.layout().addWidget(self.MRIButton)
    self.ModalityRadioButtonFrame.layout().addWidget(self.PETButton)
    self.ModalityInputLabel = qt.QLabel("Image Modality:", self.AdvancedSettingsFrame)
    self.AdvancedSettingsFrameLayout.addRow(self.ModalityInputLabel, self.ModalityRadioButtonFrame)
    # 
    # End Universal Advanced Settings Collapsible Button
    #
    
    # Parent Tab Widget
    self.computeRadiomicsTabWidget = qt.QTabWidget()
    self.computeRadiomicsFormLayout.addWidget(self.computeRadiomicsTabWidget)
    
    #  Radiomics Current Mode
    self.tabComputeRadiomicsCurr = qt.QWidget()
    self.singleCaseInputFormLayout = qt.QFormLayout()
    self.tabComputeRadiomicsCurr.setLayout(self.singleCaseInputFormLayout)
    self.tabComputeRadiomicsCurrName = "Single Case Mode"
    self.computeRadiomicsTabWidget.addTab(self.tabComputeRadiomicsCurr, self.tabComputeRadiomicsCurrName)
    
    # Input 1: Input Image
    self.input1Frame = qt.QFrame(self.tabComputeRadiomicsCurr)
    self.input1Frame.setLayout(qt.QHBoxLayout())
    self.singleCaseInputFormLayout.addWidget(self.input1Frame)
    self.input1Selector = qt.QLabel("Input Image: ", self.input1Frame)
    self.input1Frame.layout().addWidget(self.input1Selector)
    self.input1Selector = slicer.qMRMLNodeComboBox(self.input1Frame)
    self.input1Selector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.input1Selector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.input1Selector.addEnabled = False
    self.input1Selector.removeEnabled = False
    self.input1Selector.setMRMLScene( slicer.mrmlScene )
    self.input1Frame.layout().addWidget(self.input1Selector)

    # Input 2: Input Segmentation
    self.input2Frame = qt.QFrame(self.tabComputeRadiomicsCurr)
    self.input2Frame.setLayout(qt.QHBoxLayout())
    self.singleCaseInputFormLayout.addWidget(self.input2Frame)
    self.input2Selector = qt.QLabel("Input Label:  ", self.input2Frame)
    self.input2Frame.layout().addWidget(self.input2Selector)
    self.input2Selector = slicer.qMRMLNodeComboBox(self.input2Frame)
    self.input2Selector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.input2Selector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 1 )
    self.input2Selector.addEnabled = False
    self.input2Selector.removeEnabled = False
    self.input2Selector.setMRMLScene( slicer.mrmlScene )
    self.input2Frame.layout().addWidget(self.input2Selector)
    
    # Settings Collapsible Button
    self.SettingsCollapsibleButtonCurr = ctk.ctkCollapsibleButton()
    self.SettingsCollapsibleButtonCurr.text = "Settings"
    self.SettingsCollapsibleButtonCurrLayout = qt.QHBoxLayout()
    self.SettingsCollapsibleButtonCurr.setLayout(self.SettingsCollapsibleButtonCurrLayout)    
    self.singleCaseInputFormLayout.addWidget(self.SettingsCollapsibleButtonCurr)
    self.SettingsCollapsibleButtonCurr.collapsed = False
    self.SettingsFrameCurr = qt.QFrame(self.SettingsCollapsibleButtonCurr)
    self.SettingsFrameCurr.setLayout(qt.QFormLayout())
    self.SettingsCollapsibleButtonCurrLayout.addWidget(self.SettingsFrameCurr)
    
    # Settings 
    self.para2curr = qt.QCheckBox("Use MatlabBridge", self.tabComputeRadiomicsCurr)
    self.para2curr.toolTip = "When checked: Matlab features extracted"
    self.para2curr.checked = False
    self.SettingsFrameCurr.layout().addRow(self.para2curr) 
    
    # Apply Radiomics button
    self.RadiomicCurrButtonsFrame = qt.QFrame(self.tabComputeRadiomicsCurr)
    self.RadiomicCurrButtonsFrame.setLayout(qt.QHBoxLayout())
    self.singleCaseInputFormLayout.addWidget(self.RadiomicCurrButtonsFrame)
    
    self.radiomicsCurrButton = qt.QPushButton("Compute Radiomics Features (Single Case)", self.RadiomicCurrButtonsFrame)
    self.radiomicsCurrButton.enabled = True
    self.radiomicsCurrButton.toolTip = "Run the feature extraction for a single case."
    self.RadiomicCurrButtonsFrame.layout().addWidget(self.radiomicsCurrButton)
    
    # Chart
    self.RadiomicsTableFrame = qt.QFrame(self.tabComputeRadiomicsCurr)
    self.RadiomicsTableFrameLayout = qt.QHBoxLayout()
    self.RadiomicsTableFrame.setLayout(self.RadiomicsTableFrameLayout)
    self.singleCaseInputFormLayout.addWidget(self.RadiomicsTableFrame)
    
    self.RadiomicsTableView = qt.QTableView(self.RadiomicsTableFrame)
    self.RadiomicsTableView.sortingEnabled = True
    self.RadiomicsTableView.minimumHeight = 175
    self.RadiomicsTableView.verticalHeader().visible = False
    self.RadiomicsTableView.setColumnWidth(0,30)
    self.RadiomicsTableFrameLayout.addWidget(self.RadiomicsTableView)
    self.RadiomicsTableModel = qt.QStandardItemModel()
    
    # Save Table Button
    self.saveButton = qt.QPushButton("Save Table to CSV File", self.RadiomicCurrButtonsFrame)
    self.saveButton.toolTip = "Save Radiomics Feature from table to CSV file"
    self.saveButton.enabled = False
    self.singleCaseInputFormLayout.layout().addWidget(self.saveButton)
    
    #---------------------------------------------------------
    # Connections
    self.radiomicsCurrButton.connect('clicked(bool)', self.onRadiomicsCurr)
    self.saveButton.connect('clicked()', self.onSave)
    
    self.layout.addStretch(1)     # Add vertical spacer

  def onRadiomicsCurr(self):
    self.AdvancedSettings = self.initializeAdvancedSettings()

    self.selImageNode = self.input1Selector.currentNode()
    self.selLabelNode = self.input2Selector.currentNode()
    if not datahandling.ValidateVolumes(self.selImageNode, self.selLabelNode): return
    else: self.AdancedSettings = self.updateImageAndLabelSettingsCurr(self.AdvancedSettings, self.selImageNode,self.selLabelNode)
    
    if self.para2curr.checked: self.pythonExtract = False
    else: self.pythonExtract = True
    
    self.radiomicsCurrButton.enabled = False
    self.radiomicsCurrButton.text = "Extracting features..."
    self.radiomicsCurrButton.repaint()
    slicer.app.processEvents()

    # Extract features current patient
    if self.pythonExtract:
      RadiomicsPlatformLogic = radiomicsplatform.FeatureExtraction(self.AdvancedSettings)
      RadiomicsPlatformLogic.ExtractFeatures()
      RadiomicsFeatureVector = RadiomicsPlatformLogic.GetFeatureVector()
      self.FeatureVectors.append(RadiomicsFeatureVector)
      datahandling.PopulateRadiomicsTable(self, self.RadiomicsTableView, self.RadiomicsTableModel, self.FeatureVectors)
    else:
      reconstructionsDir = os.path.dirname(self.AdvancedSettings["imagefilepath"])    
      self.outputDir, self.dataFile, self.printfilePath = datahandling.InitializeDatabase(self.pythonExtract, reconstructionsDir, self.outputDirName) 
      RadiomicsFeatureVector = matlabbridge.FeatureExtractionMatlab(self.selImageNode,self.selLabelNode,self.AdvancedSettings["imagefilepath"],self.AdvancedSettings["labelfilepath"],self.outputDir, self.AdvancedSettings["patientid"], self.AdvancedSettings["levels"],logfilePath=self.printfilePath)
    
    self.saveButton.enabled = True
    self.radiomicsCurrButton.enabled = True
    self.radiomicsCurrButton.text = "Compute Radiomics (Current Case)"
    
  def initializeAdvancedSettings(self):
    AdvancedSettings = {}
    
    AdvancedSettings["levels"] = [str(level.strip()) for level in self.inputLabelValuesField.text.split(',')]
    if self.ipRawButton.checked: AdvancedSettings["resampledpixelspacing"] = False
    elif self.ip1x1x1Button.checked: AdvancedSettings["resampledpixelspacing"] = (1,1,1)
    elif self.ip2x2x2Button.checked: AdvancedSettings["resampledpixelspacing"] = (2,2,2)
    elif self.ip3x3x3Button.checked: AdvancedSettings["resampledpixelspacing"] = (3,3,3)
    
    AdvancedSettings["binwidth"] = int(self.inputBinWidthField.text.strip())
    if self.CTButton.checked: AdvancedSettings["modality"] = "CT"
    elif self.MRIButton.checked: AdvancedSettings["modality"] = "MRI"
    elif self.PETButton.checked: AdvancedSettings["modality"] = "PET"
    
    return AdvancedSettings
    
  def updateImageAndLabelSettingsCurr(self, AdvancedSettings, selImageNode, selLabelNode):
    # Set the directory to store the data (directory with the image files)
    AdvancedSettings["imagefilepath"] = selImageNode.GetStorageNode().GetFileName()
    AdvancedSettings["labelfilepath"] = selLabelNode.GetStorageNode().GetFileName()
    AdvancedSettings["basepixelspacing"] = selImageNode.GetSpacing()
    AdvancedSettings["dimensions"] = selImageNode.GetImageData().GetDimensions()
    
    reconstructionsDir = os.path.dirname(AdvancedSettings["imagefilepath"])
    studyDateDir = os.path.dirname(reconstructionsDir)
    patientDir = os.path.dirname(studyDateDir)
  
    AdvancedSettings["seriesdescription"] = os.path.splitext(os.path.basename(AdvancedSettings["imagefilepath"]))[0]
    AdvancedSettings["studydate"] = os.path.basename(studyDateDir)
    AdvancedSettings["patientid"] = os.path.basename(patientDir)
    
    return AdvancedSettings
    
  def onSave(self):
    if not self.fileDialog:
      self.fileDialog = qt.QFileDialog(self.parent)
      self.fileDialog.options = self.fileDialog.DontUseNativeDialog
      self.fileDialog.acceptMode = self.fileDialog.AcceptSave
      self.fileDialog.selectFile("_PythonFeatures")
      self.fileDialog.defaultSuffix = "csv"
      self.fileDialog.setNameFilter("Comma Separated Values (*.csv)")
      self.fileDialog.setDirectory(self.outputDir)
      self.fileDialog.connect("fileSelected(QString)", self.onFileSelected)
    self.fileDialog.show()
  
  def onFileSelected(self, fileName):
    if not fileName: return
    self.dataFile = fileName
    for RadiomicsFeatureVector in self.FeatureVectors:
      datahandling.SaveDatabase(RadiomicsFeatureVector, self.dataFile)   
    
  def onReload(self,moduleName="Radiomics"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    globals()[moduleName] = slicer.util.reloadScriptedModule(moduleName)

  def onReloadAndTest(self,moduleName="Radiomics"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")


#
# Legacy Code For Tests
#          
class Radiomics2Test(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()
  
  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Radiomics()

  def test_Radiomics(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = Radiomics2Logic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
