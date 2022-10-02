from datetime import date, datetime

from fhir.resources.condition import Condition
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.medicationadministration import MedicationAdministration
from fhir.resources.dosage import DosageDoseAndRate
from fhir.resources.dosage import Dosage
from fhir.resources.medicationadministration import MedicationAdministrationDosage
from fhir.resources.element import Element
from fhir.resources.quantity import Quantity
from fhir.resources.period import Period
from fhir.resources.meta import Meta
import pandas as pd


def func_dictMed(row):

    medication = MedicationAdministration.construct()

    try:
        # Create object and set the status field
        #data = {"status": "completed", "id": row.OBS_ID}
        data = {"status": "completed"}
    except:
        pass

    try:
        str_datetime = row.DT_SOMM
        str_date = str_datetime.split(" ")[0]
        str_time = str_datetime.split(" ")[1]
        str_day = int(str_date.split("-")[2])
        str_month = int(str_date.split("-")[1])
        str_year = int(str_date.split("-")[0])

        str_datetime_1 = row.DT_SOMM #???? We need a period but there isn't
        str_date_1 = str_datetime_1.split(" ")[0]
        str_time_1 = str_datetime_1.split(" ")[1]
        str_day_1 = int(str_date_1.split("-")[2])
        str_month_1 = int(str_date_1.split("-")[1])
        str_year_1 = int(str_date_1.split("-")[0])

        # condition.recordedDate = date(str_year, str_month, str_day)
        start = (date(str_year, str_month, str_day))
        end = (date(str_year_1, str_month_1, str_day_1))
        period = Period()
        period.start = start
        period.end = end
        data["effectivePeriod"] = period
    except:
        pass

    try:
        code_codeable = CodeableConcept()
        code_codeable.coding = []
        coding_value = Coding()

        coding_value.code = row.ATC
        coding_value.system = "http://www.whocc.no/atc"
        coding_value.display = row.FARMA_CHEMIO.lower()
        code_codeable.coding = [coding_value]
        data["medicationCodeableConcept"] = code_codeable
    except:
        pass

    try:
        fhir_meta = Meta()
        fhir_meta.profile = []
        fhir_meta.profile.append("http://hl7.eu/fhir/ig/pcsp/StructureDefinition/MedicationAdministration-eu-pcsp")
        data["meta"] = fhir_meta
    except:
        pass

    try:
        patient_reference = Reference()
        if row.PAT_ID == "P1":
            patient_reference.reference = "Patient/7993" #+ retrieve(row.PAT_ID) #N.B.: this PAT_ID is mock
            #patient_reference.id = "7993" #2015005679 #row.PAT_ID
        elif row.PAT_ID == "P2":
            patient_reference.reference = "Patient/7996" #+ retrieve(row.PAT_ID) 
            #patient_reference.id = "7996" #row.PAT_ID
        patient_reference.type = "Patient"
        data["subject"] = patient_reference
        #medication.subject = patient_reference
    except:
        pass

    dose = Quantity()
    dosage = MedicationAdministrationDosage()
    try:
        dose.value = float(row.FL_DOSE_EFF) / float(row.FL_SUPERFICIE)
        dose.unit = "mg/m2" #row.CH15_UN_MIS
        dose.system = "http://unitsofmeasure.org"
        dose.code = "mg/m2"
        dosage.dose = dose
        data["dosage"] = dosage
    except:
        pass
    
    try:
        reason_reference = Reference()
        if row.DIAG_ID == "D1":
            reason_reference.reference = "Condition/7994" #C_2015005679"
            #reason_reference.id = "7994"
        elif row.DIAG_ID == "D2":
            reason_reference.reference = "Condition/7997" #C_2015004849"
            #reason_reference.id = "7997"
        reason_reference.type = "Condition"
        data["reasonReference"] = [reason_reference]
    except:
        pass

    try:
        medicationAdministration = MedicationAdministration(**data)
    except:
        pass
    
    return medicationAdministration.json(indent=True)