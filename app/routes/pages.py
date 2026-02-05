from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": current_user,
        "page_title": "Finology - Your Financial Superhero"
    })


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "user": None,
        "page_title": "Login - Finology"
    })


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "user": None,
        "page_title": "Sign Up - Finology"
    })


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user,
        "page_title": "Dashboard - Finology"
    })


@router.get("/calculator", response_class=HTMLResponse)
async def calculator_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("calculator.html", {
        "request": request,
        "user": current_user,
        "page_title": "Financial Calculators - Finology"
    })


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("about.html", {
        "request": request,
        "user": current_user,
        "page_title": "About Us - Finology"
    })


@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "user": current_user,
        "page_title": "Contact Us - Finology"
    })


@router.get("/learn", response_class=HTMLResponse)
async def learn_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("learn.html", {
        "request": request,
        "user": current_user,
        "page_title": "Learn Investing - Finology"
    })


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "user": current_user,
        "page_title": "AI Financial Assistant - Finology"
    })
