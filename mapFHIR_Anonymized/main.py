from resources.settings import bcolors
from resources.settings import paths

#libraries
import csv
import json
import os
import pandas as pd
import cx_Oracle
import collections
import timeit
import math
from datetime import datetime
from colorama import Fore, Back, Style

#mapping functions
from resources.patient import func_dictPat
from resources.condition import func_dictCond
from resources.medicationAdm import func_dictMed
from resources.observation import func_dictObs
from resources.procedure import func_dictProcSurg
from resources.send import sendRes

#RESOURCES FLAGS
pat_flag = 0
cond_flag = 1
obs_flag = 0
med_flag = 0
procS_flag = 0

CURR_PATH = os.path.dirname(os.path.realpath(__file__))

print(f"{bcolors.WARNING}{bcolors.BOLD}Resources to be created:{bcolors.ENDC}")
if pat_flag == 1:
    print(f"{bcolors.OKGREEN}- PATIENT{bcolors.ENDC}")
if cond_flag == 1:
    print(f"{bcolors.OKGREEN}- CONDITION{bcolors.ENDC}")
if obs_flag == 1:
    print(f"{bcolors.OKGREEN}- OBSERVATION{bcolors.ENDC}")
if med_flag == 1:
    print(f"{bcolors.OKGREEN}- MEDICATION_ADM{bcolors.ENDC}")
if procS_flag == 1:
    print(f"{bcolors.OKGREEN}- PROCEDURE_SURGERY{bcolors.ENDC}")
if pat_flag == 0 and cond_flag == 0 and obs_flag == 0 and med_flag == 0 and procS_flag == 0:
    print(f"{bcolors.FAIL}no resource to create -> Set the resource flag to 1 for the resources to be created{bcolors.ENDC}")

#DATA EXTRACTION METHOD (1: Oracle server | 2: csv file)
extraction_mode = ["ORACLE SERVER","CSV FILE"]
extraction = 2
print(f"{bcolors.OKCYAN}Extraction from: "+extraction_mode[extraction-1]+f"{bcolors.ENDC}")
print("---------------")
print()

