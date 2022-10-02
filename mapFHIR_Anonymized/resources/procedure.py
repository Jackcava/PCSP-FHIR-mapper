from fhir.resources.procedure import Procedure
from fhir.resources.narrative import Narrative
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.location import Location
from fhir.resources.annotation import Annotation
from fhir.resources.meta import Meta

from resources.retrieve import retrieve_Cond
from datetime import date, datetime 

def func_dictProcSurg(row):

    try:
        data = {"status": "completed"}
    except:
        pass

    try:
        coding = Coding()
        coding.system = "http://snomed.info/sct"
        coding.code = 387713003
        coding.display = "Surgical procedure"
        categ = CodeableConcept()
        data["category"] = categ
    except:
        pass

    try:
        fhir_meta = Meta()
        fhir_meta.profile = []
        fhir_meta.profile.append("http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Procedure-surgery-eu-pcsp")
        data["meta"] = fhir_meta
    except:
        pass

    try:
        patient_reference = Reference()
        #patient_reference.reference = "Patient/" + row.A01_COD_FISCALE
        patient_reference.reference = "Patient/952"
        patient_reference.type = "Patient"
        data["subject"] = patient_reference
    except:
        pass

    try:
        reason_reference = Reference()
        cond = retrieve_Cond(row.A01_COD_FISCALE)
        reason_reference.reference = "Condition/" + cond[0] + "_" + cond[1]
        reason_reference.type = "Condition"
        data["reasonReference"] = [reason_reference]
    except:
        pass

    try:
        annot = Annotation.construct()
        annot.text = row.DESCRIZIONE
        data["note"] = []
        data["note"].append(annot)
    except:
        pass

    try:
        str_datetime = row.DATA_INTERVENTO
        str_date = str_datetime.split(" ")[0]
        str_time = str_datetime.split(" ")[1]
        str_day = int(str_date.split("-")[2])
        str_month = int(str_date.split("-")[1])
        str_year = int(str_date.split("-")[0])

        dateProc = (date(str_year, str_month, str_day))
        data["performedDateTime"] = dateProc
    except:
        pass

    try:
        procedureSurgery = Procedure(**data)
    except:
        pass
    
    return procedureSurgery.json(indent=True)
