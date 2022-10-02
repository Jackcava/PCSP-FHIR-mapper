import pandas as pd
from pprint import pprint
import numpy as np
from datetime import date, datetime
from fhir.resources.observation import Observation
from fhir.resources.meta import Meta
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.extension import Extension
from fhir.resources.quantity import Quantity
from fhir.resources.annotation import Annotation
from decimal import Decimal
from fhir.resources.period import Period

def func_dictObs(row):

    observation = Observation.construct()
    
    try:
        observation.status = "final"
    except:
        pass

    try:
        fhir_meta = Meta()
        fhir_meta.profile = []
        fhir_meta.profile.append("http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Observation-cumulativeDoseChemo-eu-pcsp")
        #fhir_meta.id = row.OBS_ID
        observation.meta = fhir_meta
    except:
        pass

    try:
        category_coding = Coding()
        category_coding.system = "http://terminology.hl7.org/CodeSystem/observation-category"
        category_coding.code = "laboratory"
        category_coding.display = "prova"
        observation.category = []
        observation.category.append(category_coding)
    except:
        pass

    try:
        patient_reference = Reference()
        if row.PAT_ID == "P1":
            patient_reference.reference = "Patient/7993" #2015005679 # + row.PAT_ID
            patient_reference.id = "7993" #2015005679 #row.PAT_ID
        elif row.PAT_ID == "P2":
            patient_reference.reference = "Patient/7996" # + row.PAT_ID
            patient_reference.id = "7996" #row.PAT_ID
        observation.subject = patient_reference
    except:
        pass

    # try:
    #     encounter_reference = Reference()
    #     encounter_reference.reference = "Encounter/" + row.ENCOUNTER_ID
    #     encounter_reference.id = row.ENCOUNTER_ID
    #     observation.encounter = encounter_reference
    # except:
    #     pass
    
    try:
        c_coding = Coding()
        c_coding.system = "http://hl7.eu/fhir/ig/pcsp/CodeSystem/cs-generic-eu-pcsp"
        c_coding.code = "cumulativeDose"
        code = CodeableConcept()
        code.coding = []
        code.coding.append(c_coding)
    except:
        pass

    try:
        ext = Extension()
        q = Quantity()
        q.value = float(row.FL_DOSE_EFF) / float(row.FL_SUPERFICIE)
        q.unit = row.CH15_UN_MIS
        q.system = "http://unitsofmeasure.org"
        q.code = "mg/mq"
        ext.valueQuantity = q
        observation.extension = []
        observation.extension.append(ext)
    except:
        pass

    try:
        str_datetime = row.DT_SOMM
        str_date = str_datetime.split(" ")[0]
        str_time = str_datetime.split(" ")[1]
        str_day = int(str_date.split("-")[2])
        str_month = int(str_date.split("-")[1])
        str_year = int(str_date.split("-")[0])
        effectiveDateTime = date(str_year, str_month, str_day)
        effectivePeriod = Period()
        effectivePeriod.start = effectiveDateTime
        effectivePeriod.end = effectiveDateTime
        observation.effectivePeriod = effectivePeriod
    except:
        pass

    return observation.json(indent=True)