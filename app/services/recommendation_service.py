import json
from sqlalchemy.orm import Session
from app.models import User,Recommendation
from app.schemas import HomeRequest,PartyRequest,JewelryRequest,RecommendationResult
from app.services.catalog import demo_catalog,fit_to_budget,search_url
from app.services.gemini_service import GeminiService
gemini=GeminiService()
def normalise(data,planner,budget):
    arr=[]
    for x in data.get('recommendations',[]):
        try: price=max(0,int(x.get('estimated_price',0))); qty=max(1,int(x.get('quantity',1)))
        except: continue
        name=str(x.get('name','Suggested item')); platform=str(x.get('platform','Amazon')); arr.append({'category':str(x.get('category','General')),'name':name,'quantity':qty,'estimated_price':price,'platform':platform,'reason':str(x.get('reason','Budget-aware suggestion.')),'search_url':str(x.get('search_url') or search_url(platform,name))})
    arr=fit_to_budget(arr,budget); total=sum(x['estimated_price']*x['quantity'] for x in arr)
    return RecommendationResult(planner_type=planner,title=str(data.get('title',planner.title()+' plan')),summary=str(data.get('summary','Budget-aware recommendations.')),budget=budget,estimated_total=total,remaining_budget=budget-total,budget_allocation={str(k):int(v) for k,v in data.get('budget_allocation',{}).items()},recommendations=arr,tips=[str(x) for x in data.get('tips',[])][:8],source_mode='gemini')
def demo(planner,budget,note):
    arr=fit_to_budget(demo_catalog(planner,budget),budget); total=sum(x['estimated_price'] for x in arr); alloc={}
    for x in arr: alloc[x['category']]=alloc.get(x['category'],0)+x['estimated_price']
    return RecommendationResult(planner_type=planner,title=planner.title()+' budget plan',summary=f'Demo recommendations within ₹{budget:,}. {note}',budget=budget,estimated_total=total,remaining_budget=budget-total,budget_allocation=alloc,recommendations=arr,tips=['Prices are illustrative demo estimates, not live quotes.','Open a platform search link to verify current price and availability.','Keep a small budget buffer for delivery, taxes and unexpected costs.'],source_mode='demo')
def save(db,user,planner,budget,payload,result):
    db.add(Recommendation(user_id=user.id,planner_type=planner,budget=budget,request_json=json.dumps(payload),result_json=result.model_dump_json())); db.commit()
def generate_home(db,user,r):
    try: out=normalise(gemini.generate('home',r.model_dump()),'home',r.budget)
    except Exception: out=demo('home',r.budget,'AI mode is unavailable or not configured.')
    save(db,user,'home',r.budget,r.model_dump(),out); return out
def generate_party(db,user,r):
    try: out=normalise(gemini.generate('party',r.model_dump()),'party',r.budget)
    except Exception: out=demo('party',r.budget,'AI mode is unavailable or not configured.')
    save(db,user,'party',r.budget,r.model_dump(),out); return out
def generate_jewelry(db,user,r,image=None,mime=None):
    try: out=normalise(gemini.generate('jewelry',r.model_dump(),image,mime),'jewelry',r.budget)
    except Exception: out=demo('jewelry',r.budget,'AI mode is unavailable or not configured.')
    save(db,user,'jewelry',r.budget,r.model_dump(),out); return out
