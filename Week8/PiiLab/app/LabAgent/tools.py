from langchain.tools import tool
from store import Appointments, Available_Dates
@tool
def lookup_appointment(appointment_id:str):
    """look up information regarding the patient's appointment according their appointment id
    Call this before determining details regarding the patient's appointment 
    """
    print(Appointments.get(str))
    appointment = Appointments.get(appointment_id)
    if appointment is not None:
        return appointment.items()


def reschedule_appointment(appointment_id,contact:str):
    "Provide the next available day for an appointment and inform the patient via email"
    return f"date: {Available_Dates[0],}, Email: {contact}"

TOOLS = [lookup_appointment,reschedule_appointment]