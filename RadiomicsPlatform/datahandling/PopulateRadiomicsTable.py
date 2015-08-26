from __main__ import vtk, qt, ctk, slicer, os

def PopulateRadiomicsTable(self, RadiomicsTableView, RadiomicsTableModel, FeatureVectors):
  #initialize table with another function 
  #use this function to add a feature vector to the table
  
  if not (FeatureVectors):
    return
    
  self.items = []
  self.RadiomicsTableModel = qt.QStandardItemModel()
  self.RadiomicsTableView.setModel(self.RadiomicsTableModel)
  self.RadiomicsTableView.verticalHeader().visible = False
  row = 0
  col = 0
  
  wholeNumberKeys = ['Voxel Count', 'Gray Levels', 'Minimum Intensity', 'Maximum Intensity', 'Median Intensity', 'Range']
  precisionOnlyKeys = ['Entropy', 'Volume mm^3', 'Volume cc', 'Mean Intensity', 'Mean Deviation', 'Root Mean Square', 'Standard Deviation', 'Surface Area mm^3']
  
  for featureVector in FeatureVectors:
    col = 0    
    for feature in featureVector:
      item = qt.QStandardItem()   
      value = featureVector[feature]       
      featureFormatted = value
      # add formatting here
      item.setText(str(featureFormatted))
      item.setToolTip(feature)
      self.RadiomicsTableModel.setItem(row,col,item)
      self.items.append(item)
      col += 1
    row += 1
  
  self.RadiomicsTableView.setColumnWidth(0,30)
  self.RadiomicsTableModel.setHeaderData(0,1," ")
  
  # set table headers
  col = 0
  for feature in FeatureVectors[0]:
    self.RadiomicsTableView.setColumnWidth(col,15*len(feature))
    self.RadiomicsTableModel.setHeaderData(col,1,feature)
    col += 1