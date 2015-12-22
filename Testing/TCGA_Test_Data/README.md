pyradiomics Testing Data

Note: Testing Data contains 5 Cases, each with an image and 
a corresponding segmentation (label map) of the tumor structure.
Each of the 5 pairs of files(image + label) have an associated
CSV file (with suffix: '_features.csv') containing the 
radiomics features computed within the label ROI, on the image.    

brain1: Brain MRI data from The Cancer Genome Atlas-Glioblastoma Multiforme (TCGA-GBM) archive.
        ID: "TCGA-02-0003"
        Series Description: "AXIAL-T1-POST-GD_TCGA-02-0003_TCGA-02-0003_PREOP_SCAN13_Background"
        
brain2: Brain MRI data from The Cancer Genome Atlas-Glioblastoma Multiforme (TCGA-GBM) archive.
        ID: "TCGA-02-0006"
        Series Description: "AXIAL-T1-POST-GD_TCGA-02-0006_TCGA-02-0006_PREOP_SCAN6_Background"
        
lung1: Lung CT data from The Cancer Genome Atlas-Lung Adenocarcinoma (TCGA-LUAD) archive.
       ID: "TCGA-17-Z013"
       Series Description: "Chest #1"
         
lung2: Lung CT data from The Cancer Genome Atlas-Lung Adenocarcinoma (TCGA-LUAD) archive.
       ID: "TCGA-17-Z015"
       Series Description: "Chest Routine #1"

breast1: Breast DCE-MRI(Pre-Contrast) tutorial data from the 
         Wiki page for the OpenCAD 3DSlicer Extension.
         ID: "TestPatient1"
         Series Description: "Pre"