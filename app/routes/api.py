import json
from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User,Recommendation
from app.schemas import RegisterRequest,LoginRequest,TokenResponse,HomeRequest,PartyRequest,JewelryRequest,RecommendationDetail
from app.security import hash_password,verify_password,create_access_token
from app.services.recommendation_service import generate_home,generate_party,generate_jewelry
from app.config import get_settings
router=APIRouter(tags=['api'])
@router.get('/health')
def health(): return {'status':'ok','service':'PocketSmart AI'}
@router.post('/register',status_code=201)
def register(p:RegisterRequest,db:Session=Depends(get_db)):
    email=p.email.lower()
    if db.query(User).filter(User.email==email).first(): raise HTTPException(409,'Email is already registered')
    u=User(email=email,full_name=p.full_name.strip(),password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return {'message':'Registration successful','access_token':create_access_token(u.id),'token_type':'bearer'}
@router.post('/login',response_model=TokenResponse)
def login(p:LoginRequest,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==p.email.lower()).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
    return TokenResponse(access_token=create_access_token(u.id))
@router.post('/token',response_model=TokenResponse)
def token(p:LoginRequest,db:Session=Depends(get_db)): return login(p,db)
@router.post('/logout')
def logout(u:User=Depends(get_current_user)): return {'message':'Logout acknowledged. Remove the token from the browser/client.','user_id':u.id}
@router.get('/session-info')
def session_info(u:User=Depends(get_current_user)): return {'authenticated':True,'user_id':u.id,'email':u.email,'full_name':u.full_name}
@router.get('/session-data')
def session_data(u:User=Depends(get_current_user),db:Session=Depends(get_db)): return {'user_id':u.id,'recommendation_count':db.query(Recommendation).filter(Recommendation.user_id==u.id).count()}
@router.get('/history')
def history(u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(Recommendation).filter(Recommendation.user_id==u.id).order_by(Recommendation.created_at.desc()).limit(50).all()
    return [{'id':x.id,'planner_type':x.planner_type,'budget':x.budget,'created_at':x.created_at.isoformat(),'result':json.loads(x.result_json)} for x in rows]
@router.get('/recommendations-details/{rid}',response_model=RecommendationDetail)
def detail(rid:int,u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    x=db.query(Recommendation).filter(Recommendation.id==rid,Recommendation.user_id==u.id).first()
    if not x: raise HTTPException(404,'Recommendation not found')
    return RecommendationDetail(id=x.id,planner_type=x.planner_type,budget=x.budget,created_at=x.created_at.isoformat(),result=json.loads(x.result_json))
@router.post('/generate-home')
def home(r:HomeRequest,u:User=Depends(get_current_user),db:Session=Depends(get_db)): return generate_home(db,u,r)
@router.post('/generate-party')
def party(r:PartyRequest,u:User=Depends(get_current_user),db:Session=Depends(get_db)): return generate_party(db,u,r)
@router.post('/generate-jewelry')
async def jewelry(budget:int=Form(...),occasion:str=Form(...),style:str=Form('Elegant'),outfit_color:str=Form(''),description:str=Form(''),outfit_image:UploadFile|None=File(None),u:User=Depends(get_current_user),db:Session=Depends(get_db)):
    image=None; mime=None; s=get_settings()
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(400,'Only JPG, PNG, or WEBP images are supported')
        image=await outfit_image.read()
        if len(image)>s.max_image_size_mb*1024*1024: raise HTTPException(413,f'Image must be <= {s.max_image_size_mb} MB')
        mime=outfit_image.content_type
    r=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_color=outfit_color,description=description)
    return generate_jewelry(db,u,r,image,mime)
@router.get('/startup')
def startup():
    s=get_settings(); return {'status':'ready','gemini_configured':bool(s.gemini_api_key),'gemini_model':s.gemini_model}
