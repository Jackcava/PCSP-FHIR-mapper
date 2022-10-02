import pandas as pd
from pprint import pprint
import numpy as np
from datetime import date, datetime
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.meta import Meta
from fhir.resources.identifier import Identifier
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.extension import Extension
from fhir.resources.address import Address
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.backboneelement import BackboneElement

def func_dictPat(row):

    patient = Patient()

    try:
            patient.active = "true"
    except:
        pass

    try:
        human_name = []
        name = HumanName()
        name.use = "official"
        name.family = row.A01_COGNOME
        given = row.A01_NOME
        name.given = []
        name.given.append(given)
        human_name.append(name)
        patient.name = human_name
    except:
        pass

    try:
        fhir_meta = Meta()
        fhir_meta.profile = []
        fhir_meta.profile.append("http://hl7.eu/fhir/ig/pcsp/StructureDefinition/Patient-eu-pcsp")
        patient.meta = fhir_meta
    except:
        pass

    try:
        ids = []
        id1 = Identifier() #Oracle ID
        id1.value = row.A01_ID_PERSONA
        code = CodeableConcept()
        code.text = "Local DB ID"
        id1.type = code 
        ids.append(id1)
        id2 = Identifier() #FISCAL CODE
        id2.value = row.A01_COD_FISCALE 
        code = CodeableConcept()
        code.text = "FISCAL CODE"
        id2.type = code
        ids.append(id2)
        patient.identifier = []
        patient.identifier.append(ids)
    except:
        pass

    #if row.A01_ID_PERSONA == row.A01_COD_FISCALE:
    try:
        phone = ContactPoint()
        phone.system = "phone"
        phone.value = row.A02_NUM_TELEFONO1
        patient.telecom = []
        patient.telecom.append(phone)
    except:
        pass
    
    try:
        phone = ContactPoint()
        phone.system = "phone"
        phone.value = row.A02_NUM_TELEFONO2
        patient.telecom.append(phone)
    except:
        pass

    try:
        email = ContactPoint()
        email.system = "email"
        email.value = row.A02_EMAIL
        patient.telecom.append(email)
    except:
        pass

    try:
        if row.A01_SESSO.lower() == "m":
            gender = "male"
        elif row.A01_SESSO.lower() == "f":
            gender = "female"
        else:
            gender = "Unknown"
        patient.gender = gender
    except:
        pass

    try:
        birthdate = row.A01_DATA_NASCITA
        patient.birthDate = str(birthdate[:10])
    except:
        pass

    try:
        birth_place = Extension()
        birth_place.url = "http://hl7.org/fhir/StructureDefinition/patient-birthPlace"
        address = Address()
        address.city = row.A01_DESC_LUOGO_NASCITA
        address.text = row.A02_VIA_RESIDENZA
        birth_place.valueAddress = address
        patient.extension = birth_place
        print(patient)
    except:
        pass
    
    return patient.json(indent=True)