import os,tempfile
from pathlib import Path
db=Path(tempfile.gettempdir())/'pocketsmart_test.sqlite'; db.unlink(missing_ok=True)
os.environ['DATABASE_URL']=f'sqlite:///{db}'; os.environ['SECRET_KEY']='test-secret-key-123456'; os.environ['GEMINI_API_KEY']=''
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def headers():
 r=c.post('/register',json={'full_name':'Test User','email':'test@example.com','password':'password123'})
 if r.status_code==409:r=c.post('/login',json={'email':'test@example.com','password':'password123'})
 return {'Authorization':'Bearer '+r.json()['access_token']}
def test_health(): assert c.get('/health').json()['status']=='ok'
def test_session(): assert c.get('/session-info',headers=headers()).status_code==200
def test_home():
 r=c.post('/generate-home',headers=headers(),json={'budget':20000,'rooms':['Living Room'],'items':[],'style':'Modern','location':'Chennai'}); assert r.status_code==200 and r.json()['estimated_total']<=20000
def test_party():
 r=c.post('/generate-party',headers=headers(),json={'budget':30000,'guests':30,'event_type':'Birthday','venue':'Hall','food_preference':'Mixed','location':'Chennai'}); assert r.status_code==200
def test_jewelry():
 r=c.post('/generate-jewelry',headers=headers(),data={'budget':10000,'occasion':'Wedding','style':'Elegant','outfit_color':'Blue','description':'Simple'}); assert r.status_code==200
def test_history(): assert isinstance(c.get('/history',headers=headers()).json(),list)
