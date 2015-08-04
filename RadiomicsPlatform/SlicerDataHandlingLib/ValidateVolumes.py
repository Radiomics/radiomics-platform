def ValidateVolumes(imageNode, labelNode):
  if not (imageNode and labelNode):
    qt.QMessageBox.critical(slicer.util.mainWindow(),
        'Radiomics:', 'Radiomics: Please select Image and Label for Radiomics feature extraction')
    return False
  if (imageNode == labelNode):
    qt.QMessageBox.critical(slicer.util.mainWindow(),
        'Radiomics:', 'Radiomics: Please select two different volumes for Image and Label ')
    return False
  if (imageNode.GetImageData().GetDimensions() != labelNode.GetImageData().GetDimensions()):
    qt.QMessageBox.critical(slicer.util.mainWindow(),
        'Radiomics:', 'Radiomics: Volumes do not have the same dimensions ')
    return False
  return True