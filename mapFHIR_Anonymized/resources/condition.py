import pandas as pd
import numpy as np
from resources.retrieve import retrieveCF
from resources.retrieve import retrieveID
#from pprint import pprint
from datetime import date, datetime
from fhir.resources.condition import Condition
from fhir.resources.meta import Meta
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.extension import Extension
from fhir.resources.annotation import Annotation
from fhir.resources.backboneelement import BackboneElement

def func_dictCond(row):

    condition = Condition.construct()

    try:
        code = CodeableConcept()
        coding = Coding()
        coding.code = "NI"
        coding.system = "http://terminology.hl7.org/ValueSet/v3-ClassNullFlavor"
        code.coding = []
        code.coding.append(coding)
        condition.code = code
    except:
        pass

    try:
        patient_reference = Reference()
        patient_reference.reference = "Patient/" + retrieveID(row.ID_PAZIENTE)
        patient_reference.id = retrieveID(row.ID_PAZIENTE)
        condition.subject = patient_reference
    except:
        pass

    # try:
    #     encounter_reference = Reference()
    #     encounter_reference.reference = "Encounter/EncounterPrimCancerCineca"
    #     condition.encounter = encounter_reference
    # except:
    #     pass

    try:
        fhir_meta = Meta()
        fhir_meta.profile = []
        fhir_meta.profile.append("http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Condition-primaryCancer-eu-pcsp")
        condition.meta = fhir_meta
    except:
        pass

    try:
        bodySiteA = CodeableConcept()
        codingA = Coding()
        if row.TITOLO_LIV2 == "Sottosede":
            codingA.code = row.CODICE_LIV2
            codingA.system = "http://terminology.hl7.org/CodeSystem/icd-o-3"
        bodySiteA.coding = []
        bodySiteA.coding.append(codingA)
        condition.bodySite = [bodySiteA]
    except:
        pass

    try:
        Rec_date = row.DT_REGISTRAZIONE
        condition.recordedDate = str(Rec_date[:10])
    except:
        pass

    try:
        if row.TITOLO_LIV2 == "Istologia" or row.TITOLO_LIV2 == "Testo libero":
            noteA = Annotation(text=row.DESC_LIV2)
            condition.note = []
            condition.note.append(noteA)
    except:
        pass

    try:
        if row.TITOLO_LIV2 == "Stadio":
            stage = BackboneElement()
            summary = CodeableConcept()
            summary.text = row.CODICE_LIV2.split(" ")[-1]
            stage.extension = []
            stage.extension.append(summary)
            condition.stage = []
            condition.stage.append(stage)
    except:
        pass            
    
    return condition.json(indent=True)