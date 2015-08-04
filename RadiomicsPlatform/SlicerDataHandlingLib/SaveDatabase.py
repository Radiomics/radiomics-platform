def SaveDatabase(RadiomicsFeatureVector,file):
    import csv, os
    if not os.path.isfile(file): open(file,mode='w') # First time open the file
    reader = csv.reader(open(file,mode='r+'))
    if not reader: return
    
    table = [[e for e in r] for r in reader]

    writer = csv.writer(open(file,mode='a'),lineterminator='\n')      
    if not table: # First entry
        writer.writerow(RadiomicsFeatureVector.keys()) # Write headers
        writer.writerow(RadiomicsFeatureVector.values())
    else:         # Replace or Append
        writer.writerow(RadiomicsFeatureVector.values())