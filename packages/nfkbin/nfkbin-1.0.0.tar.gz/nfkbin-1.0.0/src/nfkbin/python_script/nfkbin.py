################################################################
# NF-kBIn is developed for predicting KF-kB inhibitors.        #
# It is developed by Prof G. P. S. Raghava's group.            #
# Please cite: https://webs.iiitd.edu.in/raghava/nfkbin/       #
################################################################
import argparse
import warnings
import subprocess
import pkg_resources
import os
import sys
import numpy as np
import pandas as pd
import math
import itertools
from collections import Counter
import pickle
import re
import glob
import time
import uuid
from time import sleep
from tqdm import tqdm
from sklearn.ensemble import ExtraTreesClassifier
import zipfile
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Please provide following arguments') 

## Read Arguments from command
parser.add_argument("-i", "--input", type=str, required=True, help="Input: Moleculues in the SMILES format per line")
parser.add_argument("-o", "--output",type=str, help="Output: File for saving results by default outfile.csv")
parser.add_argument("-t","--threshold", type=float, help="Threshold: Value between 0 to 1 by default 0.41")
parser.add_argument("-d","--display", type=int, choices = [1,2], help="Display: 1:NF-kB Inhibitors only, 2: All molecules, by default 1")
args = parser.parse_args()

# Function to check the SMILES format
def validate_smiles_format(file_path):
    def is_valid_smiles(smile):
        """Basic rules for SMILES validation."""
        if not smile:  # Check for empty strings
            return False
        
        # Rule 1: Only allow valid SMILES characters
        valid_chars = re.compile(r"^[A-Za-z0-9@+\-\[\]\(\)=#$:/\\.%*]+$")
        if not valid_chars.match(smile):
            return False
        
        # Rule 2: Check balanced parentheses and brackets
        if smile.count('(') != smile.count(')'):
            return False
        if smile.count('[') != smile.count(']'):
            return False
        
        # Rule 3: No spaces within the SMILES string
        if " " in smile:
            return False
        
        return True

    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                smile = line.strip()
                if not is_valid_smiles(smile):
                    print(f"Error: Invalid SMILES format on line {line_num}: '{smile}'")
                    sys.exit(1)  # Halt the process
        print("All SMILES strings passed basic format validation.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
# Function to genrerate tags
def taggen(file1):
    df1 = pd.read_csv(file1, names=['SMILES'])
    df1['Name'] = ['samples'+str(i+1) for i in range(len(df1))]
    df_2 = df1[['Name','SMILES']]
    return df_2
# Function to generate the file
def filegen(td,fp):
    cc = ['Name', 'AATS3v', 'AATS7e', 'AATSC3m', 'AATSC7m', 'AATSC7e', 'MATS2c', 'MATS7m', 'MATS8s', 'VE3_Dze', 'VR2_Dzs', 'VR1_Dt', 'nHCsatu', 'ndNH', 'MDEN-11', 'nTG12HeteroRing', 'VE1_D']
    dd = ['Name', 'GraphFP171', 'FP584', 'FP785', 'FP282', 'KRFP3160', 'ExtFP116', 'KRFP72', 'ExtFP441', 'ExtFP688', 'GraphFP679', 'ExtFP777', 'FP309', 'ExtFP500', 'KRFPC349', 'PubchemFP571', 'FP59', 'KRFPC1427', 'GraphFP189', 'ExtFP61', 'KRFP3517', 'KRFPC3517', 'FP678', 'ExtFP408', 'GraphFP982', 'KRFP3256', 'KRFPC3256', 'FP7', 'FP587', 'ExtFP346', 'ExtFP909', 'FP915', 'ExtFP299', 'FP583', 'FP843', 'KRFP1933', 'KRFPC1933', 'KRFP300', 'KRFP2996', 'ExtFP896', 'PubchemFP478', 'ExtFP183', 'GraphFP912', 'ExtFP355', 'SubFPC287', 'KRFP4830', 'KRFPC4830', 'MACCSFP26', 'PubchemFP559', 'AD2D234', 'ExtFP390', 'ExtFP1015', 'KRFP4112', 'KRFPC4112', 'FP79', 'GraphFP989', 'GraphFP856', 'AD2D184', 'APC2D8_O_Cl', 'KRFPC557', 'PubchemFP147', 'FP142', 'KRFP367', 'KRFPC367', 'KRFP1117', 'GraphFP320', 'GraphFP809', 'KRFP1458', 'APC2D8_O_X', 'KRFP3634', 'KRFPC3634', 'ExtFP967', 'GraphFP696', 'ExtFP771', 'ExtFP973', 'GraphFP90', 'ExtFP421', 'ExtFP947', 'FP379', 'GraphFP168', 'APC2D5_O_F', 'APC2D6_C_X', 'KRFP4102', 'GraphFP623', 'AD2D214', 'FP98', 'GraphFP56', 'ExtFP586', 'KRFP2229', 'KRFPC2229', 'KRFPC3479', 'KRFP4248', 'KRFPC4248', 'KRFPC4002', 'FP863', 'ExtFP994', 'ExtFP998', 'ExtFP37', 'AD2D658', 'APC2D9_S_S', 'FP741', 'SubFPC288', 'ExtFP140', 'FP356', 'GraphFP32', 'ExtFP174', 'SubFPC137', 'ExtFP932', 'ExtFP741', 'FP856', 'KRFP3592', 'KRFP3107', 'KRFPC3107', 'ExtFP328', 'FP296', 'KRFP4749', 'KRFP3213', 'KRFPC2139', 'KRFPC3213', 'KRFP2842', 'KRFP1437', 'KRFPC1437', 'KRFP3447', 'KRFPC3447', 'KRFP4334', 'KRFPC4334', 'KRFP418', 'KRFP1074', 'KRFPC1074', 'KRFP188', 'KRFP933', 'KRFPC4207', 'KRFP4470', 'KRFPC4470', 'AD2D755', 'KRFP4815', 'KRFPC4815', 'KRFP1939', 'KRFP3739', 'KRFP4497', 'KRFPC4497', 'FP400', 'GraphFP236', 'ExtFP918', 'GraphFP100', 'ExtFP732', 'FP808', 'ExtFP471', 'GraphFP346', 'APC2D10_F_Br', 'KRFP4531', 'FP736', 'GraphFP74', 'KRFP1624', 'KRFPC1624', 'KRFP1575', 'KRFPC1575', 'ExtFP528', 'KRFPC1146', 'KRFP4312', 'KRFPC4312', 'KRFP874', 'KRFPC874', 'ExtFP938', 'ExtFP195', 'ExtFP671', 'KRFP3554', 'KRFP4045', 'KRFPC3704', 'KRFPC4045', 'MACCSFP116', 'FP872', 'PubchemFP718', 'PubchemFP781', 'FP313', 'KRFPC4197', 'KRFPC4736', 'KRFP2289', 'KRFPC2712', 'GraphFP222', 'ExtFP643', 'KRFP2011', 'KRFPC2011', 'KRFP2955', 'KRFPC2955', 'KRFPC2815', 'KRFP3923', 'KRFPC2107', 'KRFPC3923', 'GraphFP749', 'ExtFP955', 'FP998', 'ExtFP119', 'ExtFP878', 'GraphFP879', 'ExtFP253', 'FP301', 'GraphFP377', 'AD2D375', 'FP55', 'GraphFP625', 'KRFP3148', 'KRFPC3148', 'APC2D5_Cl_X', 'GraphFP97', 'KRFP27', 'AD2D116', 'APC2D2_S_Br', 'SubFP302', 'PubchemFP543', 'FP638', 'ExtFP661', 'GraphFP223', 'KRFPC3707', 'FP427', 'ExtFP599', 'FP437', 'ExtFP419', 'GraphFP910', 'KRFP2435', 'KRFPC2435', 'FP112', 'ExtFP789', 'GraphFP954', 'KRFP4193', 'KRFPC4193', 'GraphFP202', 'FP891', 'ExtFP444', 'GraphFP82', 'FP911', 'AD2D547', 'FP663', 'KRFP3897', 'GraphFP331', 'KRFPC492', 'KRFP444', 'PubchemFP695', 'AD2D627', 'KRFP1473', 'KRFPC1473', 'ExtFP664', 'AD2D705', 'FP238', 'ExtFP374', 'GraphFP479', 'GraphFP639', 'GraphFP712', 'FP905', 'KRFPC4508', 'ExtFP627']
    df1 = pd.read_csv(td)
    df1.fillna(0,inplace=True)
    df2 = pd.read_csv(fp)
    df2.fillna(0,inplace=True)
    df4 = df1[cc]
    df6 = df2[dd]
    df7 = pd.merge(df4, df6, on="Name")
    return df7
# Function to normalize
def scaling_file(new_df):
    with open('model/scaler_model.pkl', 'rb') as f:
        scaler = pickle.load(f)
    scaled_new_data = scaler.transform(new_df)
    scaled_new_df = pd.DataFrame(scaled_new_data, columns=new_df.columns)
    return scaled_new_df
# Function to read and implement the model
def model_run(file1,file2):
    a = []
    data_test = file1
    clf = pickle.load(open(file2,'rb'))
    y_p_score1=clf.predict_proba(data_test)
    y_p_s1=y_p_score1.tolist()
    a.extend(y_p_s1)
    df = pd.DataFrame(a)
    df1 = df.iloc[:,-1].round(2)
    df2 = pd.DataFrame(df1)
    df2.columns = ['ML_score']
    return df2
def determine(file1,file2):
    df1 = file1
    thr = float(file2)
    aa = []
    for i in range(0,len(df1)):
        if df1['ML_score'][i] >= thr:
            aa.append("NF-kB Inhibitor")
        else:
            aa.append("Non-inhibitor")
    df2 = pd.DataFrame(aa)
    df2.columns = ['Prediction']
    return df2
('############################################################################################')
print('# This program NF-kBIn is developed for predicting the NF-kB inhibitors.        #')
print('# This tool was developed by Prof G. P. S. Raghava\'s group.                    #')
print('# Please cite: NF-kBIn; available at https://webs.iiitd.edu.in/raghava/nfkbin/  #')
print('############################################################################################')

# Parameter initialization or assigning variable for command level arguments

Sequence= args.input        # Input variable 
 
# Output file 
 
if args.output == None:
    result_filename= "outfile.csv" 
else:
    result_filename = args.output
         
# Threshold 
if args.threshold == None:
        Threshold = 0.41
else:
        Threshold= float(args.threshold)
# Display
if args.display == None:
        dplay = int(1)
else:
        dplay = int(args.display)


###########################################################################################

print("\n");
print('##############################################################################')
print('Summary of Parameters:')
print('Input File: ',Sequence,'; Threshold: ', Threshold)
print('Output File: ',result_filename,'; Display: ',dplay)
print('##############################################################################')
#========================================Extracting Model====================================
if os.path.isdir('model') == False:
    with zipfile.ZipFile('./model.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
else:
    pass
#======================= Prediction Module start from here =====================
print('\n======= Thanks for using Predict module of NF-kBIn. Your results will be stored in file :',result_filename,' =====\n')
print('\n=======Validating the format of SMILES in the submitted file =====\n')
validate_smiles_format(Sequence)
tags = taggen(Sequence)
print(Sequence)
print(tags)
os.system("obabel "+ Sequence + " -O molecules/samples.smi -m")
os.system("/usr/bin/java -jar padel/PaDEL-Descriptor.jar -2d -descriptortypes padel/nfkbin_descriptors.xml -dir molecules/ -usefilenameasmolname -log -file 2d.csv")
os.system("/usr/bin/java -jar padel/PaDEL-Descriptor.jar -fingerprints -descriptortypes padel/nfkbin_descriptors.xml -dir molecules/ -usefilenameasmolname -log -file fp.csv")
X1 = filegen('2d.csv','fp.csv')
X = X1.iloc[:,1:]
y = X1[['Name']]
X2 = scaling_file(X)
mlres = model_run(X2,'model/svc_model_server')
mlres = mlres.round(3)
det = determine(mlres,Threshold)
df41 = pd.concat([y,mlres,det],axis=1)
df44 = pd.merge(tags,df41,on='Name')
df44.columns = ['Molecule_ID','SMILE','ML_Score','Prediction']
if dplay == 1:
    df44 = df44.loc[df44.Prediction=="NF-kB Inhibitor"]
else:
    df44 = df44
df44 = round(df44,3)
df44.to_csv(result_filename, index=None)
directory_path = 'molecules'
if os.path.exists(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            os.remove(os.path.join(root, file))  # Remove files
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))  # Remove subdirectories
os.remove('2d.csv')
os.remove('2d.csv.log')
os.remove('fp.csv')
os.remove('fp.csv.log')
print("\n=========Process Completed. Have an awesome day ahead.=============\n")
print('\n======= Thanks for using NF-kBIn. Your results are stored in file :',result_filename,' =====\n\n')
