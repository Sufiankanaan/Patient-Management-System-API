from fastapi import FastAPI ,Path,HTTPException,Query
from pydantic import BaseModel ,Field,field_validator,model_validator,computed_field, EmailStr
from typing import Optional,List,Annotated,Literal
from fastapi.responses import JSONResponse
import json
import pickle
import pandas as pd

app=FastAPI()

with open('model.pkl','rb') as f:
    model= pickle.load(f)
class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=130,description='age user')]
    weight: Annotated[float, Field(..., gt=0, description='weight')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='height')]
    income_lpa: Annotated[float, Field(..., gt=0, description=' Annual income')]
    smoker: Annotated[bool, Field(..., description='smoker')]
    city: Annotated[str, Field(..., description='city')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                   'business_owner', 'unemployed', 'private_job'],
                          Field(..., description='occupation')]

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi <= 18.5:
            return 'Underweight'
        elif self.bmi <= 25:
            return 'Normal'
        elif self.bmi <= 30:
            return 'Overweight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(gt=0,default=None)]
    weight: Annotated[Optional[float], Field(gt=0,default=None)]
    

def load_data():
    with open('Patients.json','r') as f :
        data = json.load(f)
    return data

def save_data(data):
    with open('Patients.json','w') as f :
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return{"message:A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples='P001')):
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sort_patient(sort_by:str = Query(...,description='Sort on the basis of height, weight or bmi'),
                 order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields =['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data=load_data()
    sort_order = (order == 'desc')
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_Update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    existing_patient_info=data[patient_id]
    existing_patient_info.update(patient_Update.model_dump(exclude_unset=True))

    existing_patient_info['id']=patient_id
    updated=Patient(**existing_patient_info).model_dump(exclude={'id'})

    data[patient_id]=updated
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient deleted'})

@app.post('/predict')
def predict_premium(data: UserInput):
    bmi = data.weight / (data.height ** 2)

    if data.age < 25:      age_group = "young"
    elif data.age < 45:    age_group = "adult"
    elif data.age < 60:    age_group = "middle_aged"
    else:                  age_group = "senior"

    if data.smoker and bmi > 30:    lifestyle_risk = "high"
    elif data.smoker or bmi > 27:   lifestyle_risk = "medium"
    else:                           lifestyle_risk = "low"

    tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
    tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Bhopal",
                     "Nagpur", "Surat", "Rajkot", "Mysore", "Guwahati", "Kota", "Noida", "Coimbatore"]
    if data.city in tier_1_cities:   city_tier = 1
    elif data.city in tier_2_cities: city_tier = 2
    else:                            city_tier = 3

    input_df = pd.DataFrame([{
        'age_group': age_group,
        'lifestyle_risk': lifestyle_risk,
        'city_tier': city_tier,
        'bmi': bmi,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return {'predicted_category': prediction}
