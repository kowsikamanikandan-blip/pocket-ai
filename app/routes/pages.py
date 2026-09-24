from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router=APIRouter(tags=['pages']); templates=Jinja2Templates(directory='templates')
def page(name):
    def f(request:Request): return templates.TemplateResponse(name,{'request':request})
    return f
router.add_api_route('/',page('index.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/testimonials',page('testimonials.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/register',page('register.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/login',page('login.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/dashboard',page('dashboard.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/planner/home',page('home_planner.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/planner/party',page('party_planner.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/planner/jewelry',page('jewelry_planner.html'),methods=['GET'],response_class=HTMLResponse)
router.add_api_route('/history',page('history.html'),methods=['GET'],response_class=HTMLResponse)
