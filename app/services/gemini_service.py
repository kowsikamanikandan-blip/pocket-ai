import json
from google import genai
from google.genai import types
from app.config import get_settings
SYSTEM="""You are PocketSmart AI, a budget-aware recommendation assistant. Return ONLY valid JSON. Never invent live prices, stock, ratings or reviews. Platform names are search destinations, not verified inventory sources. Schema: {"title":"","summary":"","estimated_total":0,"budget_allocation":{},"recommendations":[{"category":"","name":"","quantity":1,"estimated_price":0,"platform":"Amazon","reason":"","search_url":""}],"tips":[]}. Keep recommendations within the supplied budget."""
class GeminiService:
    def __init__(self):
        s=get_settings(); self.key=s.gemini_api_key.strip(); self.model=s.gemini_model; self.client=genai.Client(api_key=self.key) if self.key else None
    def generate(self,planner,payload,image_bytes=None,mime_type=None):
        if not self.client: raise RuntimeError('Gemini not configured')
        prompt=SYSTEM+'\nPlanner: '+planner+'\nInput: '+json.dumps(payload,ensure_ascii=False)+'\nReturn JSON only.'
        contents=[prompt]
        if image_bytes: contents.append(types.Part.from_bytes(data=image_bytes,mime_type=mime_type))
        r=self.client.models.generate_content(model=self.model,contents=contents,config=types.GenerateContentConfig(temperature=.4,max_output_tokens=4000))
        text=(r.text or '').strip().replace('```json','').replace('```','').strip(); return json.loads(text)
