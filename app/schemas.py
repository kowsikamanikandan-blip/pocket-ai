from typing import Literal
from pydantic import BaseModel,EmailStr,Field
PlannerType=Literal['home','party','jewelry']
class RegisterRequest(BaseModel): full_name:str=Field(min_length=2,max_length=120); email:EmailStr; password:str=Field(min_length=6,max_length=128)
class LoginRequest(BaseModel): email:EmailStr; password:str
class TokenResponse(BaseModel): access_token:str; token_type:str='bearer'
class HomeRequest(BaseModel): budget:int=Field(gt=0,le=10000000); rooms:list[str]=Field(min_length=1); items:list[dict]=[]; style:str='Modern'; location:str=''
class PartyRequest(BaseModel): budget:int=Field(gt=0,le=10000000); guests:int=Field(gt=0,le=10000); event_type:str=Field(min_length=2,max_length=80); venue:str='Any'; food_preference:str='Mixed'; location:str=''
class JewelryRequest(BaseModel): budget:int=Field(gt=0,le=10000000); occasion:str=Field(min_length=2,max_length=80); style:str='Elegant'; outfit_color:str=''; description:str=''
class Item(BaseModel): category:str; name:str; quantity:int=1; estimated_price:int; platform:str; reason:str; search_url:str
class RecommendationResult(BaseModel): planner_type:PlannerType; title:str; summary:str; budget:int; estimated_total:int; remaining_budget:int; budget_allocation:dict[str,int]={}; recommendations:list[Item]; tips:list[str]=[]; source_mode:Literal['gemini','demo']='demo'
class RecommendationDetail(BaseModel): id:int; planner_type:PlannerType; budget:int; created_at:str; result:RecommendationResult
