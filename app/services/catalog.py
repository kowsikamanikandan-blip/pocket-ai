from urllib.parse import quote_plus
PLATFORMS={'Amazon':'https://www.amazon.in/s?k={q}','Flipkart':'https://www.flipkart.com/search?q={q}','IKEA':'https://www.ikea.com/in/en/search/?q={q}','Swiggy':'https://www.swiggy.com/search?query={q}','Zomato':'https://www.zomato.com/search?q={q}','OYO':'https://www.oyorooms.com/search?location={q}'}
def search_url(platform,q): return PLATFORMS.get(platform,PLATFORMS['Amazon']).format(q=quote_plus(q))
def demo_catalog(planner,budget):
    data={'home':[('Living Room','LED ceiling light',1800,'Amazon'),('Living Room','Minimal wall art set',1400,'IKEA'),('Bedroom','Bedside lamp',1200,'IKEA'),('Kitchen','Storage organizer set',900,'Amazon'),('Dining','Table runner',700,'Flipkart')],'party':[('Catering','Mixed party meal package',450,'Swiggy'),('Catering','Snack platter',250,'Zomato'),('Decoration','Balloon decoration set',1800,'Amazon'),('Venue','Budget venue/stay search',2500,'OYO'),('Entertainment','Party game kit',900,'Amazon')],'jewelry':[('Earrings','Minimal statement earrings',900,'Amazon'),('Necklace','Elegant pendant necklace',1600,'Flipkart'),('Bangles','Classic bangle set',1200,'Amazon'),('Bracelet','Delicate bracelet',800,'Flipkart'),('Jewelry set','Occasion-ready jewelry set',2200,'Amazon')]}[planner]
    scale=max(.5,min(2.5,budget/8000)); out=[]
    for cat,name,price,platform in data:
        p=max(300,round(price*scale/100)*100); out.append({'category':cat,'name':name,'quantity':1,'estimated_price':p,'platform':platform,'reason':'Illustrative demo item selected for budget planning.','search_url':search_url(platform,name)})
    return out
def fit_to_budget(items,budget):
    out=[]; total=0
    for x in sorted(items,key=lambda z:z['estimated_price']):
        if total+x['estimated_price']<=budget: out.append(x); total+=x['estimated_price']
    if not out and items:
        x=min(items,key=lambda z:z['estimated_price']).copy(); x['estimated_price']=min(x['estimated_price'],budget); out=[x]
    return out