if extraction == 1:
    dsn_tns = cx_Oracle.makedsn('orarac-scan.gaslini.lan', '1521', service_name='GEST') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
    conn = cx_Oracle.connect(user=r'PANCARESURPASS', password='PicrgG=31!', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
    c = conn.cursor()

elif extraction == 2:
    if pat_flag == 1:
        print(f"{bcolors.OKGREEN}- Extraction from{bcolors.ENDC}", paths.IN_Pat)
    if cond_flag == 1:
        print(f"{bcolors.OKGREEN}- Extraction from{bcolors.ENDC}", paths.IN_Cond)
    if obs_flag == 1:
        print(f"{bcolors.OKGREEN}- Extraction from{bcolors.ENDC}", paths.IN_Obs)
    if med_flag == 1:
        print(f"{bcolors.OKGREEN}- Extraction from{bcolors.ENDC}", paths.IN_MedAdm)
    if procS_flag == 1:
        print(f"{bcolors.OKGREEN}- Extraction from{bcolors.ENDC}", paths.IN_ProcS)
    
##PAT
if pat_flag == 1:
    res = "Patient"
    print(f"{bcolors.WARNING}building Patients...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute("SELECT * FROM V_ANAGRAFE_PAZIENTI")
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_ANAGRAFE_PAZIENTI",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        with open(paths.IN_Pat) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    printed_jsons = 0
    id_ress = []
    for r in range(len(df.index)):
        row = df.iloc[r]
        
        primaryKey = [row.A01_ID_PERSONA]
        OUT_Pat = 'Patient/P_'+str(primaryKey[0])+'.json'

        fhirPat = func_dictPat(row)

        id_res = sendRes(fhirPat,res)
        record = [id_res,primaryKey[0]]
        id_ress.append(record)

        printed_jsons += 1
        with open(OUT_Pat, 'w') as json_fileP:
            json_fileP.write(fhirPat)

    pd.DataFrame(id_ress,columns=['ID','k1']).to_csv('IDs/' + res + '_ids.csv',index=False)
    print("Printed jsons: ",printed_jsons)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start)            

#COND
if cond_flag ==1:
    res = "Condition"
    print(f"{bcolors.WARNING}building Conditions...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute('SELECT * FROM V_PAZIENTI_DIAGNOSI')
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_PAZIENTI_DIAGNOSI",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        with open(paths.IN_Cond) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    df.insert(0, "PRIMARY_KEY",df.index)

    printed_jsons = 0
    id_ress = []
    for r in range(len(df.index)):
        row = df.iloc[r]

        primaryKey = [row.ID_PAZIENTE,row.PRIMARY_KEY]
        OUT_Cond = 'Condition/C_'+str(primaryKey[0])+'_'+str(primaryKey[1])+'.json'

        fhirCond = func_dictCond(row)

        #id_res = sendRes(fhirCond,res)
        #record = [id_res,primaryKey[0],primaryKey[1]]
        #id_ress.append(record)

        printed_jsons += 1
        with open(OUT_Cond, 'w') as json_fileC:
            json_fileC.write(fhirCond)

    #pd.DataFrame(id_ress,columns=['ID','k1','k2']).to_csv('IDs/' + res + '_ids.csv',index=False)
    print("Printed jsons: ",printed_jsons)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start) 

##OBS
if obs_flag == 1:
    res = "Observation"
    print(f"{bcolors.WARNING}building Observations...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute("SELECT * FROM V_TER_CHEMIO_DA2022")
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_TER_CHEMIO_DA2022",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        df = pd.DataFrame()
        with open(IN_Obs) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    printed_jsons = 0
    num_its = 0
    id_ress = []
    for r in range(0,len(df.index)):
        row = df.iloc[r]
        num_its += 1
        
        primaryKey = [row.OBS_ID]

        OUT_Obs = 'Observation/O_'+str(primaryKey[0])+'.json'

        fhirObs = func_dictObs(row)

        #id_res = sendRes(fhirObs,res)
        record = [id_res,primaryKey[0]]
        id_ress.append(record)

        printed_jsons += 1
        with open(OUT_Obs, 'w') as json_fileO:
            json_fileO.write(fhirObs)

    pd.DataFrame(id_ress,columns=['ID','k1']).to_excel(res + '_ids.xlsx')
    print("Printed jsons: ",printed_jsons)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start)

##MedicationAdministration
if med_flag == 1:
    res = "MedicationAdministration"
    print(f"{bcolors.WARNING}building MedicationAdministration...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute("SELECT * FROM V_TER_CHEMIO_DA2022")
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_TER_CHEMIO_DA2022",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        df = pd.DataFrame()
        with open(IN_Med) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    printed_jsons = 0
    num_its = 0
    id_ress = []
    for r in range(0,len(df.index)):
        row = df.iloc[r]
        num_its += 1
        
        primaryKey = [row.OBS_ID]

        OUT_Med = 'MedicationAdm/M_'+str(primaryKey[0])+'.json'

        fhirMed = func_dictMed(row)

        #id_res = sendRes(fhirMed,res)
        record = [id_res,primaryKey[0]]
        id_ress.append(record)

        printed_jsons += 1
        with open(OUT_Med, 'w') as json_fileM:
            json_fileM.write(fhirMed)

    pd.DataFrame(id_ress,columns=['ID','k1']).to_excel(res + '_ids.xlsx')
    print("Printed jsons: ",printed_jsons)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start)

##Procedure
if procS_flag == 1:
    res = "Procedure"
    print(f"{bcolors.WARNING}building Procedure...{bcolors.ENDC}\n")
    start = timeit.default_timer() 
    if extraction == 1:
        c.execute("SELECT * FROM ")
        names = [col[0] for col in c.description]
        c.rowfactory = collections.namedtuple("V_INTERV_E_PROCED",names)
        df = pd.DataFrame(c)

    elif extraction == 2:
        df = pd.DataFrame()
        with open(IN_ProcS) as csvFile:
            csvReader = csv.DictReader(csvFile)
            df = pd.DataFrame(csvReader)

    printed_jsons = 0
    num_its = 0
    id_ress = []
    for r in range(0,2):
    #for r in range(0,len(df.index)):
        row = df.iloc[r]
        num_its += 1
        
        primaryKey = [row.INTERVENTO_ID,row.NOSOLOGICO]

        OUT_ProcS = 'Procedure/P_'+str(primaryKey[0])+'_'+str(primaryKey[1])+'.json'

        fhirProcS = func_dictProcSurg(row)

        id_res = sendRes(fhirProcS,res)
        record = [id_res,primaryKey[0],primaryKey[1]]
        id_ress.append(record)

        printed_jsons += 1
        with open(OUT_ProcS, 'w') as json_filePS:
            json_filePS.write(fhirProcS)

    pd.DataFrame(id_ress,columns=['ID','k1','k2']).to_excel(res + '_ids.xlsx')
    print("Printed jsons: ",printed_jsons)
    stop = timeit.default_timer()
    print('TIME SPENT: ', stop - start)

##
    if extraction == 1:
        conn.close()
