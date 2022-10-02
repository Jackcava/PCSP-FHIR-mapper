from pandas import read_csv

def retrieveCF(id):
    path = "/home/giaco/Scrivania/DOTTORATO/PCSP/CSVs/10Gen/V_ANAGRAFE_PAZIENTI_REAL.csv"
    df = read_csv(path)
    cf = df["A01_COD_FISCALE"][(int(id) == df["A01_ID_PERSONA"])]     #or df[df.eq(id).any(1)]["A01_COD_FISCALE"]
    return cf.values[0]

def retrieve_Cond(id):
    path1 = "/home/giaco/Scrivania/DOTTORATO/PCSP/CSVs/10Gen/V_ANAGRAFE_PAZIENTI_REAL.csv"
    path2 = "/home/giaco/Scrivania/DOTTORATO/PCSP/CSVs/10Gen/V_PAZIENTI_DIAGNOSI.csv"
    df1 = read_csv(path1,usecols=["A01_ID_PERSONA","A01_COD_FISCALE"])
    df2 = read_csv(path2,usecols=["ID_PAZIENTE","DT_REGISTRAZIONE","DESCR_DIAGNOSI"])
    pat = df1[df1.eq(id).any(1)]["A01_ID_PERSONA"]
    if len(pat) > 0:
        print("CP")
    # if list(pat) != []:
    #     print("cp")
    #pat = df1["A01_ID_PERSONA"][id == str(df1["A01_COD_FISCALE"])]
    cond = df2[df2.eq(str(pat.values[0])).any(1)][["ID_PAZIENTE","DT_REGISTRAZIONE","DESCR_DIAGNOSI"]]
    # if cond.shape[0] != 0:
    #     print("cp")
    return cond.values[0]

def retrieveID(id):
    pathFile = "/home/giaco/Scrivania/DOTTORATO/PCSP/map25Sept/IDs/Patient_ids.csv"
    df = read_csv(pathFile)
    row = df[[str(df.k1[0]) == id]]
    return str(row.ID[0])
    