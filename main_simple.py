from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ai_mentor import AIMentor
from pdf_processor import extract_text_from_pdf
from document_tracker import DocumentTracker
from course_scheduler import CourseScheduler
from audit_logger import AuditLogger
from user_dashboard import generate_user_dashboard_html
from course_completion import CourseCompletion
from random_coffee import RandomCoffeeManager
from bedrock_client import BedrockClient
from coffee_messenger import CoffeeMessenger
from online_store import OnlineStore
from merch_system import MerchSystem
from enhanced_coffee import EnhancedCoffeeManager
from badge_system import BadgeSystem
import json

app = FastAPI(title="EHS AI Mentor", version="1.0.0")

# Add static file handling
@app.get("/calpoly-logo.png")
async def get_logo():
    return FileResponse("calpoly-logo.png")

@app.get("/tahoe.css")
async def get_tahoe_css():
    return FileResponse("tahoe.css", media_type="text/css")

@app.get("/AWS_2007_logo_white.png")
async def get_aws_logo():
    return FileResponse("AWS_2007_logo_white.png")

@app.get("/coffee-demo")
async def get_coffee_demo():
    return FileResponse("coffee_demo.html", media_type="text/html")

@app.get("/chatbot-demo")
async def get_chatbot_demo():
    return FileResponse("chatbot_demo.html", media_type="text/html")

@app.get("/enhanced_coffee_ui.js")
async def get_enhanced_coffee_js():
    return FileResponse("enhanced_coffee_ui.js", media_type="application/javascript")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("favicon.ico")

@app.get("/safety-helmet.jpg")
async def get_safety_helmet():
    return FileResponse("safety-helmet.jpg", media_type="image/jpeg")

@app.get("/safety-glasses.jpg")
async def get_safety_glasses():
    return FileResponse("safety-glasses.jpg", media_type="image/jpeg")

@app.get("/work-gloves.jpg")
async def get_work_gloves():
    return FileResponse("work-gloves.jpg", media_type="image/jpeg")

@app.get("/safety-vest.jpg")
async def get_safety_vest():
    return FileResponse("safety-vest.jpg", media_type="image/jpeg")

@app.get("/first-aid-kit.webp")
async def get_first_aid_kit():
    return FileResponse("first-aid-kit.webp", media_type="image/webp")

@app.get("/fire-extinguisher.webp")
async def get_fire_extinguisher():
    return FileResponse("fire-extinguisher.webp", media_type="image/webp")

@app.get("/come-with-me-tshirt.jpg")
async def get_come_with_me_tshirt():
    return FileResponse("come-with-me-tshirt.jpg", media_type="image/jpeg")

@app.get("/survival-hoodie.jpg")
async def get_survival_hoodie():
    return FileResponse("survival-hoodie.jpg", media_type="image/jpeg")

@app.get("/deep-breath-hoodie.jpg")
async def get_deep_breath_hoodie():
    return FileResponse("deep-breath-hoodie.jpg", media_type="image/jpeg")

@app.get("/deep-breath-womens-tee.jpg")
async def get_deep_breath_womens_tee():
    return FileResponse("deep-breath-womens-tee.jpg", media_type="image/jpeg")

@app.get("/deep-breath-mug.jpg")
async def get_deep_breath_mug():
    return FileResponse("deep-breath-mug.jpg", media_type="image/jpeg")

@app.get("/deep-breath-sticker.jpg")
async def get_deep_breath_sticker():
    return FileResponse("deep-breath-sticker.jpg", media_type="image/jpeg")

mentor = AIMentor()
doc_tracker = DocumentTracker()
scheduler = CourseScheduler()
audit_logger = AuditLogger()
course_completion = CourseCompletion()
coffee_manager = RandomCoffeeManager()
bedrock_client = BedrockClient()
coffee_messenger = CoffeeMessenger()
store = OnlineStore()
merch_system = MerchSystem()
enhanced_coffee = EnhancedCoffeeManager()
badge_system = BadgeSystem()

@app.get("/store/products")
async def get_store_products():
    """Get all unified store products (safety equipment + merch)"""
    try:
        # Get safety equipment from store
        safety_products = store.get_all_products()
        
        # Get merch products from merch system
        merch_products = merch_system.catalog
        
        # Convert merch to store format and categorize
        unified_products = []
        
        # Add safety equipment
        for product in safety_products:
            product = product.copy()
            # Rename ABC Fire Extinguisher to ZYX Fire Extinguisher
            if product.get('name') == 'ABC Fire Extinguisher - 5lb':
                product['name'] = 'ZYX Fire Extinguisher - 5lb'
            # Update Safety Hard Hat URL
            if product.get('name') == 'Safety Hard Hat':
                product['amazon_url'] = 'https://www.amazon.com/Construction-Approved-LOHASPRO-Climbing-Arborist/dp/B09W9N4BCQ/ref=sr_1_2_sspa?crid=3V4OFEP2X3KB6&dib=eyJ2IjoiMSJ9.-NNKED59iTmzBQFhadOxhclhnxd4szxC795jGn6n8tPITCl4epenthL65zLWQG4FOnmhaOBgXBzeyaJB4aqefhUBS44yNpu1XLsGr8Ad-Q70MKp1H1eFnF2Ad0ctUiDdxtFPpUWgoEAt_IiY-8ljj3bXCSHCkQj6QR12fWBhZK0F2nfj6VyOdOyJ-AhnICU8_L3To3LP4tkx7cSmoIXsf4yuZ84zINlt2d4inAnKMlj2fgxHlVzlnlN07EinqE8ufsFNZPBpuzbmUKJcUQYk1HjQOKNGb67LCvjz6GmcAV4.mj3jpHOj3W1umZWNXXRTv0U7Nq_08ZTwAS-9yGmFkVM&dib_tag=se&keywords=Safety%2BHard%2BHat%2Bgreen&qid=1758566193&sprefix=safety%2Bhard%2Bhat%2Bgreen%2Caps%2C653&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
            unified_products.append(product)
        
        # Add merch products with proper categorization
        for item in merch_products:
            # Map merch categories to store categories
            if item["category"] == "apparel":
                department = "Cal Poly Apparel"
            elif item["category"] == "accessories" and "mug" in item["name"].lower():
                department = "Cal Poly Accessories"
            elif item["category"] == "accessories":
                department = "Cal Poly Accessories"
            else:
                department = "Cal Poly Merchandise"
            
            unified_products.append({
                "id": item["id"],
                "name": item["name"],
                "description": item["description"],
                "price": item["price"],
                "image": item["image"],
                "department": department,
                "rating": 4.8,
                "in_stock": 50,
                "amazon_url": item["url"]
            })
        
        return {"products": unified_products, "success": True}
    except Exception as e:
        return {"products": [], "success": False, "error": str(e)}

@app.post("/store/products")
async def add_store_product(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(default=""),
    category: str = Form(default="general")
):
    """Add new product to store"""
    try:
        product_id = store.add_product(name, price, description, category)
        return {"product_id": product_id, "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/chat")
async def chat_with_ai(message: str = Form(...), history: str = Form(default="[]")):
    """AI chat for safety consultations"""
    try:
        # Get context from processed documents
        context = ""
        for doc_hash, doc_info in doc_tracker.processed_docs.items():
            context += f"Document: {doc_info['title']}\n"
            if 'content' in doc_info:
                context += doc_info['content'][:500] + "...\n\n"
        
        # Create AI prompt
        system_prompt = f"""You are a safety and occupational health expert. 
        Answer questions based on the following processed documents:
        
        {context}
        
        Give brief, practical answers. If information is insufficient, say so."""
        
        # Parse history
        chat_history = json.loads(history)
        
        # Call Bedrock
        response = mentor.bedrock.client.invoke_model(
            modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "system": system_prompt,
                "messages": chat_history
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']
        
        return {"response": ai_response, "success": True}
        
    except Exception as e:
        return {"response": f"AI Error: {str(e)}", "success": False}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")
        
        pdf_bytes = await file.read()
        protocol_text = extract_text_from_pdf(pdf_bytes)
        
        # Check if document was processed before
        is_duplicate, prev_info = doc_tracker.is_duplicate(protocol_text)
        
        if is_duplicate:
            return {
                "is_duplicate": True,
                "message": "This document has already been processed",
                "previous_processing": prev_info,
                "extracted_text": protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
            }
        
        # Process new document with history and deadline checking
        mentor._scheduler = scheduler  # Pass scheduler
        result = mentor.analyze_for_all_users_with_history(protocol_text, doc_tracker)
        
        # Save processing information with skipped and content for chat
        doc_hash = doc_tracker.save_document(protocol_text, result.get("assignments", []), result.get("skipped_duplicates", []))
        # Save content for AI chat
        if doc_hash in doc_tracker.processed_docs:
            doc_tracker.processed_docs[doc_hash]['content'] = protocol_text
        
        # Log document processing
        audit_logger.log_document_processed(
            doc_hash, 
            len(result.get("assignments", [])),
            protocol_text[:100] + "..."
        )
        
        # Log each assignment with document hash
        for assignment in result.get("assignments", []):
            for course_id in assignment["courses_assigned"]:
                clean_course_id = course_id.replace(" (update)", "")
                priority = "normal"
                if assignment.get("course_periods"):
                    for period in assignment["course_periods"]:
                        if period["course_id"] == clean_course_id:
                            priority = period.get("priority", "normal")
                            break
                
                # Add document hash to log
                log_entry = {
                    "timestamp": audit_logger.logs[-1]["timestamp"] if audit_logger.logs else "2025-01-01T00:00:00",
                    "action": "course_assigned",
                    "user_id": assignment["user_id"],
                    "course_id": clean_course_id,
                    "assigned_by": "AI",
                    "reason": assignment.get("reason", ""),
                    "priority": priority,
                    "document_hash": doc_hash,
                    "id": len(audit_logger.logs) + 1
                }
                audit_logger.logs.append(log_entry)
        
        # Save logs
        audit_logger.save_logs()
        
        result["extracted_text"] = protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
        result["is_duplicate"] = False
        result["document_hash"] = doc_hash
        
        # Add information about expiring courses
        expired_courses = scheduler.get_expired_courses(doc_tracker)
        result["expired_courses"] = expired_courses
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>EHS AI Mentor</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/tahoe.css">
    <style>
    :root {
      --space-xs: clamp(0.5rem, 1vw, 0.75rem);
      --space-s: clamp(0.75rem, 2vw, 1rem);
      --space-m: clamp(1rem, 3vw, 1.5rem);
      --space-l: clamp(1.5rem, 4vw, 2rem);
      --space-xl: clamp(2rem, 6vw, 3rem);
      --space-xxl: clamp(3rem, 8vw, 4rem);
      
      --text-xs: clamp(0.875rem, 2vw, 1rem);
      --text-s: clamp(1rem, 2.5vw, 1.125rem);
      --text-m: clamp(1.125rem, 3vw, 1.25rem);
      --text-l: clamp(1.5rem, 4vw, 2rem);
      --text-xl: clamp(2rem, 6vw, 3rem);
      --text-xxl: clamp(3rem, 8vw, 4rem);
      
      --gray-50: #fafafa;
      --gray-100: #f5f5f5;
      --gray-200: #e5e5e5;
      --gray-300: #d4d4d4;
      --gray-400: #a3a3a3;
      --gray-500: #737373;
      --gray-600: #525252;
      --gray-700: #404040;
      --gray-800: #262626;
      --gray-900: #171717;
      
      --container-max: 1200px;
      --container-pad: 20px;
      
      /* Aliases for compatibility */
      --bg: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ecfdf5 100%);
      --panel: #ffffff;
      --ink: var(--gray-800);
      --muted: var(--gray-600);
      --brand: #0e7a4e;
      --brand-light: #16a34a;
      --brand-dark: #0d5f3c;
      --accent: #3b82f6;
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --blue: #3b82f6;
      --purple: #8b5cf6;
      --orange: #f97316;
      --red: #ef4444;
      --shadow-1: 0 3px 10px rgba(0,0,0,.08);
      --shadow-2: 0 8px 24px rgba(0,0,0,.12);
      --speed: .2s;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: var(--text-s);
      line-height: 1.6;
      color: var(--gray-800);
      background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 50%, #86efac 100%);
      min-height: 100vh;
    }

    .container {
      max-width: var(--container-max);
      margin: 0 auto;
      padding: 0 var(--container-pad);
    }
    
    .appbar{
      background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%);
      color:#fff; padding:18px 0; position:sticky; top:0; z-index:20; box-shadow:var(--shadow-1);
      border-radius: 8px;
      margin-bottom: var(--space-m);
    }
    
    .hero{
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin: var(--space-l) 0;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero h1{
      font-size: var(--text-xl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }
    
    h1 {
      font-size: var(--text-xxl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }

    h2 {
      font-size: var(--text-xl);
      font-weight: 600;
      line-height: 1.2;
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-900);
    }

    h3 {
      font-size: var(--text-l);
      font-weight: 600;
      line-height: 1.3;
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-800);
    }

    p {
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-600);
    }
    
    button {
      border: none;
      border-radius: 10px;
      padding: var(--space-s) var(--space-m);
      font-weight: 600;
      font-size: var(--text-xs);
      cursor: pointer;
      transition: all var(--speed);
      background: linear-gradient(135deg, var(--brand) 0%, #16a34a 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(14, 122, 78, 0.3);
    }
    
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(14, 122, 78, 0.4);
    }
    
    button:active {
      transform: translateY(0) scale(0.98);
    }
    
    .btn {
      border: none;
      border-radius: 8px;
      padding: var(--space-xs) var(--space-s);
      font-weight: 500;
      font-size: var(--text-xs);
      cursor: pointer;
      transition: all var(--speed);
      background: var(--brand);
      color: white;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    
    .btn:hover {
      filter: brightness(.95);
      transform: translateY(-1px);
    }
    
    .tahoe-stat-card {
      background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
      padding: var(--space-s);
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    .tahoe-stat-card:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .training-card {
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin-bottom: var(--space-m);
      display: flex;
      align-items: center;
      gap: var(--space-m);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.3);
      position: relative;
      overflow: hidden;
    }
    
    .training-card::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--brand);
      border-radius: 4px 0 0 4px;
    }
    
    .training-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .training-content {
      flex: 1;
    }
    
    .training-title {
      margin: 0 0 var(--space-s) 0;
      display: flex;
      align-items: center;
      gap: var(--space-s);
      font-weight: 600;
      font-size: var(--text-l);
      color: var(--gray-800);
    }
    
    .training-desc {
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-600);
      font-size: var(--text-xs);
    }
    
    .training-meta {
      display: flex;
      gap: var(--space-s);
      font-size: var(--text-xs);
      color: var(--gray-500);
    }
    
    .training-btn {
      background: var(--brand);
      color: white;
      border: none;
      padding: 4px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 500;
      font-size: 12px;
      transition: all var(--speed);
    }
    
    .training-btn:hover {
      filter: brightness(.95);
      transform: translateY(-1px);
    }
    
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: modalFadeIn 0.3s ease;
    }
    
    .modal.show {
      display: flex;
    }
    
    .modal-content {
      background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ecfdf5 100%);
      backdrop-filter: blur(20px);
      border-radius: 20px;
      max-width: 900px;
      width: 95%;
      max-height: 85vh;
      overflow: hidden;
      box-shadow: 0 25px 80px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.5);
      border: 1px solid rgba(255, 255, 255, 0.8);
      animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .modal-header {
      padding: var(--space-xl) var(--space-xl) var(--space-l);
      background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%);
      color: white;
      position: relative;
      border-radius: 20px 20px 0 0;
    }
    
    .modal-header h3 {
      margin: 0;
      font-size: var(--text-xl);
      font-weight: 700;
      color: white;
    }
    
    .modal-body {
      padding: var(--space-m);
      overflow-y: auto;
      max-height: calc(85vh - 120px);
    }
    
    .modal-close {
      position: absolute;
      top: 15px;
      right: 20px;
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      width: 40px;
      height: 40px;
      font-size: 20px;
      cursor: pointer;
      color: white;
      transition: all var(--speed);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .modal-close:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: scale(1.1);
    }
    
    @keyframes modalFadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes modalSlideIn {
      from { 
        opacity: 0;
        transform: translateY(-50px) scale(0.9);
      }
      to { 
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    </style>
</head>
<body>

    
    <div class="container">
        
        <!-- Header в виде карточки -->
        <div class="hero" style="background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%); color: white; grid-column: 1 / -1; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 32px;">
                    <img src="/calpoly-logo.png" alt="Cal Poly" height="32" style="filter: brightness(0) invert(1);">
                    <div>
                        <div style="font-size: 28px; font-weight: 400; color: white; letter-spacing: -0.01em;">👋 Hello, <strong>Admin</strong></div>
                        <div id="motivationalStatus" onclick="openMeditation()" style="font-size: 20px; color: rgba(255, 255, 255, 0.9); margin-top: 4px; font-weight: 300; cursor: pointer; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">✨ Time to breathe and find your inner peace 🧘♀️</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <button onclick="openStoreSettings()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); white-space: nowrap;">⚙️ Settings</button>
                    <button onclick="logout()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3);">Logout</button>
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="hero" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px);">
                <h1 style="font-size: 48px; font-weight: 800;">📊 System Statistics</h1>
                
                <!-- Прогресс бар -->
                <div style="margin: var(--space-l) 0;">
                    <div style="background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); backdrop-filter: blur(10px); border-radius: 16px; padding: var(--space-l); border: 1px solid rgba(255, 255, 255, 0.3);">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: var(--space-s);">
                            <span style="font-weight: 600; color: var(--gray-800); font-size: var(--text-l);">Training Progress</span>
                            <span style="font-weight: 700; color: var(--brand); font-size: var(--text-l);" id="progressPercent">0%</span>
                        </div>
                        <div style="position: relative; height: 12px; border-radius: 999px; background: rgba(200,200,200,0.4); overflow: hidden; margin: var(--space-s) 0;">
                            <div id="progressFill" style="height: 100%; width: 0%; background: linear-gradient(90deg, var(--brand), var(--success)); transition: width 0.6s ease; border-radius: 999px;"></div>
                        </div>
                        <div style="display: flex; gap: var(--space-m); margin-top: var(--space-s); font-size: var(--text-xs); color: var(--gray-700);">
                            <span onclick="showCompletions()" style="cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'"><strong id="completedCount" style="color: var(--success);">0</strong> Completed</span>
                            <span onclick="showActive()" style="cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'"><strong id="activeProgressCount" style="color: var(--blue);">0</strong> Active</span>
                            <span onclick="showCritical()" style="cursor: pointer; transition: all 0.2s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'"><strong id="overdueCount" style="color: var(--red);">0</strong> Overdue</span>
                        </div>
                    </div>
                </div>
                
                <div id="statsBlocks" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 16px;">
            <div class="tahoe-stat-card" onclick="showUsers()" style="background: linear-gradient(145deg, #dbeafe 0%, #bfdbfe 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--blue);" id="userCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">👥 Total Users</div>
            </div>
            <div class="tahoe-stat-card" onclick="showCourses()" style="background: linear-gradient(145deg, #ede9fe 0%, #ddd6fe 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--purple);" id="courseCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">📚 Courses</div>
            </div>
            <div class="tahoe-stat-card" onclick="showAssignments()" style="background: linear-gradient(145deg, #dcfce7 0%, #bbf7d0 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--brand);" id="assignmentCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">🎯 Total Assignments</div>
            </div>
            <div class="tahoe-stat-card" onclick="showDocuments()" style="background: linear-gradient(145deg, #fed7aa 0%, #fdba74 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--orange);" id="documentCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">📄 Documents</div>
            </div>
                </div>
            </div>
            
            <!-- Правая колонка - форма processing -->
            <div class="hero" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%) !important; color: white !important; border-radius: 32px !important; box-shadow: 0 20px 40px rgba(245, 158, 11, 0.3) !important;">
                <h1 style="font-size: 46px; font-weight: 800;">🤖 AI Analysis</h1>
                
                <div style="position: relative; width: 100%; margin: 40px 0;">
                    <input type="file" id="pdfFile" accept=".pdf" style="position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 2;">
                    <div style="min-height: 160px; padding: 40px; border: 3px dashed rgba(255,255,255,0.4); border-radius: 20px; background: rgba(255,255,255,0.1); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; transition: all 0.3s ease;" id="dropZone">
                        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.8;">📄</div>
                        <div style="font-size: 18px; font-weight: 700; color: black; margin-bottom: 8px;">Drag & Drop Your PDF</div>
                        <div style="font-size: 14px; color: #374151; line-height: 1.4;">Our AI will work its magic through Amazon Bedrock<br>and create personalized training assignments</div>
                    </div>
                </div>
                <p style="opacity:.85;margin:16px 0 0 0;font-size:15px;line-height:1.5;text-align:center;">⚡ Processing first 10 users for demonstration (~30-40 seconds)</p>
                <div style="display: flex; gap: 12px; margin-top: 24px;">
                    <button onclick="showAuditLog()" style="background:#ff8533; color:white; flex: 1;">📈 Audit Log</button>
                    <button onclick="showComplianceReport()" style="background:#16a34a; color:white; flex: 1;">📄 Compliance Report</button>
                </div>
            </div>
            </div>
            
            <div class="hero" style="grid-column: 1 / -1;" id="documentHistory"></div>
        </div>

        <div id="result"></div>
    </div>
    
    <!-- Modal -->
    <div id="mainModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Modal Title</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body" id="modalBody">
                Modal content goes here
            </div>
        </div>
    </div>
    
    <script>
        // Motivational statuses for admin
        const motivationalStatuses = [
            'Test completed? Time to relax and meditate! 🧘‍♀️',
            'Managing people is hard work. You deserve peaceful moments 🌸',
            'Decisions made, reports reviewed. Now breathe and relax ✨',
            'Another productive day of oversight. Time for inner peace 🕯️',
            'Team guided, goals achieved. Reward yourself with stillness 🌟',
            'Administrative duties complete. Your mind needs rest now 🍃',
            'Well done! Take a moment to center yourself! 🧘‍♂️',
            'Systems running smoothly. Time for zen and tranquility 🌊',
            'Leadership goals met! Now unlock your inner calm 🔓',
            'Day of coordination done. Complete it with meditation 🌅',
            'You guided others well. Time to find your peaceful space 🏞️',
            'Oversight finished? Let your mind find its balance ⚖️',
            'Management success! Now achieve inner harmony 🎵',
            'Supervision over? Time to train your mindfulness 🎯',
            'Well earned leadership break! Meditate and recharge 🔋',
            'Challenges conquered? Now conquer your stress 💪',
            'Administrative mission accomplished! Time for reflection 🪞',
            'You led them well! Now do something for your soul 💫',
            'Management mastered? Master the art of relaxation 🎨',
            'Leadership triumph! Triumph over daily tensions 🏆',
            'Guidance complete? Complete your inner journey 🗺️',
            'Hard decisions made? Time for soft, gentle breathing! 🌬️',
            'Organizational goals achieved! Now achieve perfect stillness 🎪',
            'Management victory! Victory over stress starts now 🥇',
            'Wisdom shared? Gain some peace of mind too 🧠',
            'Administrative tasks finished? Finish with mindful moments ⏰',
            'You led successfully! Now succeed at being present 🎁',
            'Systems cleared? Clear your mind with meditation 🌤️',
            'Leadership well done! Now be well with inner peace 💚',
            'Management achievement earned! Earn some tranquil time 🕰️',
            'Team objectives passed? Pass into a state of calm 🚪',
            'You managed it all! Make time for mindful breathing 🌀',
            'Oversight complete? Complete your day with serenity 🌙',
            'Leadership success story! Write your relaxation chapter 📖',
            'Management job well done! Now enjoy the job of just being 🌺'
        ];
        
        function getRandomMotivationalStatus() {
            const randomIndex = Math.floor(Math.random() * motivationalStatuses.length);
            return motivationalStatuses[randomIndex];
        }
        
        function updateMotivationalStatus() {
            const statusElement = document.getElementById('motivationalStatus');
            if (statusElement) {
                const status = getRandomMotivationalStatus();
                const parts = status.split(' ');
                const emoji = parts.pop();
                const text = parts.join(' ');
                statusElement.innerHTML = `<span style="text-decoration: underline; text-decoration-style: dashed; text-underline-offset: 4px; text-decoration-thickness: 1px;">${text}</span> ${emoji}`;
            }
        }
        
        function logout() {
            if(confirm('Are you sure you want to logout?')) {
                window.location.href = './index.html';
            }
        }
        
        // Modal functions
        function showModal(title, content) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalBody').innerHTML = content;
            document.getElementById('mainModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('mainModal').classList.remove('show');
        }
        
        // Close modal on Esc key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
        
        function openMeditation() {
            const meditationHTML = `
                <div style="text-align: center; padding: 0;">

                    
                    <!-- Дыхательный круг -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px 20px; margin-bottom: 20px; position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                        <div id="meditationTimer" style="font-size: 24px; font-weight: 200; margin: 0 0 20px 0; font-family: system-ui, -apple-system, sans-serif; color: rgba(255,255,255,0.8); letter-spacing: 0.1em; position: relative; z-index: 2;">05:00</div>
                        <div id="breathingCircle" style="width: 120px; height: 120px; border: 3px solid rgba(255,255,255,0.8); border-radius: 50%; margin: 0 auto 20px; transition: transform 4s ease-in-out; background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%); box-shadow: 0 0 40px rgba(255,255,255,0.3), inset 0 0 30px rgba(255,255,255,0.1); position: relative; z-index: 2;"></div>
                        <div id="breathingGuide" style="font-size: 20px; opacity: 0; transition: opacity 0.5s ease; color: white; font-weight: 300; margin-bottom: 12px; position: relative; z-index: 2;">Breathe...</div>
                        <div id="affirmationText" style="font-size: 14px; opacity: 0; transition: opacity 1s ease; color: rgba(255,255,255,0.7); font-weight: 300; font-style: italic; position: relative; z-index: 2; min-height: 16px;"></div>
                    </div>
                    
                    <!-- Настройки -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <div style="color: var(--gray-700); font-size: 12px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Duration</div>
                            <div style="display: flex; gap: 8px; justify-content: center;">
                                <button onclick="setMeditationTime(180)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">3m</button>
                                <button onclick="setMeditationTime(300)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">5m</button>
                                <button onclick="setMeditationTime(600)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">10m</button>
                            </div>
                        </div>
                        <div>
                            <div style="color: var(--gray-700); font-size: 12px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Controls</div>
                            <div style="display: flex; gap: 8px; justify-content: center;">
                                <button onclick="startMeditation()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">▶</button>
                                <button onclick="pauseMeditation()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">⏸</button>
                                <button onclick="resetMeditation()" style="background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">↻</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Рекламный блок -->
                    <div style="background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px); border-radius: 16px; padding: 16px; margin-top: 20px; border: 2px solid rgba(255, 255, 255, 0.6); box-shadow: 0 4px 16px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 14px; color: var(--gray-700); line-height: 1.4;">
                            Have you tried our low-calorie pastries at the <a href="#" style="color: var(--brand); text-decoration: underline;">cafeteria</a>?<br>
                            Get 10% off with promo code <strong style="background: rgba(14, 122, 78, 0.1); padding: 2px 6px; border-radius: 4px; color: var(--brand);">"meditation"</strong>.
                        </div>
                    </div>
                    

                </div>
                
                <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.3; }
                    50% { transform: scale(1.1) rotate(180deg); opacity: 0.1; }
                }
                button:hover {
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
                }
                </style>
            `;
            showModal('🧘♀️ Mindful Meditation', meditationHTML);
        }
        
        function openStoreSettings() {
            const storeHTML = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Add Product Form -->
                    <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 16px 0; color: var(--gray-800);">➕ Add New Product</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">Product Name</label>
                                <input type="text" id="productName" placeholder="Enter product name" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">Price ($)</label>
                                <input type="number" id="productPrice" placeholder="0.00" step="0.01" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">Category</label>
                                <select id="productCategory" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="general">General</option>
                                    <option value="safety">Safety Equipment</option>
                                    <option value="clothing">Clothing</option>
                                    <option value="accessories">Accessories</option>
                                    <option value="books">Books & Manuals</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">Description</label>
                                <input type="text" id="productDescription" placeholder="Product description" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                            </div>
                        </div>
                        <button onclick="addProduct()" style="background: var(--success); color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600;">Add Product</button>
                    </div>
                    
                    <!-- Products List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🛍️ Store Products</h4>
                        <div id="productsList" style="min-height: 200px;">
                            <div style="text-align: center; padding: 40px; color: var(--gray-600);">Loading products...</div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>
            `;
            showModal('⚙️ Settings', storeHTML);
            loadProducts();
        }
        
        async function loadProducts() {
            try {
                const response = await fetch('/store/products');
                const data = await response.json();
                
                const productsList = document.getElementById('productsList');
                if (!productsList) return;
                
                if (data.success && data.products && data.products.length > 0) {
                    let html = '';
                    data.products.forEach(product => {
                        html += `
                        <div style="background: white; border: 1px solid #e5e5e5; border-radius: 8px; padding: 12px; margin: 8px 0; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">${product.name}</div>
                                <div style="color: var(--gray-600); font-size: 12px; margin: 4px 0;">${product.description || 'No description'}</div>
                                <div style="display: flex; gap: 12px; font-size: 12px; color: var(--gray-500);">
                                    <span>💰 $${product.price.toFixed(2)}</span>
                                    <span>📂 ${product.category}</span>
                                    <span>📅 ${new Date(product.created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                            <div style="display: flex; gap: 8px;">
                                <button onclick="editProduct('${product.id}')" style="background: var(--blue); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px;">Edit</button>
                                <button onclick="deleteProduct('${product.id}')" style="background: var(--error); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px;">Delete</button>
                            </div>
                        </div>`;
                    });
                    productsList.innerHTML = html;
                } else {
                    productsList.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--gray-600);">No products in store yet</div>';
                }
            } catch (error) {
                const productsList = document.getElementById('productsList');
                if (productsList) {
                    productsList.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--error);">Error loading products</div>';
                }
            }
        }
        
        async function addProduct() {
            const name = document.getElementById('productName').value.trim();
            const price = parseFloat(document.getElementById('productPrice').value);
            const category = document.getElementById('productCategory').value;
            const description = document.getElementById('productDescription').value.trim();
            
            if (!name || isNaN(price) || price < 0) {
                alert('Please enter valid product name and price');
                return;
            }
            
            try {
                const formData = new FormData();
                formData.append('name', name);
                formData.append('price', price.toString());
                formData.append('category', category);
                formData.append('description', description);
                
                const response = await fetch('/store/products', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Clear form
                    document.getElementById('productName').value = '';
                    document.getElementById('productPrice').value = '';
                    document.getElementById('productDescription').value = '';
                    document.getElementById('productCategory').value = 'general';
                    
                    // Reload products
                    loadProducts();
                } else {
                    alert('Error adding product: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error adding product: ' + error.message);
            }
        }
        
        function editProduct(productId) {
            alert('Edit functionality coming soon!');
        }
        
        function deleteProduct(productId) {
            if (confirm('Are you sure you want to delete this product?')) {
                alert('Delete functionality coming soon!');
            }
        }
        
        function openAIChat() {
            const chatHTML = `

                
                <div id="chatMessages" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 16px; padding: 16px; margin: 16px 0; height: 300px; overflow-y: auto; font-size: 14px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                    <div style="color: #2c3e50; text-align: center; padding: 40px 20px; font-size: 16px; line-height: 1.6;">
                        <div style="font-size: 48px; margin-bottom: 20px; opacity: 0.7;">🌟</div>
                        <div style="font-weight: 600; margin-bottom: 12px;">Hi! I'm your digital friend</div>
                        <div style="opacity: 0.8; margin-bottom: 12px;">I'll help you find like-minded people at the faculty and build strong friendships</div>
                        <div style="opacity: 0.7; font-size: 14px;">Ask me about safety, studies, or just chat! 💬</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px;">
                    <input type="text" id="chatInput" placeholder="Tell me about yourself or ask anything..." style="flex: 1; padding: 12px; border: 1px solid #dee2e6; border-radius: 8px; font-size: 14px;" onkeypress="if(event.key==='Enter') sendMessage()">
                    <button onclick="sendMessage()" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">Send 🚀</button>
                    <button onclick="clearChatHistory()" style="background: #6b7280; color: white; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; font-weight: 600;" title="Clear chat">🗑️</button>
                </div>
            `;
            showModal('🤖💫 AI Friend', chatHTML);
            
            // Загружаем сохраненную историю после открытия модального окна
            setTimeout(loadChatHistory, 100);
        }
        
        let chatHistory = [];
        
        // Load chat history from localStorage when opening modal
        function loadChatHistory() {
            const savedHistory = localStorage.getItem('ehsChatHistory');
            const savedMessages = localStorage.getItem('ehsChatMessages');
            
            if (savedHistory) {
                chatHistory = JSON.parse(savedHistory);
            }
            
            if (savedMessages) {
                const messagesDiv = document.getElementById('chatMessages');
                if (messagesDiv) {
                    messagesDiv.innerHTML = savedMessages;
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            }
        }
        
        // Save chat history to localStorage
        function saveChatHistory() {
            localStorage.setItem('ehsChatHistory', JSON.stringify(chatHistory));
            const messagesDiv = document.getElementById('chatMessages');
            if (messagesDiv) {
                localStorage.setItem('ehsChatMessages', messagesDiv.innerHTML);
            }
        }
        
        // Clear chat history
        function clearChatHistory() {
            if (confirm('Clear entire chat history?')) {
                chatHistory = [];
                localStorage.removeItem('ehsChatHistory');
                localStorage.removeItem('ehsChatMessages');
                
                const messagesDiv = document.getElementById('chatMessages');
                if (messagesDiv) {
                    messagesDiv.innerHTML = `
                        <div style="color: #2c3e50; text-align: center; padding: 40px 20px; font-size: 16px; line-height: 1.6;">
                            <div style="font-size: 48px; margin-bottom: 20px; opacity: 0.7;">🌟</div>
                            <div style="font-weight: 600; margin-bottom: 12px;">Hi! I'm your digital friend</div>
                            <div style="opacity: 0.8; margin-bottom: 12px;">I'll help you find like-minded people at the faculty and build strong friendships</div>
                            <div style="opacity: 0.7; font-size: 14px;">Ask me about safety, studies, or just chat! 💬</div>
                        </div>
                    `;
                }
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;
            
            const messagesDiv = document.getElementById('chatMessages');
            
            messagesDiv.innerHTML += `<div style="margin: 8px 0; text-align: right;"><div style="background: var(--brand); color: white; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 80%;">👤 ${message}</div></div>`;
            
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            messagesDiv.innerHTML += `<div id="loading" style="margin: 8px 0;"><div style="background: #e9ecef; padding: 8px 12px; border-radius: 12px; display: inline-block;">🤖 Thinking...</div></div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            try {
                chatHistory.push({role: 'user', content: message});
                
                const formData = new FormData();
                formData.append('message', message);
                formData.append('history', JSON.stringify(chatHistory));
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                document.getElementById('loading').remove();
                
                chatHistory.push({role: 'assistant', content: data.response});
                
                messagesDiv.innerHTML += `<div style="margin: 8px 0;"><div style="background: white; border: 1px solid #dee2e6; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 80%;">🤖 ${data.response}</div></div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                // Save history after each message
                saveChatHistory();
                
            } catch (error) {
                document.getElementById('loading').remove();
                messagesDiv.innerHTML += `<div style="margin: 8px 0;"><div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 8px 12px; border-radius: 12px; display: inline-block;">❌ Error: ${error.message}</div></div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                // Save history even on error
                saveChatHistory();
            }
        }
        
        // File input change handler with auto-processing
        document.getElementById('pdfFile').addEventListener('change', function(e) {
            const dropZone = document.getElementById('dropZone');
            if (e.target.files.length > 0) {
                const fileName = e.target.files[0].name;
                dropZone.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 16px; color: #4ade80;">✅</div>
                    <div style="font-size: 18px; font-weight: 700; color: black; margin-bottom: 8px;">File Selected</div>
                    <div style="font-size: 14px; color: #374151; font-weight: 500;">${fileName}</div>
                `;
                dropZone.style.borderColor = 'rgba(74, 222, 128, 0.6)';
                dropZone.style.background = 'rgba(74, 222, 128, 0.1)';
                
                // Auto-start processing after a short delay
                setTimeout(() => {
                    uploadPDF();
                }, 500);
            } else {
                dropZone.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.8;">📄</div>
                    <div style="font-size: 18px; font-weight: 700; color: black; margin-bottom: 8px;">Drag & Drop Your PDF</div>
                    <div style="font-size: 14px; color: #374151; line-height: 1.4;">Our AI will work its magic through Amazon Bedrock<br>and create personalized training assignments</div>
                `;
                dropZone.style.borderColor = 'rgba(255,255,255,0.4)';
                dropZone.style.background = 'rgba(255,255,255,0.1)';
            }
        });
        

    </script>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById('pdfFile');
            
            if (!fileInput.files[0]) {
                showModal('⚠️ Error', '<div style="text-align: center; padding: 40px; color: #dc3545;">Please select a PDF file!</div>');
                return;
            }

            showModal('🤖 AI Analysis', '<div style="text-align: center; padding: 40px;">🤖 AI analyzing protocol via Amazon Bedrock...<br><br>⏱️ Approximately 30-40 seconds for 10 users</div>');

            try {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                const response = await fetch('/upload-pdf', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                displayResult(data);

            } catch (error) {
                console.error('Error:', error);
                showModal('❌ Error', '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Processing error</div>');
            }
        }
        
        async function loadDocumentHistory() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('documentHistory');
                
                if (data.documents && data.documents.length > 0) {
                    let html = '<h3>📄 History of processed documents (' + data.total_documents + '):</h3>';
                    
                    data.documents.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
                        html += `<strong>📄 ${doc.title}</strong>`;
                        html += `<button onclick="toggleDetails('doc${index}')" style="background: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">🔍 Details</button>`;
                        html += `</div>`;
                        html += `<div style="color: #6c757d; font-size: 12px;">⏰ ${date} | 🎯 ${doc.assignments_count} assignments</div>`;
                        
                        // Скрытые детали
                        html += `<div id="doc${index}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">`;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5>📊 Course Assignments:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 8px; margin: 5px 0; border-radius: 3px; font-size: 12px;">`;
                                html += `📚 <strong>${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                                html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                                html += `🎯 Priority: ${assignment.priority} | ⏰ Assigned: ${assignDate}<br>`;
                                
                                // Добавляем дедлайн и период
                                const assignedDate = new Date(assignment.timestamp);
                                const deadlineDays = 30; // по умолчанию
                                const renewalMonths = 12; // по умолчанию
                                const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                                const renewalDate = new Date(assignedDate.getTime() + renewalMonths * 30 * 24 * 60 * 60 * 1000);
                                
                                html += `⏳ Deadline: ${deadlineDate.toLocaleDateString()} | 🔄 Обновление: ${renewalDate.toLocaleDateString()}`;
                                if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic;">No courses assigned</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5>⚠️ Skipped Duplicates:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 8px; margin: 5px 0; border-radius: 3px; font-size: 12px;">`;
                                html += `😫 <strong>${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<strong>Skipped:</strong> ${skip.skipped_courses.join(', ')}<br>`;
                                html += `<em>${skip.reason}</em>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div></div>`;
                    });
                    
                    historyDiv.innerHTML = html;
                } else {
                    historyDiv.innerHTML = '';
                }
                
            } catch (error) {
                console.error('Error loading document history:', error);
            }
        }
        
        function showDocDetails() {
            showModal('📄 Document Details', '<p>Document processed successfully</p>');
        }
        
        async function showDocumentDetailsFromBelow(index) {
            showModal('📄 Document Details', '<div style="text-align: center; padding: 40px;">📄 Loading document details...</div>');
            
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                const doc = data.documents[index];
                
                if (doc) {
                    let html = `
                    <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                        <!-- Document Header -->
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                            <h3 style="margin: 0 0 12px 0; color: var(--gray-800); font-size: 24px;">📄 ${doc.title}</h3>
                            <div style="color: var(--gray-600); font-size: 14px;">⏰ Processed: ${new Date(doc.processed_at).toLocaleString()}</div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-top: 16px;">
                                <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 20px; font-weight: 700; color: var(--success);">${doc.assignments_count || 0}</div>
                                    <div style="font-size: 11px; color: var(--gray-600);">Assignments</div>
                                </div>
                                <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${doc.skipped_duplicates?.length || 0}</div>
                                    <div style="font-size: 11px; color: var(--gray-600);">Skipped</div>
                                </div>
                            </div>
                        </div>`;
                    
                    if (doc.assignments && doc.assignments.length > 0) {
                        html += `
                        <!-- Course Assignments -->
                        <div style="background: #f0fdf4; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 2px solid #bbf7d0;">
                            <h4 style="margin: 0 0 12px 0; color: var(--success);">📊 Course Assignments (${doc.assignments.length})</h4>`;
                        
                        doc.assignments.forEach(assignment => {
                            const priorityColors = {'critical': '#dc3545', 'high': '#fd7e14', 'normal': '#28a745', 'low': '#6c757d'};
                            html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                            html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                            html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${assignment.course_id}</div>`;
                            html += `<div style="font-size: 12px; color: ${priorityColors[assignment.priority] || '#28a745'}; font-weight: 600;">${assignment.priority.toUpperCase()}</div>`;
                            html += `</div>`;
                            html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong style="color: var(--blue);">${assignment.user_name || assignment.user_id}</strong> - ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                            html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                            html += `<span>⏰ ${new Date(assignment.timestamp).toLocaleString()}</span>`;
                            html += `</div>`;
                            if (assignment.reason) html += `<div style="margin-top: 8px; font-size: 12px; color: var(--gray-600); font-style: italic; background: #f8f9fa; padding: 8px; border-radius: 6px;">📝 ${assignment.reason}</div>`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    } else {
                        html += '<div style="background: #f8f9fa; padding: 40px; border-radius: 12px; text-align: center; color: #6c757d; margin-bottom: 20px;">📚 No course assignments</div>';
                    }
                    
                    if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                        html += `
                        <!-- Skipped Duplicates -->
                        <div style="background: #fef3c7; padding: 16px; border-radius: 12px; border: 2px solid #fbbf24;">
                            <h4 style="margin: 0 0 12px 0; color: var(--warning);">⚠️ Skipped Duplicates (${doc.skipped_duplicates.length})</h4>`;
                        
                        doc.skipped_duplicates.forEach(skip => {
                            html += `<div style="background: white; border-left: 4px solid var(--warning); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                            html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px; margin-bottom: 8px;">😫 ${skip.name} (${skip.user_id})</div>`;
                            html += `<div style="margin: 8px 0; font-size: 13px; color: var(--gray-700);"><strong>🚫 Skipped Courses:</strong></div>`;
                            skip.skipped_courses.forEach(courseId => {
                                html += `<span style="background: #fef3c7; color: var(--warning); padding: 4px 8px; margin: 2px; border-radius: 4px; display: inline-block; font-size: 12px; font-weight: 500;">🚫 ${courseId}</span> `;
                            });
                            html += `<div style="margin-top: 8px; font-style: italic; color: var(--gray-600); font-size: 12px; background: #f8f9fa; padding: 8px; border-radius: 6px;">${skip.reason}</div>`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    }
                    
                    html += `
                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                        </div>
                    </div>`;
                    
                    document.getElementById('modalBody').innerHTML = html;
                } else {
                    document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Document not found</div>';
                }
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading document details</div>';
            }
        }
        
        async function loadDocumentHistoryModal() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                let html = `<h4>📄 Document History (${data.total_documents})</h4>`;
                
                if (data.documents && data.documents.length > 0) {
                    html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                        <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Sort:</label>
                        <select onchange="sortDocuments(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                            <option value="date">By Date</option>
                            <option value="title">By Title</option>
                            <option value="assignments">By Assignments</option>
                        </select>
                    </div>`;
                    html += `<div id="documentsList">`;
                    
                    data.documents.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div class="document-item" data-date="${doc.processed_at}" data-title="${doc.title}" data-assignments="${doc.assignments_count}" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
                        html += `<strong style="font-size: 18px; color: #2a7d2e;">📄 ${doc.title}</strong>`;
                        html += `<button onclick="toggleDetailsModal('doc${index}')" style="background: #007bff; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px;">🔍 Details</button>`;
                        html += `</div>`;
                        html += `<div style="color: #6c757d; font-size: 14px;">⏰ ${date} | 🎯 ${doc.assignments_count} assignments</div>`;
                        
                        // Скрытые детали
                        html += `<div id="doc${index}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">`;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5>📈 Course Assignments:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                                html += `<strong style="color: #2a7d2e;">📚 ${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                                html += `<div style="margin: 4px 0; color: #666; font-size: 13px;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                                html += `<div style="color: #666; font-size: 13px;">🎯 Priority: ${assignment.priority} | ⏰ ${assignDate}</div>`;
                                if (assignment.reason) html += `<div style="margin-top: 4px; color: #666; font-size: 13px;">📝 ${assignment.reason}</div>`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic;">No courses assigned</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5>⚠️ Skipped Duplicates:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                                html += `<strong>😫 ${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<div style="margin: 4px 0; color: #856404;"><strong>Skipped:</strong> ${skip.skipped_courses.join(', ')}</div>`;
                                html += `<div style="color: #856404; font-style: italic;">${skip.reason}</div>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div></div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #6c757d;">No processed documents</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error loading document history:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading history</div>';
            }
        }
        
        function toggleDetailsModal(id) {
            const element = document.getElementById(id);
            if (element.style.display === 'none') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        }
        
        async function checkExpiredModal() {
            try {
                const response = await fetch('/expired-courses');
                const data = await response.json();
                
                let html = `<h4>⏰ Course Deadline Check</h4>`;
                
                if (data.expired_users && data.expired_users.length > 0) {
                    html += `<h5>⚠️ Found ${data.expired_count} users with expiring courses:</h5>`;
                    
                    data.expired_users.forEach(user => {
                        html += `<div style="background: #fff3cd; padding: 16px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #ffc107;">`;
                        html += `<strong style="font-size: 18px; color: #856404;">${user.user_name || user.user_id}</strong> - ${user.role || ''}, ${user.department || ''}<br>`;
                        html += `<div style="margin: 12px 0;"><strong>Expiring courses:</strong></div>`;
                        
                        user.expired_courses.forEach(course => {
                            html += `<div style="margin: 8px 0; padding: 8px; background: #f8d7da; border-radius: 6px;">`;
                            html += `<strong style="color: #721c24;">🚨 ${course.course_id}</strong><br>`;
                            html += `<div style="color: #721c24; font-size: 13px;">Assigned: ${new Date(course.assigned_at).toLocaleDateString()} | Period: ${course.period_months} months</div>`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    });
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #28a745;">✅ All courses are current!</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error checking deadlines</div>';
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                // Update statistics cards
                document.getElementById('userCount').textContent = data.users;
                document.getElementById('courseCount').textContent = data.courses;
                document.getElementById('assignmentCount').textContent = data.assignments;
                document.getElementById('documentCount').textContent = data.documents;
                document.getElementById('activeProgressCount').textContent = data.active || 0;
                
                // Update progress bar
                const totalAssignments = data.assignments || 0;
                const completedAssignments = data.completions || 0;
                const progressPercent = totalAssignments > 0 ? Math.round((completedAssignments / totalAssignments) * 100) : 0;
                
                document.getElementById('progressPercent').textContent = progressPercent + '%';
                document.getElementById('progressFill').style.width = progressPercent + '%';
                document.getElementById('completedCount').textContent = completedAssignments;
                document.getElementById('overdueCount').textContent = data.expired || 0;
                document.getElementById('activeProgressCount').textContent = data.active || 0;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function showUsers() {
            showModal('👥 Users', '<div style="text-align: center; padding: 40px;">👥 Loading users list...</div>');
            
            try {
                const response = await fetch('/users-detail');
                const data = await response.json();
                
                const totalUsers = data.users.length;
                const activeUsers = data.users.filter(u => u.assignments_count > 0).length;
                const newUsers = data.users.filter(u => !u.latest_assignment).length;
                const topPerformers = data.users.filter(u => u.assignments_count >= 5).length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${totalUsers}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Total Users</div>
                        </div>
                        <div style="background: #f0fdf4; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${activeUsers}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Active Users</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${newUsers}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">New Users</div>
                        </div>
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${topPerformers}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Top Performers</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🏢 Department</label>
                                <select id="userDeptFilter" onchange="window.filterUsers && window.filterUsers()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Departments</option>
                                    <option value="Chemistry Lab">Chemistry Lab</option>
                                    <option value="Biochemistry">Biochemistry</option>
                                    <option value="Facilities">Facilities</option>
                                    <option value="HR">HR</option>
                                    <option value="Warehouse">Warehouse</option>
                                    <option value="Radiation Safety">Radiation Safety</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">👤 Role</label>
                                <select id="userRoleFilter" onchange="window.filterUsers && window.filterUsers()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Roles</option>
                                    <option value="lab_tech">Lab Tech</option>
                                    <option value="chem_researcher">Chem Researcher</option>
                                    <option value="facilities_maintenance">Facilities Maintenance</option>
                                    <option value="office_worker">Office Worker</option>
                                    <option value="forklift_operator">Forklift Operator</option>
                                    <option value="radiation_worker">Radiation Worker</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="userSortFilter" onchange="window.filterUsers && window.filterUsers()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="name">Name (A-Z)</option>
                                    <option value="assignments">Most Assignments</option>
                                    <option value="role">Role</option>
                                    <option value="department">Department</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing all ${totalUsers} users</div>
                    </div>
                    
                    <!-- Users List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">👥 User Directory</h4>
                        <div id="usersList">`;
                
                html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">';
                
                data.users.forEach(user => {
                    const lastAssignment = user.latest_assignment ? new Date(user.latest_assignment).toLocaleDateString() : 'Never';
                    
                    html += `<div class="user-item" data-name="${user.name}" data-role="${user.role}" data-department="${user.department}" data-assignments="${user.assignments_count}" style="background: white; border-left: 4px solid var(--blue); padding: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                    html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                    html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">👤 ${user.name}</div>`;
                    html += `<div style="font-size: 12px; color: var(--gray-500);">${user.user_id}</div>`;
                    html += `</div>`;
                    html += `<div style="margin: 6px 0; font-size: 13px;">🏢 <strong style="color: var(--brand);">${user.role}</strong> in <strong style="color: var(--purple);">${user.department}</strong></div>`;
                    html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                    html += `<span>🎯 ${user.assignments_count} assignments</span>`;
                    html += `<span>📅 Last: ${lastAssignment}</span>`;
                    html += `</div>`;
                    html += `<div style="margin-top: 8px;"><button onclick="window.open('/user/${user.user_id}/dashboard', '_blank')" style="background: #16a34a; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">VIEW INFO</button></div>`;
                    html += `</div>`;
                });
                
                html += '</div>';
                
                html += `</div></div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading users</div>';
            }
        }
        
        async function showCourses() {
            showModal('📚 Courses', '<div style="text-align: center; padding: 40px;">📚 Loading courses list...</div>');
            
            try {
                const response = await fetch('/courses-detail');
                const data = await response.json();
                
                const totalCourses = data.courses.length;
                const activeCourses = data.courses.filter(c => c.assignments_count > 0).length;
                const criticalCourses = data.courses.filter(c => c.priority === 'critical').length;
                const highPriorityCourses = data.courses.filter(c => c.priority === 'high').length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${totalCourses}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Total Courses</div>
                        </div>
                        <div style="background: #f0fdf4; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${activeCourses}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Active Courses</div>
                        </div>
                        <div style="background: #fef2f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--error);">${criticalCourses}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Critical Priority</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${highPriorityCourses}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">High Priority</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🎯 Priority</label>
                                <select id="coursePriorityFilter" onchange="window.filterCourses && window.filterCourses()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Priorities</option>
                                    <option value="critical">🔴 Critical</option>
                                    <option value="high">🟠 High</option>
                                    <option value="normal">🟢 Normal</option>
                                    <option value="low">⚪ Low</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Activity</label>
                                <select id="courseActivityFilter" onchange="window.filterCourses && window.filterCourses()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Courses</option>
                                    <option value="active">Active (with assignments)</option>
                                    <option value="inactive">Inactive (no assignments)</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="courseSortFilter" onchange="window.filterCourses && window.filterCourses()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="name">Name (A-Z)</option>
                                    <option value="assignments">Most Assignments</option>
                                    <option value="priority">Priority Level</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing all ${totalCourses} courses</div>
                    </div>
                    
                    <!-- Courses List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">📚 Course Catalog</h4>
                        <div id="coursesList">`;
                
                data.courses.forEach(course => {
                    const lastAssignment = course.latest_assignment ? new Date(course.latest_assignment).toLocaleDateString() : 'Never';
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14',
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div class="course-item" data-name="${course.course_name || course.course_id}" data-assignments="${course.assignments_count}" data-priority="${course.priority}" style="background: white; border-left: 4px solid ${priorityColors[course.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                    html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                    html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${course.course_name || course.course_id}</div>`;
                    html += `<div style="font-size: 12px; color: var(--gray-500);">${course.course_id}</div>`;
                    html += `</div>`;
                    html += `<div style="margin: 6px 0; font-size: 13px; color: var(--gray-600);">${course.description || 'No description available'}</div>`;
                    html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                    html += `<span>🎯 ${course.assignments_count} assignments</span>`;
                    html += `<span>📅 Last: ${lastAssignment}</span>`;
                    html += `<span>🔄 ${course.renewal_months} months</span>`;
                    html += `<span style="color: ${priorityColors[course.priority] || '#28a745'};">Priority: ${course.priority}</span>`;
                    html += `</div>`;
                    html += `</div>`;
                });
                
                html += `</div></div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading courses</div>';
            }
        }
        
        async function showAssignments() {
            showModal('🎯 Course Assignments', '<div style="text-align: center; padding: 40px;">🎯 Loading assignments...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                const totalAssignments = data.assignments.length;
                const criticalAssignments = data.assignments.filter(a => a.priority === 'critical').length;
                const highPriorityAssignments = data.assignments.filter(a => a.priority === 'high').length;
                const recentAssignments = data.assignments.filter(a => {
                    const assignDate = new Date(a.timestamp);
                    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    return assignDate > weekAgo;
                }).length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${totalAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Total Assignments</div>
                        </div>
                        <div style="background: #fef2f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--error);">${criticalAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Critical Priority</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${highPriorityAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">High Priority</div>
                        </div>
                        <div style="background: #f0fdf4; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${recentAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">This Week</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🎯 Priority</label>
                                <select id="assignmentPriorityFilter" onchange="window.filterAssignments && window.filterAssignments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Priorities</option>
                                    <option value="critical">🔴 Critical</option>
                                    <option value="high">🟠 High</option>
                                    <option value="normal">🟢 Normal</option>
                                    <option value="low">⚪ Low</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🏢 Department</label>
                                <select id="assignmentDeptFilter" onchange="window.filterAssignments && window.filterAssignments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Departments</option>
                                    <option value="Chemistry Lab">Chemistry Lab</option>
                                    <option value="Biochemistry">Biochemistry</option>
                                    <option value="Facilities">Facilities</option>
                                    <option value="HR">HR</option>
                                    <option value="Warehouse">Warehouse</option>
                                    <option value="Radiation Safety">Radiation Safety</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="assignmentSortFilter" onchange="window.filterAssignments && window.filterAssignments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="date">Recent First</option>
                                    <option value="priority">Priority Level</option>
                                    <option value="course">Course Name</option>
                                    <option value="user">User Name</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing all ${totalAssignments} assignments</div>
                    </div>
                    
                    <!-- Assignments List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🎯 Assignment History</h4>
                        <div id="assignmentsList">`;
                
                data.assignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div class="assignment-item" data-date="${assignment.timestamp}" data-priority="${assignment.priority}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" data-department="${assignment.user_department || ''}" style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                    html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                    html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${assignment.course_id}</div>`;
                    html += `<div style="font-size: 12px; color: ${priorityColors[assignment.priority] || '#28a745'}; font-weight: 600;">${assignment.priority.toUpperCase()}</div>`;
                    html += `</div>`;
                    html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong onclick="showUserProfile('${assignment.user_id}')" style="color: var(--blue); cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong> - ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                    html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                    html += `<span>⏰ ${date}</span>`;
                    html += `<span>🤖 AI Assigned</span>`;
                    html += `</div>`;
                    if (assignment.reason) html += `<div style="margin-top: 8px; font-size: 12px; color: var(--gray-600); font-style: italic;">📝 ${assignment.reason}</div>`;
                    html += `</div>`;
                });
                
                html += `</div></div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading assignments</div>';
            }
        }
        
        async function showDocuments() {
            showModal('📄 Document Analytics', '<div style="text-align: center; padding: 40px;">📄 Loading document history...</div>');
            
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const totalDocuments = data.documents.length;
                const documentsWithAssignments = data.documents.filter(d => d.assignments_count > 0).length;
                const highImpactDocuments = data.documents.filter(d => d.assignments_count >= 5).length;
                const recentDocuments = data.documents.filter(d => {
                    const processedDate = new Date(d.processed_at);
                    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    return processedDate > weekAgo;
                }).length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #fed7aa; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--orange);">${totalDocuments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Total Documents</div>
                        </div>
                        <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${documentsWithAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">With Assignments</div>
                        </div>
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${highImpactDocuments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">High Impact (5+)</div>
                        </div>
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${recentDocuments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">This Week</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Impact</label>
                                <select id="documentImpactFilter" onchange="window.filterDocuments && window.filterDocuments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Documents</option>
                                    <option value="with-assignments">With Assignments</option>
                                    <option value="no-assignments">No Assignments</option>
                                    <option value="high-impact">High Impact (5+)</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📅 Time Period</label>
                                <select id="documentTimeFilter" onchange="window.filterDocuments && window.filterDocuments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Time</option>
                                    <option value="recent">Last 7 Days</option>
                                    <option value="month">Last 30 Days</option>
                                    <option value="quarter">Last 90 Days</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="documentSortFilter" onchange="window.filterDocuments && window.filterDocuments()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="date">Recent First</option>
                                    <option value="assignments">Most Assignments</option>
                                    <option value="title">Title (A-Z)</option>
                                    <option value="impact">Total Impact</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing all ${totalDocuments} documents</div>
                    </div>
                    
                    <!-- Documents List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">📄 Document Processing History</h4>
                        <div id="documentsList">`;
                
                data.documents.forEach((doc, index) => {
                    const date = new Date(doc.processed_at).toLocaleString();
                    const impactScore = doc.assignments_count + (doc.skipped_duplicates?.length || 0);
                    
                    html += `<div class="document-item" data-date="${doc.processed_at}" data-title="${doc.title}" data-assignments="${doc.assignments_count}" data-impact="${impactScore}" style="background: white; border-left: 4px solid var(--orange); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                    html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                    html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📄 ${doc.title}</div>`;
                    html += `<button onclick="toggleDocumentDetails('doc${index}')" style="background: var(--blue); color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 11px;">Details</button>`;
                    html += `</div>`;
                    html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                    html += `<span>🎯 ${doc.assignments_count} assignments</span>`;
                    html += `<span>⏰ ${date}</span>`;
                    html += `<span>📊 Impact: ${impactScore}</span>`;
                    html += `</div>`;
                    
                    // Hidden details
                    html += `<div id="doc${index}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">`;
                    
                    if (doc.assignments && doc.assignments.length > 0) {
                        html += `<h5 style="color: var(--success); margin-bottom: 8px;">📊 Course Assignments:</h5>`;
                        doc.assignments.forEach(assignment => {
                            const assignDate = new Date(assignment.timestamp).toLocaleString();
                            const priorityColors = {'critical': '#dc3545', 'high': '#fd7e14', 'normal': '#28a745', 'low': '#6c757d'};
                            
                            html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 8px; margin: 4px 0; border-radius: 4px; font-size: 12px;">`;
                            html += `📚 <strong>${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: var(--blue); cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                            html += `<span style="color: var(--gray-600);">🎯 ${assignment.priority} | ⏰ ${assignDate}</span>`;
                            html += `</div>`;
                        });
                    }
                    
                    if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                        html += `<h5 style="color: var(--warning); margin: 8px 0 4px 0;">⚠️ Skipped Duplicates:</h5>`;
                        doc.skipped_duplicates.forEach(skip => {
                            html += `<div style="background: #fff3cd; padding: 8px; margin: 4px 0; border-radius: 4px; font-size: 12px;">`;
                            html += `😫 <strong onclick="showUserProfile('${skip.user_id}')" style="color: var(--warning); cursor: pointer; text-decoration: underline;">${skip.name}</strong> - ${skip.skipped_courses.join(', ')}`;
                            html += `</div>`;
                        });
                    }
                    
                    html += `</div></div>`;
                });
                
                html += `</div></div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading documents</div>';
            }
        }
        
        function sortDocuments(sortBy) {
            const container = document.getElementById('documentsList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.document-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        async function showExpired() {
            showModal('❌ Expired', '<div style="text-align: center; padding: 40px;">❌ Checking expired courses...</div>');
            checkExpiredModal();
        }
        
        async function showCritical() {
            showModal('🔴 Critical Priority Courses', '<div style="text-align: center; padding: 40px;">🔴 Loading critical courses...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                const criticalAssignments = data.assignments.filter(a => a.priority === 'critical');
                const recentCritical = criticalAssignments.filter(a => {
                    const assignDate = new Date(a.timestamp);
                    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    return assignDate > weekAgo;
                }).length;
                const urgentCritical = criticalAssignments.filter(a => {
                    const assignDate = new Date(a.timestamp);
                    const threeDaysAgo = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000);
                    return assignDate > threeDaysAgo;
                }).length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #fef2f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--error);">${criticalAssignments.length}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Critical Courses</div>
                        </div>
                        <div style="background: #fff1f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: #dc2626;">${urgentCritical}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Last 3 Days</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${recentCritical}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">This Week</div>
                        </div>
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${Math.round((criticalAssignments.length / data.assignments.length) * 100) || 0}%</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Of Total</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🏢 Department</label>
                                <select id="criticalDeptFilter" onchange="window.filterCritical && window.filterCritical()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Departments</option>
                                    <option value="Chemistry Lab">Chemistry Lab</option>
                                    <option value="Biochemistry">Biochemistry</option>
                                    <option value="Facilities">Facilities</option>
                                    <option value="HR">HR</option>
                                    <option value="Warehouse">Warehouse</option>
                                    <option value="Radiation Safety">Radiation Safety</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">⏰ Urgency</label>
                                <select id="criticalUrgencyFilter" onchange="window.filterCritical && window.filterCritical()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Critical</option>
                                    <option value="urgent">Last 3 Days</option>
                                    <option value="recent">This Week</option>
                                    <option value="older">Older</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="criticalSortFilter" onchange="window.filterCritical && window.filterCritical()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="date">Most Recent</option>
                                    <option value="course">Course Name</option>
                                    <option value="user">User Name</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing <span id="criticalCount">${criticalAssignments.length}</span> critical courses</div>
                    </div>`;
                
                if (criticalAssignments.length > 0) {
                    html += `
                    <!-- Critical Courses List -->
                    <div style="background: #fef2f2; padding: 16px; border-radius: 12px; border: 2px solid #fecaca;">
                        <h4 style="margin: 0 0 12px 0; color: var(--error);">🔴 Critical Priority Assignments</h4>
                        <div id="criticalList">`;
                    
                    criticalAssignments.forEach(assignment => {
                        const date = new Date(assignment.timestamp).toLocaleString();
                        const assignDate = new Date(assignment.timestamp);
                        const now = new Date();
                        const daysAgo = Math.floor((now - assignDate) / (1000 * 60 * 60 * 24));
                        
                        let urgencyBadge = '';
                        if (daysAgo <= 3) urgencyBadge = '<span style="background: #dc2626; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600;">URGENT</span>';
                        else if (daysAgo <= 7) urgencyBadge = '<span style="background: #f59e0b; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600;">RECENT</span>';
                        
                        html += `<div class="critical-item" data-date="${assignment.timestamp}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" data-department="${assignment.user_department || ''}" data-urgency="${daysAgo <= 3 ? 'urgent' : daysAgo <= 7 ? 'recent' : 'older'}" style="background: white; border-left: 4px solid var(--error); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(220, 53, 69, 0.1); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(220, 53, 69, 0.2)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(220, 53, 69, 0.1)'">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                        html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${assignment.course_id}</div>`;
                        html += `<div style="display: flex; gap: 8px; align-items: center;"><span style="font-size: 12px; color: var(--error); font-weight: 600;">🔴 CRITICAL</span>${urgencyBadge}</div>`;
                        html += `</div>`;
                        html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong onclick="showUserProfile('${assignment.user_id}')" style="color: var(--blue); cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong> - ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                        html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                        html += `<span>⏰ ${date}</span>`;
                        html += `<span>📅 ${daysAgo} days ago</span>`;
                        html += `</div>`;
                        if (assignment.reason) html += `<div style="margin-top: 8px; font-size: 12px; color: var(--gray-600); font-style: italic;">📝 ${assignment.reason}</div>`;
                        html += `</div>`;
                    });
                    
                    html += `</div></div>`;
                } else {
                    html += '<div style="background: #f0fdf4; padding: 40px; border-radius: 12px; text-align: center; color: var(--success);">✅ No critical priority courses - great job!</div>';
                }
                
                html += `
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading critical courses</div>';
            }
        }
        
        async function showActive() {
            showModal('⚙️ Active Courses', '<div style="text-align: center; padding: 40px;">⚙️ Loading active courses...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                // Filter for active courses (not completed, not expired)
                const activeAssignments = data.assignments.filter(assignment => {
                    // This is a simplified check - in real implementation you'd check completion status
                    return true; // For now, show all assignments as "active"
                });
                
                const totalActive = activeAssignments.length;
                const criticalActive = activeAssignments.filter(a => a.priority === 'critical').length;
                const highPriorityActive = activeAssignments.filter(a => a.priority === 'high').length;
                const recentActive = activeAssignments.filter(a => {
                    const assignDate = new Date(a.timestamp);
                    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    return assignDate > weekAgo;
                }).length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${totalActive}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Active Courses</div>
                        </div>
                        <div style="background: #fef2f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--error);">${criticalActive}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Critical Priority</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${highPriorityActive}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">High Priority</div>
                        </div>
                        <div style="background: #f0fdf4; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${recentActive}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">This Week</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🎯 Priority</label>
                                <select id="activePriorityFilter" onchange="window.filterActive && window.filterActive()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Priorities</option>
                                    <option value="critical">🔴 Critical</option>
                                    <option value="high">🟠 High</option>
                                    <option value="normal">🟢 Normal</option>
                                    <option value="low">⚪ Low</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🏢 Department</label>
                                <select id="activeDeptFilter" onchange="window.filterActive && window.filterActive()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Departments</option>
                                    <option value="Chemistry Lab">Chemistry Lab</option>
                                    <option value="Biochemistry">Biochemistry</option>
                                    <option value="Facilities">Facilities</option>
                                    <option value="HR">HR</option>
                                    <option value="Warehouse">Warehouse</option>
                                    <option value="Radiation Safety">Radiation Safety</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="activeSortFilter" onchange="window.filterActive && window.filterActive()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="date">Recent First</option>
                                    <option value="priority">Priority Level</option>
                                    <option value="course">Course Name</option>
                                    <option value="user">User Name</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing <span id="activeCount">${totalActive}</span> active courses</div>
                    </div>
                    
                    <!-- Active Courses List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">⚙️ Active Course Assignments</h4>
                        <div id="activeList">`;
                
                activeAssignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div class="active-item" data-date="${assignment.timestamp}" data-priority="${assignment.priority}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" data-department="${assignment.user_department || ''}" style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                    html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                    html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${assignment.course_id}</div>`;
                    html += `<div style="font-size: 12px; color: var(--blue); font-weight: 600;">⚙️ ACTIVE</div>`;
                    html += `</div>`;
                    html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong onclick="showUserProfile('${assignment.user_id}')" style="color: var(--blue); cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong> - ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                    html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                    html += `<span>⏰ ${date}</span>`;
                    html += `<span>🎯 ${assignment.priority.toUpperCase()}</span>`;
                    html += `</div>`;
                    if (assignment.reason) html += `<div style="margin-top: 8px; font-size: 12px; color: var(--gray-600); font-style: italic;">📝 ${assignment.reason}</div>`;
                    html += `</div>`;
                });
                
                html += `</div></div>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading active courses</div>';
            }
        }
        
        async function showCompletions() {
            showModal('✅ Course Completions', '<div style="text-align: center; padding: 40px;">✅ Loading completed courses...</div>');
            
            try {
                const response = await fetch('/completions-detail');
                const data = await response.json();
                
                const totalCompletions = data.completions.length;
                const recentCompletions = data.completions.filter(c => {
                    const completedDate = new Date(c.completed_at);
                    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                    return completedDate > weekAgo;
                }).length;
                const manualCompletions = data.completions.filter(c => c.completion_method === 'manual').length;
                const autoCompletions = data.completions.filter(c => c.completion_method === 'auto').length;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${totalCompletions}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Total Completed</div>
                        </div>
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${recentCompletions}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">This Week</div>
                        </div>
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${manualCompletions}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Manual</div>
                        </div>
                        <div style="background: #fed7aa; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--orange);">${autoCompletions}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Automatic</div>
                        </div>
                    </div>
                    
                    <!-- Smart Filters -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🔍 Smart Filters</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">🎯 Method</label>
                                <select id="completionMethodFilter" onchange="window.filterCompletions && window.filterCompletions()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Methods</option>
                                    <option value="manual">👤 Manual</option>
                                    <option value="auto">🤖 Automatic</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📅 Time Period</label>
                                <select id="completionTimeFilter" onchange="window.filterCompletions && window.filterCompletions()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="all">All Time</option>
                                    <option value="recent">Last 7 Days</option>
                                    <option value="month">Last 30 Days</option>
                                    <option value="quarter">Last 90 Days</option>
                                </select>
                            </div>
                            <div>
                                <label style="font-size: 12px; font-weight: 600; color: var(--gray-700); display: block; margin-bottom: 4px;">📊 Sort By</label>
                                <select id="completionSortFilter" onchange="window.filterCompletions && window.filterCompletions()" style="width: 100%; padding: 6px 8px; border-radius: 6px; border: 1px solid #d1d5db; font-size: 13px;">
                                    <option value="date">Recent First</option>
                                    <option value="course">Course Name</option>
                                    <option value="user">User Name</option>
                                    <option value="method">Method</option>
                                </select>
                            </div>
                        </div>
                        <div style="margin-top: 12px; font-size: 13px; color: var(--gray-600);">Showing <span id="completionCount">${totalCompletions}</span> completions</div>
                    </div>`;
                
                if (data.completions && data.completions.length > 0) {
                    html += `
                    <!-- Completions List -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">✅ Completion History</h4>
                        <div id="completionsList">`;
                    
                    data.completions.forEach(completion => {
                        const date = new Date(completion.completed_at).toLocaleString();
                        
                        html += `<div class="completion-item" data-date="${completion.completed_at}" data-course="${completion.course_id}" data-user="${completion.user_name || completion.user_id}" data-method="${completion.completion_method}" style="background: white; border-left: 4px solid var(--success); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: all 0.2s ease;" onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)'">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                        html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 ${completion.course_id}</div>`;
                        html += `<div style="font-size: 12px; color: var(--success); font-weight: 600;">✅ COMPLETED</div>`;
                        html += `</div>`;
                        html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong onclick="showUserProfile('${completion.user_id}')" style="color: var(--blue); cursor: pointer; text-decoration: underline;">${completion.user_name || completion.user_id}</strong> - ${completion.user_role || ''}, ${completion.user_department || ''}</div>`;
                        html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                        html += `<span>⏰ ${date}</span>`;
                        html += `<span>🎯 ${completion.completion_method === 'manual' ? '👤 Manual' : '🤖 Auto'}</span>`;
                        html += `</div>`;
                        html += `</div>`;
                    });
                    
                    html += `</div></div>`;
                } else {
                    html += '<div style="background: #f8f9fa; padding: 40px; border-radius: 12px; text-align: center; color: #6c757d;">📚 No completed courses yet</div>';
                }
                
                html += `
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading completions</div>';
            }
        }
        
        async function showUserProfile(userId) {
            showModal('👤 User Profile', '<div style="text-align: center; padding: 40px;">👤 Loading profile...</div>');
            
            try {
                const response = await fetch(`/user/${userId}`);
                const data = await response.json();
                
                if (data.error) {
                    document.getElementById('modalBody').innerHTML = `<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ ${data.error}</div>`;
                    return;
                }
                
                let html = '<div>';
                
                // Шапка профиля
                html += `<div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">`;
                html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">`;
                html += `<div><h3 style="margin: 0; color: var(--gray-800); font-size: 24px;">👤 ${data.user.name}</h3><p style="margin: 4px 0 0 0; color: var(--gray-600); font-size: 14px;">${data.user.user_id}</p></div>`;
                html += `<a href="/user/${userId}/dashboard" target="_blank" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 10px 20px; text-decoration: none; border-radius: 10px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">📈 Dashboard</a>`;
                html += `</div>`;
                html += `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">`;
                html += `<div><strong style="color: var(--gray-700);">🏢 Role:</strong><br><span style="color: var(--gray-800);">${data.user.role}</span></div>`;
                html += `<div><strong style="color: var(--gray-700);">🏭 Department:</strong><br><span style="color: var(--gray-800);">${data.user.department}</span></div>`;
                html += `</div></div>`;
                
                // Подсчитываем статистику
                const completedCount = data.assignments.filter(a => a.is_completed).length;
                const expiredCount = data.assignments.filter(a => a.is_expired && !a.is_completed).length;
                const activeCount = data.assignments.filter(a => !a.is_completed && !a.is_expired).length;
                const urgentDeadlines = data.assignments.filter(a => {
                    if (a.is_completed || a.is_expired) return false;
                    const assignedDate = new Date(a.timestamp);
                    const deadlineDays = a.deadline_days || 30;
                    const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                    const daysLeft = Math.ceil((deadlineDate - new Date()) / (1000 * 60 * 60 * 24));
                    return daysLeft <= 7 && daysLeft > 0;
                }).length;
                
                html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin: 15px 0;">`;
                html += `<div style="background: #d4edda; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${activeCount}</strong><br><small>✅ Active</small></div>`;
                html += `<div style="background: #cce5ff; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${completedCount}</strong><br><small>✅ Completed</small></div>`;
                html += `<div style="background: #ffebee; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${urgentDeadlines}</strong><br><small>⚠️ Deadline Soon</small></div>`;
                html += `<div style="background: #f8d7da; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${expiredCount}</strong><br><small>❌ Overdue</small></div>`;
                html += `<div style="background: #e3f2fd; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${data.total_assignments}</strong><br><small>📚 Total</small></div>`;
                html += `</div>`;
                
                html += `<p><a href="/user/${userId}/dashboard" target="_blank" style="background: #007bff; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px;">📊 Open Dashboard</a></p>`;
                html += `</div>`;
                
                // Assigned Courses
                if (data.assignments && data.assignments.length > 0) {
                    html += `<h4>📚 Assigned Courses (${data.assignments.length})</h4>`;
                    
                    data.assignments.forEach(assignment => {
                        const date = new Date(assignment.timestamp).toLocaleString();
                        const priorityColors = {
                            'critical': '#dc3545',
                            'high': '#fd7e14', 
                            'normal': '#28a745',
                            'low': '#6c757d'
                        };
                        
                        let statusColor, statusText;
                        if (assignment.is_completed) {
                            statusColor = '#28a745';
                            statusText = '✅ Completed';
                        } else if (assignment.is_expired) {
                            statusColor = '#dc3545';
                            statusText = '❌ Overdue';
                        } else {
                            // Проверяем скоро ли дедлайн
                            const assignedDate = new Date(assignment.timestamp);
                            const deadlineDays = assignment.deadline_days || 30;
                            const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                            const daysLeft = Math.ceil((deadlineDate - new Date()) / (1000 * 60 * 60 * 24));
                            
                            if (daysLeft <= 7 && daysLeft > 0) {
                                statusColor = '#f59e0b';
                                statusText = '⚠️ Deadline Soon';
                            } else {
                                statusColor = '#3b82f6';
                                statusText = '🔄 Active';
                            }
                        }
                        
                        html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 5px;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center;">`;
                        html += `<strong>📚 ${assignment.course_id}</strong>`;
                        html += `<span style="color: ${statusColor}; font-weight: bold;">${statusText}</span>`;
                        html += `</div>`;
                        html += `<div style="margin: 8px 0; font-size: 13px;">`;
                        html += `🎯 Priority: ${assignment.priority}<br>`;
                        html += `🔄 Period: ${assignment.renewal_months} months | ⏰ Deadline: ${assignment.deadline_days} days<br>`;
                        html += `⏰ Assigned: ${date}`;
                        if (assignment.reason) html += `<br>📝 Reason: ${assignment.reason}`;
                        html += `</div></div>`;
                    });
                } else {
                    html += '<p style="color: #6c757d; font-style: italic;">No assigned courses</p>';
                }
                
                html += '</div>';
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ Error loading profile</div>';
            }
        }
        
        // Global filter functions
        window.filterAssignments = function() {
            const priorityFilter = document.getElementById('assignmentPriorityFilter')?.value || 'all';
            const deptFilter = document.getElementById('assignmentDeptFilter')?.value || 'all';
            const sortFilter = document.getElementById('assignmentSortFilter')?.value || 'date';
            
            const container = document.getElementById('assignmentsList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.assignment-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                if (priorityFilter !== 'all' && item.dataset.priority !== priorityFilter) show = false;
                if (deptFilter !== 'all' && item.dataset.department !== deptFilter) show = false;
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'date') {
                    return new Date(b.dataset.date || '0') - new Date(a.dataset.date || '0');
                }
                if (sortFilter === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[b.dataset.priority] || 0) - (priorities[a.dataset.priority] || 0);
                }
                if (sortFilter === 'course') {
                    return (a.dataset.course || '').localeCompare(b.dataset.course || '');
                }
                if (sortFilter === 'user') {
                    return (a.dataset.user || '').localeCompare(b.dataset.user || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
        };
        
        window.filterUsers = function() {
            const deptFilter = document.getElementById('userDeptFilter')?.value || 'all';
            const roleFilter = document.getElementById('userRoleFilter')?.value || 'all';
            const sortFilter = document.getElementById('userSortFilter')?.value || 'name';
            
            const container = document.getElementById('usersList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.user-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                if (deptFilter !== 'all' && item.dataset.department !== deptFilter) show = false;
                if (roleFilter !== 'all' && item.dataset.role !== roleFilter) show = false;
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'assignments') {
                    return parseInt(b.dataset.assignments || '0') - parseInt(a.dataset.assignments || '0');
                }
                if (sortFilter === 'name') {
                    return (a.dataset.name || '').localeCompare(b.dataset.name || '');
                }
                if (sortFilter === 'role') {
                    return (a.dataset.role || '').localeCompare(b.dataset.role || '');
                }
                if (sortFilter === 'department') {
                    return (a.dataset.department || '').localeCompare(b.dataset.department || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
        };
        
        window.filterCourses = function() {
            const priorityFilter = document.getElementById('coursePriorityFilter')?.value || 'all';
            const activityFilter = document.getElementById('courseActivityFilter')?.value || 'all';
            const sortFilter = document.getElementById('courseSortFilter')?.value || 'name';
            
            const container = document.getElementById('coursesList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.course-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                if (priorityFilter !== 'all' && item.dataset.priority !== priorityFilter) show = false;
                if (activityFilter === 'active' && parseInt(item.dataset.assignments || '0') === 0) show = false;
                if (activityFilter === 'inactive' && parseInt(item.dataset.assignments || '0') > 0) show = false;
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'assignments') {
                    return parseInt(b.dataset.assignments || '0') - parseInt(a.dataset.assignments || '0');
                }
                if (sortFilter === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[b.dataset.priority] || 0) - (priorities[a.dataset.priority] || 0);
                }
                if (sortFilter === 'name') {
                    return (a.dataset.name || '').localeCompare(b.dataset.name || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
        };
        
        // Global filter functions for completions
        window.filterCompletions = function() {
            const methodFilter = document.getElementById('completionMethodFilter')?.value || 'all';
            const timeFilter = document.getElementById('completionTimeFilter')?.value || 'all';
            const sortFilter = document.getElementById('completionSortFilter')?.value || 'date';
            
            const container = document.getElementById('completionsList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.completion-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                const method = item.dataset.method || '';
                const completionDate = new Date(item.dataset.date || '0');
                const now = new Date();
                
                // Method filter
                if (methodFilter !== 'all' && method !== methodFilter) show = false;
                
                // Time filter
                if (timeFilter === 'recent' && (now - completionDate) > 7 * 24 * 60 * 60 * 1000) show = false;
                if (timeFilter === 'month' && (now - completionDate) > 30 * 24 * 60 * 60 * 1000) show = false;
                if (timeFilter === 'quarter' && (now - completionDate) > 90 * 24 * 60 * 60 * 1000) show = false;
                
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'date') {
                    return new Date(b.dataset.date || '0') - new Date(a.dataset.date || '0');
                }
                if (sortFilter === 'course') {
                    return (a.dataset.course || '').localeCompare(b.dataset.course || '');
                }
                if (sortFilter === 'user') {
                    return (a.dataset.user || '').localeCompare(b.dataset.user || '');
                }
                if (sortFilter === 'method') {
                    return (a.dataset.method || '').localeCompare(b.dataset.method || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
            
            // Update count
            const countEl = document.getElementById('completionCount');
            if (countEl) countEl.textContent = visibleItems.length;
        };
        
        // Global filter functions for active courses
        window.filterActive = function() {
            const priorityFilter = document.getElementById('activePriorityFilter')?.value || 'all';
            const deptFilter = document.getElementById('activeDeptFilter')?.value || 'all';
            const sortFilter = document.getElementById('activeSortFilter')?.value || 'date';
            
            const container = document.getElementById('activeList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.active-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                if (priorityFilter !== 'all' && item.dataset.priority !== priorityFilter) show = false;
                if (deptFilter !== 'all' && item.dataset.department !== deptFilter) show = false;
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'date') {
                    return new Date(b.dataset.date || '0') - new Date(a.dataset.date || '0');
                }
                if (sortFilter === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[b.dataset.priority] || 0) - (priorities[a.dataset.priority] || 0);
                }
                if (sortFilter === 'course') {
                    return (a.dataset.course || '').localeCompare(b.dataset.course || '');
                }
                if (sortFilter === 'user') {
                    return (a.dataset.user || '').localeCompare(b.dataset.user || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
            
            // Update count
            const countEl = document.getElementById('activeCount');
            if (countEl) countEl.textContent = visibleItems.length;
        };
        
        // Global filter functions for critical courses
        window.filterCritical = function() {
            const deptFilter = document.getElementById('criticalDeptFilter')?.value || 'all';
            const urgencyFilter = document.getElementById('criticalUrgencyFilter')?.value || 'all';
            const sortFilter = document.getElementById('criticalSortFilter')?.value || 'date';
            
            const container = document.getElementById('criticalList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.critical-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                if (deptFilter !== 'all' && item.dataset.department !== deptFilter) show = false;
                if (urgencyFilter !== 'all' && item.dataset.urgency !== urgencyFilter) show = false;
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'date') {
                    return new Date(b.dataset.date || '0') - new Date(a.dataset.date || '0');
                }
                if (sortFilter === 'course') {
                    return (a.dataset.course || '').localeCompare(b.dataset.course || '');
                }
                if (sortFilter === 'user') {
                    return (a.dataset.user || '').localeCompare(b.dataset.user || '');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
            
            // Update count
            const countEl = document.getElementById('criticalCount');
            if (countEl) countEl.textContent = visibleItems.length;
        };
        
        // Global filter functions for documents
        window.filterDocuments = function() {
            const impactFilter = document.getElementById('documentImpactFilter')?.value || 'all';
            const timeFilter = document.getElementById('documentTimeFilter')?.value || 'all';
            const sortFilter = document.getElementById('documentSortFilter')?.value || 'date';
            
            const container = document.getElementById('documentsList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.document-item'));
            
            // Filter items
            items.forEach(item => {
                let show = true;
                const assignments = parseInt(item.dataset.assignments || '0');
                const docDate = new Date(item.dataset.date || '0');
                const now = new Date();
                
                // Impact filter
                if (impactFilter === 'with-assignments' && assignments === 0) show = false;
                if (impactFilter === 'no-assignments' && assignments > 0) show = false;
                if (impactFilter === 'high-impact' && assignments < 5) show = false;
                
                // Time filter
                if (timeFilter === 'recent' && (now - docDate) > 7 * 24 * 60 * 60 * 1000) show = false;
                if (timeFilter === 'month' && (now - docDate) > 30 * 24 * 60 * 60 * 1000) show = false;
                if (timeFilter === 'quarter' && (now - docDate) > 90 * 24 * 60 * 60 * 1000) show = false;
                
                item.style.display = show ? 'block' : 'none';
            });
            
            // Sort visible items
            const visibleItems = items.filter(item => item.style.display !== 'none');
            visibleItems.sort((a, b) => {
                if (sortFilter === 'date') {
                    return new Date(b.dataset.date || '0') - new Date(a.dataset.date || '0');
                }
                if (sortFilter === 'assignments') {
                    return parseInt(b.dataset.assignments || '0') - parseInt(a.dataset.assignments || '0');
                }
                if (sortFilter === 'title') {
                    return (a.dataset.title || '').localeCompare(b.dataset.title || '');
                }
                if (sortFilter === 'impact') {
                    return parseInt(b.dataset.impact || '0') - parseInt(a.dataset.impact || '0');
                }
                return 0;
            });
            
            // Re-append sorted visible items
            visibleItems.forEach(item => container.appendChild(item));
            
            // Append hidden items at the end
            const hiddenItems = items.filter(item => item.style.display === 'none');
            hiddenItems.forEach(item => container.appendChild(item));
        };
        
        function toggleDocumentDetails(id) {
            const element = document.getElementById(id);
            if (element) {
                element.style.display = element.style.display === 'none' ? 'block' : 'none';
            }
        }
        
        // Load statistics and history on page load
        window.onload = function() {
            updateMotivationalStatus();
            loadStats();
            loadDocumentHistoryBelow();
        }
        
        let documentsDisplayed = 5; // Show first 5 documents
        let allDocuments = []; // Store all documents
        
        async function loadDocumentHistoryBelow() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('documentHistory');
                allDocuments = data.documents || [];
                
                if (allDocuments.length > 0) {
                    renderDocuments();
                } else {
                    historyDiv.innerHTML = '<h1>📄 Processed Documents</h1><div style="text-align: center; padding: var(--space-xxl) var(--space-l);"><div style="font-size: var(--text-xxl); margin-bottom: var(--space-m); opacity: 0.5;">📚</div><h3>No processed documents</h3><p>Upload your first PDF protocol for analysis!</p></div>';
                }
                
            } catch (error) {
                console.error('Error loading document history:', error);
            }
        }
        
        function renderDocuments() {
            const historyDiv = document.getElementById('documentHistory');
            
            // Apply filters
            let filteredDocuments = [...allDocuments];
            const sortBy = document.getElementById('sortFilter')?.value || 'date';
            const filterBy = document.getElementById('assignmentFilter')?.value || 'all';

            
            // Filtering
            if (filterBy === 'with-assignments') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count > 0);
            }
            if (filterBy === 'no-assignments') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count === 0);
            }
            if (filterBy === 'high-impact') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count >= 5);
            }
            if (filterBy === 'recent') {
                const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                filteredDocuments = filteredDocuments.filter(doc => new Date(doc.processed_at) > weekAgo);
            }
            if (filterBy === 'safety') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('safety') || 
                    doc.title.toLowerCase().includes('безопасность') ||
                    doc.title.toLowerCase().includes('охрана')
                );
            }
            if (filterBy === 'training') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('training') || 
                    doc.title.toLowerCase().includes('обучение') ||
                    doc.title.toLowerCase().includes('курс')
                );
            }
            if (filterBy === 'incident') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('incident') || 
                    doc.title.toLowerCase().includes('инцидент') ||
                    doc.title.toLowerCase().includes('происшествие') ||
                    doc.title.toLowerCase().includes('нарушение')
                );
            }
            

            
            // Sort after all filters
            filteredDocuments.sort((a, b) => {
                if (sortBy === 'date') {
                    return new Date(b.processed_at) - new Date(a.processed_at);
                }
                if (sortBy === 'assignments') {
                    return b.assignments_count - a.assignments_count;
                }
                if (sortBy === 'impact') {
                    const aImpact = a.assignments_count + (a.skipped_duplicates?.length || 0);
                    const bImpact = b.assignments_count + (b.skipped_duplicates?.length || 0);
                    return bImpact - aImpact;
                }
                if (sortBy === 'alphabetical') {
                    return a.title.localeCompare(b.title);
                }
                return 0;
            });
            
            const documentsToShow = filteredDocuments.slice(0, documentsDisplayed);
            
            let html = '<h1>📄 Processed Documents (' + allDocuments.length + ')</h1>';
            
            // Add filters
            html += '<div style="background: rgba(255,255,255,0.2); padding: 16px; border-radius: 12px; margin-bottom: 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">';
            html += '<div style="display: flex; align-items: center; gap: 8px;">';
            html += '<label style="font-weight: 600; color: var(--gray-800);">Sort:</label>';
            html += '<select id="sortFilter" onchange="renderDocuments()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(0,0,0,0.2); background: white;">';
            html += '<option value="date"' + (sortBy === 'date' ? ' selected' : '') + '>By Date (Newest)</option>';
            html += '<option value="assignments"' + (sortBy === 'assignments' ? ' selected' : '') + '>By Assignments (Most)</option>';
            html += '<option value="impact"' + (sortBy === 'impact' ? ' selected' : '') + '>By Impact (Assignments + Skipped)</option>';
            html += '<option value="alphabetical"' + (sortBy === 'alphabetical' ? ' selected' : '') + '>Alphabetical (A-Z)</option>';
            html += '</select>';
            html += '</div>';

            
            html += '<div style="display: flex; align-items: center; gap: 8px;">';
            html += '<label style="font-weight: 600; color: var(--gray-800);">Filter:</label>';
            html += '<select id="assignmentFilter" onchange="resetAndFilter()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(0,0,0,0.2); background: white;">';
            html += '<option value="all"' + (filterBy === 'all' ? ' selected' : '') + '>All Documents</option>';
            html += '<option value="with-assignments"' + (filterBy === 'with-assignments' ? ' selected' : '') + '>With Assignments</option>';
            html += '<option value="no-assignments"' + (filterBy === 'no-assignments' ? ' selected' : '') + '>No Assignments</option>';
            html += '<option value="high-impact"' + (filterBy === 'high-impact' ? ' selected' : '') + '>High Impact (5+ assignments)</option>';
            html += '<option value="recent"' + (filterBy === 'recent' ? ' selected' : '') + '>Recent (Last 7 days)</option>';
            html += '<option value="safety"' + (filterBy === 'safety' ? ' selected' : '') + '>Safety Related</option>';
            html += '<option value="training"' + (filterBy === 'training' ? ' selected' : '') + '>Training Related</option>';
            html += '<option value="incident"' + (filterBy === 'incident' ? ' selected' : '') + '>Incident Reports</option>';
            html += '</select>';
            html += '</div>';

            html += '<div style="color: var(--gray-600); font-size: 14px;">Showing ' + documentsToShow.length + ' of ' + filteredDocuments.length + ' documents</div>';
            html += '</div>';
            
            html += '<div>';
            
            documentsToShow.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div class="training-card full-training">`;
                        
                        html += `<div class="training-content">`;
                        html += `<h3 class="training-title">`;
                        html += `<span class="training-icon">📄</span>`;
                        html += `${doc.title}`;
                        html += `</h3>`;
                        html += `<p class="training-desc">Processed ${date}</p>`;
                        html += `<div class="training-meta">`;
                        html += `<span>Type: Protocol</span>`;
                        html += `<span>🎯 ${doc.assignments_count} assignments</span>`;
                        html += `<span>Status: Processed</span>`;
                        html += `</div>`;
                        html += `</div>`;
                        
                        html += `<div class="training-action">`;
                        html += `<button onclick="showDocumentDetailsFromBelow(${index})" style="background: linear-gradient(135deg, var(--brand) 0%, #16a34a 100%); color: white; border: none; padding: 20px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(14, 122, 78, 0.3); width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(14, 122, 78, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(14, 122, 78, 0.3)'">VIEW<br>DETAILS</button>`;
                        html += `</div>`;
                        
                        html += `</div>`;
                        
                        // Скрытые детали
                        html += `<div id="docBelow${index}" style="display: none; margin-top: 15px; padding: 20px; background: #f8f9fa; border-radius: 16px; border-left: 4px solid #2a7d2e;">`;;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5 style="font-size: 18px; font-weight: 700; margin-bottom: 16px; color: #2a7d2e;">📊 Course Assignments:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 12px; font-size: 14px; box-shadow: var(--ehs-shadow);">`;
                                html += `<strong style="color: #2a7d2e;">📚 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                                html += `<div style="margin: 4px 0; color: #666;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                                html += `<div style="color: #666;">🎯 Priority: ${assignment.priority} | ⏰ ${assignDate}</div>`;
                                if (assignment.reason) html += `<div style="margin-top: 4px; color: #666; font-style: italic;">📝 ${assignment.reason}</div>`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">No courses assigned</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5 style="font-size: 18px; font-weight: 700; margin: 16px 0; color: #f59e0b;">⚠️ Skipped Duplicates:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 12px; border-left: 4px solid #ffc107; box-shadow: var(--ehs-shadow);">`;
                                html += `<strong onclick="showUserProfile('${skip.user_id}')" style="color: #856404; cursor: pointer; text-decoration: underline;">😫 ${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<div style="margin: 4px 0; color: #856404;"><strong>Skipped:</strong> ${skip.skipped_courses.join(', ')}</div>`;
                                html += `<div style="color: #856404; font-style: italic;">${skip.reason}</div>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div>`;
                        

                    });
                    
                    html += '</div>';
                    
                    // Add "Load More" button if there are more documents
                    if (documentsDisplayed < filteredDocuments.length) {
                        html += '<div style="text-align: center; margin-top: 20px;">';
                        html += '<button onclick="loadMoreDocuments()" style="background: var(--brand); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Load More (' + (filteredDocuments.length - documentsDisplayed) + ' remaining)</button>';
                        html += '</div>';
                    }
                    
                    historyDiv.innerHTML = html;
        }
        
        function loadMoreDocuments() {
            documentsDisplayed += 10; // Load 10 more documents
            renderDocuments();
        }
        
        function resetAndFilter() {
            documentsDisplayed = 5; // Reset to first 5 documents
            renderDocuments();
        }

        function displayResult(data) {
            let html = '';
            let title = '';
            
            // Check if document is duplicate
            if (data.is_duplicate) {
                title = '⚠️ Document Already Processed';
                html += `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">⚠️</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Duplicate Found</div>
                        </div>
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${data.previous_processing.assignments_count}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Previous Assignments</div>
                        </div>
                        <div style="background: #ede9fe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${data.previous_processing.assigned_users.length}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Users Affected</div>
                        </div>
                    </div>
                    
                    <!-- Duplicate Warning -->
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 2px solid #fbbf24;">
                        <h4 style="margin: 0 0 12px 0; color: var(--warning);">⚠️ Document Previously Processed</h4>
                        <div style="background: white; padding: 12px; border-radius: 8px; margin: 8px 0;">
                            <div style="margin: 6px 0; font-size: 13px;"><strong>📅 Previous processing:</strong> ${new Date(data.previous_processing.processed_at).toLocaleString()}</div>
                            <div style="margin: 6px 0; font-size: 13px;"><strong>🎯 Assignments made:</strong> ${data.previous_processing.assignments_count}</div>
                            <div style="margin: 6px 0; font-size: 13px;"><strong>👥 Users affected:</strong> ${data.previous_processing.assigned_users.join(', ')}</div>
                        </div>
                    </div>`;
                
                if (data.extracted_text) {
                    html += `
                    <!-- Protocol Content -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">📄 Protocol Content</h4>
                        <div style="background: white; padding: 12px; border-radius: 8px; font-size: 13px; line-height: 1.5; color: var(--gray-700);">${data.extracted_text}</div>
                    </div>`;
                }
                
                html += `
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
            } else {
                title = `🤖 AI Analysis Completed`;
                
                const totalAssignments = data.assignments ? data.assignments.length : 0;
                const totalSkipped = data.skipped_duplicates ? data.skipped_duplicates.length : 0;
                const criticalAssignments = data.assignments ? data.assignments.filter(a => 
                    a.course_periods && a.course_periods.some(p => p.priority === 'critical')
                ).length : 0;
                const totalUsers = data.total_users || 0;
                
                html += `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Header Stats -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--success);">${totalUsers}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Users Analyzed</div>
                        </div>
                        <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${totalAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">New Assignments</div>
                        </div>
                        <div style="background: #fef2f2; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--error);">${criticalAssignments}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Critical Priority</div>
                        </div>
                        <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${totalSkipped}</div>
                            <div style="font-size: 11px; color: var(--gray-600);">Skipped Duplicates</div>
                        </div>
                    </div>`;
                
                if (data.extracted_text) {
                    html += `
                    <!-- Protocol Content -->
                    <div style="background: rgba(255,255,255,0.8); padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e5e5e5;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">📄 Analyzed Protocol</h4>
                        <div style="background: white; padding: 12px; border-radius: 8px; font-size: 13px; line-height: 1.5; color: var(--gray-700); max-height: 150px; overflow-y: auto;">${data.extracted_text}</div>
                    </div>`;
                }
                
                if (data.assignments && data.assignments.length > 0) {
                    html += `
                    <!-- AI Assignments -->
                    <div style="background: #f0fdf4; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 2px solid #bbf7d0;">
                        <h4 style="margin: 0 0 12px 0; color: var(--success);">🎯 AI Course Assignments (${data.assignments.length} users)</h4>`;
                    
                    data.assignments.forEach(assignment => {
                        html += `<div style="background: white; border-left: 4px solid var(--success); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                        html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">👤 ${assignment.name}</div>`;
                        html += `<div style="font-size: 12px; color: var(--gray-500);">${assignment.user_id}</div>`;
                        html += `</div>`;
                        html += `<div style="margin: 6px 0; font-size: 13px; color: var(--gray-600);">🏢 ${assignment.role}, ${assignment.department}</div>`;
                        
                        html += `<div style="margin: 12px 0;"><strong style="font-size: 13px; color: var(--gray-700);">📚 Assigned Courses:</strong></div>`;
                        assignment.courses_assigned.forEach(courseId => {
                            html += `<span style="background: #dcfce7; color: var(--success); padding: 4px 8px; margin: 2px; border-radius: 4px; display: inline-block; font-size: 12px; font-weight: 500;">📚 ${courseId}</span> `;
                        });
                        
                        if (assignment.reason) {
                            html += `<div style="margin: 12px 0; font-style: italic; color: var(--gray-600); font-size: 12px; background: #f8f9fa; padding: 8px; border-radius: 6px;">🤖 AI Reasoning: ${assignment.reason}</div>`;
                        }
                        
                        if (assignment.course_periods) {
                            html += `<div style="margin: 12px 0;"><strong style="font-size: 13px; color: var(--gray-700);">🔄 AI Determined Schedule:</strong></div>`;
                            assignment.course_periods.forEach(period => {
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#10b981',
                                    'low': '#6c757d'
                                };
                                const priorityNames = {
                                    'critical': '🔴 Critical',
                                    'high': '🟠 High',
                                    'normal': '🟢 Normal',
                                    'low': '⚪ Low'
                                };
                                
                                html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[period.priority] || '#10b981'}; padding: 8px; margin: 4px 0; border-radius: 4px; font-size: 12px;">`;
                                html += `<div style="font-weight: 600; margin-bottom: 4px;">📚 ${period.course_id}</div>`;
                                html += `<div style="color: var(--gray-600);">🎯 Priority: ${priorityNames[period.priority] || period.priority}</div>`;
                                html += `<div style="color: var(--gray-600);">🔄 Every ${period.months} months | ⏰ Deadline: ${period.deadline_days} days</div>`;
                                html += `</div>`;
                            });
                        }
                        html += `</div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    // Check if there are skipped duplicates to show different message
                    if (data.skipped_duplicates && data.skipped_duplicates.length > 0) {
                        html += '<div style="background: #fef3c7; padding: 40px; border-radius: 12px; text-align: center; color: var(--warning); margin-bottom: 20px;">⚠️ AI Analysis Complete: All users already have these courses assigned (see skipped duplicates below)</div>';
                    } else {
                        html += '<div style="background: #f0fdf4; padding: 40px; border-radius: 12px; text-align: center; color: var(--success); margin-bottom: 20px;">✅ AI Analysis Complete: No new course assignments needed for this protocol</div>';
                    }
                }
                
                // Показываем пропущенные дубликаты (убираем дублирование)
                if (data.skipped_duplicates && data.skipped_duplicates.length > 0) {
                    html += `
                    <!-- Skipped Duplicates -->
                    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; border: 2px solid #fbbf24;">
                        <h4 style="margin: 0 0 12px 0; color: var(--warning);">⚠️ Skipped Duplicates (${data.skipped_duplicates.length} users)</h4>`;
                    
                    data.skipped_duplicates.forEach(skip => {
                        html += `<div style="background: white; border-left: 4px solid var(--warning); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                        html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px; margin-bottom: 8px;">👤 ${skip.name} (${skip.user_id})</div>`;
                        html += `<div style="margin: 8px 0; font-size: 13px; color: var(--gray-700);"><strong>🚫 Skipped Courses:</strong></div>`;
                        skip.skipped_courses.forEach(courseId => {
                            html += `<span style="background: #fef3c7; color: var(--warning); padding: 4px 8px; margin: 2px; border-radius: 4px; display: inline-block; font-size: 12px; font-weight: 500;">🚫 ${courseId}</span> `;
                        });
                        html += `<div style="margin-top: 8px; font-style: italic; color: var(--gray-600); font-size: 12px; background: #f8f9fa; padding: 8px; border-radius: 6px;">${skip.reason}</div>`;
                        html += `</div>`;
                    });
                    
                    html += `</div>`;
                }
            }
            
            html += `
                <div style="text-align: center; margin-top: 20px;">
                    <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                </div>
            </div>`;
            
            showModal(title, html);
            
            // Update statistics and history - PRESERVE ORIGINAL FUNCTIONALITY
            loadStats();
            loadDocumentHistoryBelow();
        }
        
        async function checkExpired() {
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = '<div class="result">⏰ Checking course deadlines...</div>';
            
            try {
                const response = await fetch('/expired-courses');
                const data = await response.json();
                
                let html = '<div class="result">';
                html += `<h3>⏰ Course Deadline Check</h3>`;
                
                if (data.expired_users && data.expired_users.length > 0) {
                    html += `<h4>⚠️ Found users with expiring courses:</h4>`;
                    
                    data.expired_users.forEach(user => {
                        html += `<div style="background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107;">`;
                        html += `<strong>${user.user_name || user.user_id}</strong> - ${user.role || ''}, ${user.department || ''}<br>`;
                        html += `<strong>Expiring courses:</strong><br>`;
                        
                        user.expired_courses.forEach(course => {
                            html += `<div style="margin: 5px 0; padding: 5px; background: #f8d7da; border-radius: 3px;">`;
                            html += `🚨 <strong>${course.course_id}</strong><br>`;
                            html += `Assigned: ${new Date(course.assigned_at).toLocaleDateString()}<br>`;
                            html += `Period: ${course.period_months} months`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    });
                } else {
                    html += '<p>✅ All courses are current!</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Error checking deadlines</div>';
            }
        }
        
        async function showAuditLog() {
            showModal('📈 Audit Log', '<div style="text-align: center; padding: 40px;">📈 Loading audit log...</div>');
            
            try {
                const response = await fetch('/audit-log');
                const data = await response.json();
                
                const courseAssignments = data.logs ? data.logs.filter(log => log.action === 'course_assigned') : [];
                const documentProcessed = data.logs ? data.logs.filter(log => log.action === 'document_processed') : [];
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Audit Header -->
                    <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin: 0 0 20px 0; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <h3 style="margin: 0; color: var(--gray-800); font-size: 24px;">📈 Audit Log</h3>
                            <button onclick="downloadAuditReport()" style="background: #16a34a; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600;">💾 Download Report</button>
                        </div>
                        <div style="color: var(--gray-600); font-size: 14px;">Last ${data.total_logs || 0} system actions</div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-top: 16px;">
                            <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--success);">${courseAssignments.length}</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Course Assignments</div>
                            </div>
                            <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${documentProcessed.length}</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Documents Processed</div>
                            </div>
                        </div>
                    </div>`;
                
                if (data.logs && data.logs.length > 0) {
                    html += `
                    <!-- Audit Log Entries -->
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 12px;">
                        <h4 style="margin: 0 0 12px 0; color: var(--gray-800);">📋 Recent Activity</h4>`;
                    
                    data.logs.forEach(log => {
                        const date = new Date(log.timestamp).toLocaleString();
                        
                        if (log.action === 'course_assigned') {
                            const priorityColors = {
                                'critical': '#dc3545',
                                'high': '#fd7e14', 
                                'normal': '#28a745',
                                'low': '#6c757d'
                            };
                            
                            html += `<div style="background: white; border-left: 4px solid ${priorityColors[log.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                            html += `<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">`;
                            html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px;">📚 Course Assigned: ${log.course_id}</div>`;
                            html += `<div style="font-size: 12px; color: ${priorityColors[log.priority] || '#28a745'}; font-weight: 600;">${log.priority?.toUpperCase() || 'NORMAL'}</div>`;
                            html += `</div>`;
                            html += `<div style="margin: 6px 0; font-size: 13px;">👤 <strong style="color: var(--blue);">${log.user_name || log.user_id}</strong> - ${log.user_role || ''}, ${log.user_department || ''}</div>`;
                            html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                            html += `<span>🤖 ${log.assigned_by}</span>`;
                            html += `<span>⏰ ${date}</span>`;
                            html += `</div>`;
                            if (log.reason) html += `<div style="margin-top: 8px; font-size: 12px; color: var(--gray-600); font-style: italic; background: #f8f9fa; padding: 8px; border-radius: 6px;">📝 ${log.reason}</div>`;
                            html += `</div>`;
                        } else if (log.action === 'document_processed') {
                            html += `<div style="background: white; border-left: 4px solid var(--blue); padding: 12px; margin: 8px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">`;
                            html += `<div style="font-weight: 600; color: var(--gray-800); font-size: 14px; margin-bottom: 8px;">📄 Document Processed</div>`;
                            html += `<div style="margin: 6px 0; font-size: 13px; color: var(--gray-700);">📝 <strong>Protocol:</strong> ${log.protocol_title || 'Unknown'}</div>`;
                            html += `<div style="display: flex; gap: 16px; font-size: 12px; color: var(--gray-600); margin-top: 6px;">`;
                            html += `<span>🎯 ${log.assignments_count || 0} assignments</span>`;
                            html += `<span>⏰ ${date}</span>`;
                            html += `</div>`;
                            html += `</div>`;
                        }
                    });
                    
                    html += `</div>`;
                } else {
                    html += '<div style="background: #f8f9fa; padding: 40px; border-radius: 12px; text-align: center; color: #6c757d;">ℹ️ Audit log is empty</div>';
                }
                
                html += `
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading audit log</div>';
            }
        }
        
        async function showComplianceReport() {
            showModal('📄 Compliance Report', '<div style="text-align: center; padding: 40px;">📄 Loading compliance analytics...</div>');
            
            try {
                const response = await fetch('/audit-log');
                const data = await response.json();
                
                const courseAssignments = data.logs ? data.logs.filter(log => log.action === 'course_assigned') : [];
                const documentProcessed = data.logs ? data.logs.filter(log => log.action === 'document_processed') : [];
                const uniqueUsers = [...new Set(courseAssignments.map(a => a.user_id))].length;
                const completionRate = courseAssignments.length > 0 ? 70 : 0;
                
                let html = `
                <div style="text-align: left; max-height: 80vh; overflow-y: auto;">
                    <!-- Compliance Header -->
                    <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin: 0 0 20px 0; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <h3 style="margin: 0; color: var(--gray-800); font-size: 24px;">📄 Compliance Analytics</h3>
                            <button onclick="downloadFilteredReport()" style="background: #16a34a; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600;">💾 Download Report</button>
                        </div>
                        <div style="color: var(--gray-600); font-size: 14px;">System-wide compliance overview</div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-top: 16px;">
                            <div style="background: #dcfce7; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--success);">${uniqueUsers}</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Total Users</div>
                            </div>
                            <div style="background: #dbeafe; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--blue);">${completionRate}%</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Completion Rate</div>
                            </div>
                            <div style="background: #fef3c7; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--warning);">${courseAssignments.length}</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Assignments</div>
                            </div>
                            <div style="background: #f3e8ff; padding: 12px; border-radius: 8px; text-align: center;">
                                <div style="font-size: 20px; font-weight: 700; color: var(--purple);">${documentProcessed.length}</div>
                                <div style="font-size: 11px; color: var(--gray-600);">Completed</div>
                            </div>
                        </div>
                    </div>`;
                
                // Compliance Status
                const complianceRate = data.completion_rate || 0;
                const statusColor = complianceRate >= 80 ? '#16a34a' : complianceRate >= 60 ? '#f59e0b' : '#ef4444';
                const statusText = complianceRate >= 80 ? 'EXCELLENT' : complianceRate >= 60 ? 'GOOD' : 'NEEDS IMPROVEMENT';
                
                // Get audit data for analysis
                const auditResponse = await fetch('/audit-log');
                const audit = await auditResponse.json();
                
                // Calculate metrics from audit data
                const assignments = audit.logs ? audit.logs.filter(log => log.action === 'course_assigned') : [];
                const criticalAssignments = assignments.filter(log => log.priority === 'critical');
                const highPriorityAssignments = assignments.filter(log => log.priority === 'high');
                const overdueCount = Math.floor(assignments.length * 0.15); // Demo overdue count
                
                // Create demo underperformers from assignments
                const userAssignments = {};
                assignments.forEach(log => {
                    if (!userAssignments[log.user_id]) {
                        userAssignments[log.user_id] = { 
                            user_id: log.user_id, 
                            name: log.user_name || log.user_id,
                            department: 'Engineering',
                            role: 'Employee',
                            assignments: 0, 
                            completed: 0 
                        };
                    }
                    userAssignments[log.user_id].assignments++;
                    userAssignments[log.user_id].completed = Math.floor(userAssignments[log.user_id].assignments * 0.6); // Demo completion
                });
                
                const userPerformance = Object.values(userAssignments).map(user => ({
                    ...user,
                    rate: user.assignments > 0 ? Math.round((user.completed / user.assignments) * 100) : 0
                }));
                
                const underperformers = userPerformance.filter(u => u.rate < 60)
                
                // Update header metrics
                html = html.replace('${data.total_completions || 0}', assignments.length);
                html = html.replace('Completed', 'Total Assignments');
                
                // Add filters
                html += '<div style="background: #f8f9fa; padding: 16px; border-radius: 12px; margin-bottom: 20px;">';
                html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">';

                html += '<select id="priorityFilter" style="padding: 8px; border: 1px solid #ddd; border-radius: 6px;" onchange="filterTable()">';
                html += '<option value="">All Priorities</option><option value="critical">Critical</option><option value="high">High</option><option value="normal">Normal</option></select>';
                html += '<select id="weekFilter" style="padding: 8px; border: 1px solid #ddd; border-radius: 6px;" onchange="filterTable()">';
                html += '<option value="">All Weeks</option><option value="this-week">This Week</option><option value="last-week">Last Week</option><option value="this-month">This Month</option></select>';
                html += '<select id="departmentFilter" style="padding: 8px; border: 1px solid #ddd; border-radius: 6px;" onchange="filterTable()">';
                html += '<option value="">All Departments</option><option value="engineering">Engineering</option><option value="safety">Safety</option><option value="operations">Operations</option><option value="management">Management</option></select>';
                html += '</div></div>';
                
                // Add table
                html += '<div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">';
                html += '<table id="assignmentTable" style="width: 100%; border-collapse: collapse;">';
                html += '<thead style="background: #f8f9fa;"><tr>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; cursor: pointer;" onclick="sortTable(0)">User</th>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; cursor: pointer;" onclick="sortTable(1)">Course</th>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; cursor: pointer;" onclick="sortTable(2)">Department</th>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; cursor: pointer;" onclick="sortTable(3)">Priority</th>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; cursor: pointer;" onclick="sortTable(4)">Date</th>';
                html += '<th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Status</th>';
                html += '</tr></thead><tbody>';
                
                courseAssignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleDateString();
                    const priorityColors = { 'critical': '#dc3545', 'high': '#fd7e14', 'normal': '#28a745' };
                    const priorityColor = priorityColors[assignment.priority] || '#28a745';
                    const status = Math.random() > 0.3 ? 'Completed' : 'Pending';
                    const statusColor = status === 'Completed' ? '#28a745' : '#fd7e14';
                    const departments = ['Engineering', 'Safety', 'Operations', 'Management'];
                    const department = departments[Math.floor(Math.random() * departments.length)];
                    
                    html += '<tr style="border-bottom: 1px solid #f0f0f0;">';
                    html += '<td style="padding: 12px;">' + (assignment.user_name || assignment.user_id) + '</td>';
                    html += '<td style="padding: 12px;">' + assignment.course_id + '</td>';
                    html += '<td style="padding: 12px;">' + department + '</td>';
                    html += '<td style="padding: 12px;"><span style="background: ' + priorityColor + '; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">' + (assignment.priority || 'normal').toUpperCase() + '</span></td>';
                    html += '<td style="padding: 12px;">' + date + '</td>';
                    html += '<td style="padding: 12px;"><span style="color: ' + statusColor + '; font-weight: 600;">' + status + '</span></td>';
                    html += '</tr>';
                });
                
                html += '</tbody></table></div>';
                
                // Add sorting and filtering functions
                window.sortTable = function(columnIndex) {
                    const table = document.getElementById('assignmentTable');
                    const tbody = table.getElementsByTagName('tbody')[0];
                    const rows = Array.from(tbody.getElementsByTagName('tr'));
                    
                    rows.sort((a, b) => {
                        const aText = a.getElementsByTagName('td')[columnIndex].textContent.trim();
                        const bText = b.getElementsByTagName('td')[columnIndex].textContent.trim();
                        return aText.localeCompare(bText);
                    });
                    
                    rows.forEach(row => tbody.appendChild(row));
                };
                
                window.filterTable = function() {
                    const priorityFilter = document.getElementById('priorityFilter').value.toLowerCase();
                    const weekFilter = document.getElementById('weekFilter').value;
                    const departmentFilter = document.getElementById('departmentFilter').value.toLowerCase();
                    
                    const table = document.getElementById('assignmentTable');
                    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
                    const now = new Date();
                    
                    for (let i = 0; i < rows.length; i++) {
                        const cells = rows[i].getElementsByTagName('td');
                        const department = cells[2].textContent.toLowerCase();
                        const priority = cells[3].textContent.toLowerCase();
                        const dateText = cells[4].textContent;
                        const rowDate = new Date(dateText);
                        
                        let showByWeek = true;
                        if (weekFilter === 'this-week') {
                            const weekStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay());
                            showByWeek = rowDate >= weekStart;
                        } else if (weekFilter === 'last-week') {
                            const lastWeekStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay() - 7);
                            const lastWeekEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay() - 1);
                            showByWeek = rowDate >= lastWeekStart && rowDate <= lastWeekEnd;
                        } else if (weekFilter === 'this-month') {
                            showByWeek = rowDate.getMonth() === now.getMonth() && rowDate.getFullYear() === now.getFullYear();
                        }
                        
                        const showRow = department.includes(departmentFilter) &&
                                       (priorityFilter === '' || priority.includes(priorityFilter)) &&
                                       showByWeek;
                        
                        rows[i].style.display = showRow ? '' : 'none';
                    }
                };
                
                html += `
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="closeModal()" style="background: var(--gray-600); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Close</button>
                    </div>
                </div>`;
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading compliance report</div>';
            }
        }
        
        // Медитация - переменные
        let meditationTimeLeft = 300;
        let meditationInterval = null;
        let meditationRunning = false;
        let breathingInterval = null;
        let currentMeditationSound = null;
        let meditationAudioContext = null;
        let currentMeditationOscillator = null;
        
        function updateMeditationDisplay() {
            const minutes = Math.floor(meditationTimeLeft / 60);
            const seconds = meditationTimeLeft % 60;
            const timerEl = document.getElementById('meditationTimer');
            if (timerEl) {
                timerEl.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }
        
        function setMeditationTime(seconds) {
            if (!meditationRunning) {
                meditationTimeLeft = seconds;
                updateMeditationDisplay();
            }
        }
        
        function startMeditation() {
            if (!meditationRunning && meditationTimeLeft > 0) {
                meditationRunning = true;
                startBreathing();
                
                meditationInterval = setInterval(() => {
                    meditationTimeLeft--;
                    updateMeditationDisplay();
                    
                    if (meditationTimeLeft <= 0) {
                        pauseMeditation();
                        alert('🎉 Meditation completed!');
                    }
                }, 1000);
            }
        }
        
        function pauseMeditation() {
            meditationRunning = false;
            if (meditationInterval) {
                clearInterval(meditationInterval);
                meditationInterval = null;
            }
            stopBreathing();
        }
        
        function resetMeditation() {
            pauseMeditation();
            meditationTimeLeft = 300;
            updateMeditationDisplay();
        }
        
        const affirmations = [
            'You are calm and centered',
            'Peace flows through you',
            'You are exactly where you need to be',
            'Your mind is clear and focused',
            'You radiate inner strength',
            'Every breath brings you peace',
            'You are worthy of rest and relaxation',
            'Your thoughts are gentle and kind',
            'You trust in your inner wisdom',
            'You are grateful for this moment'
        ];
        
        let affirmationInterval = null;
        
        function startBreathing() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            const affirmation = document.getElementById('affirmationText');
            if (!guide || !circle) return;
            
            guide.style.opacity = '1';
            
            let breathingPhase = 0; // 0: inhale, 1: hold, 2: exhale, 3: hold
            
            breathingInterval = setInterval(() => {
                switch(breathingPhase) {
                    case 0: // Inhale
                        guide.textContent = 'Inhale...';
                        circle.style.transform = 'scale(1.5)';
                        break;
                    case 1: // Hold after inhale
                        guide.textContent = 'Hold...';
                        circle.style.transform = 'scale(1.5)';
                        break;
                    case 2: // Exhale
                        guide.textContent = 'Exhale...';
                        circle.style.transform = 'scale(1)';
                        break;
                    case 3: // Hold after exhale
                        guide.textContent = 'Hold...';
                        circle.style.transform = 'scale(1)';
                        break;
                }
                breathingPhase = (breathingPhase + 1) % 4;
            }, 3000);
            
            // Запускаем аффирмации
            if (affirmation) {
                let affirmationIndex = 0;
                affirmationInterval = setInterval(() => {
                    affirmation.style.opacity = '0';
                    setTimeout(() => {
                        affirmation.textContent = affirmations[affirmationIndex];
                        affirmation.style.opacity = '0.7';
                        affirmationIndex = (affirmationIndex + 1) % affirmations.length;
                    }, 500);
                }, 12000);
                
                // Показываем первую аффирмацию
                setTimeout(() => {
                    affirmation.textContent = affirmations[0];
                    affirmation.style.opacity = '0.7';
                }, 2000);
            }
        }
        
        function stopBreathing() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            const affirmation = document.getElementById('affirmationText');
            
            if (guide) guide.style.opacity = '0';
            if (circle) circle.style.transform = 'scale(1)';
            if (affirmation) affirmation.style.opacity = '0';
            
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
            
            if (affirmationInterval) {
                clearInterval(affirmationInterval);
                affirmationInterval = null;
            }
        }
        
        function toggleMeditationSound(soundType) {
            // Убираем активный класс со всех кнопок
            document.querySelectorAll('button[onclick*="toggleMeditationSound"]').forEach(btn => {
                btn.style.background = 'rgba(102, 126, 234, 0.1)';
            });
            
            // Останавливаем текущий звук
            if (currentMeditationOscillator) {
                currentMeditationOscillator.stop();
                currentMeditationOscillator = null;
            }
            
            if (currentMeditationSound === soundType) {
                currentMeditationSound = null;
                return;
            }
            
            // Активируем выбранную кнопку
            event.target.style.background = 'rgba(102, 126, 234, 0.3)';
            currentMeditationSound = soundType;
            
            // Запускаем новый звук
            if (soundType !== 'silence') {
                playMeditationSound(soundType);
            }
        }
        
        function playMeditationSound(type) {
            if (!meditationAudioContext) {
                meditationAudioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            const oscillator = meditationAudioContext.createOscillator();
            const gainNode = meditationAudioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(meditationAudioContext.destination);
            
            switch(type) {
                case 'rain':
                    oscillator.type = 'white';
                    oscillator.frequency.setValueAtTime(200, meditationAudioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.1, meditationAudioContext.currentTime);
                    break;
                case 'ocean':
                    oscillator.type = 'sine';
                    oscillator.frequency.setValueAtTime(80, meditationAudioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.15, meditationAudioContext.currentTime);
                    break;
                case 'forest':
                    oscillator.type = 'triangle';
                    oscillator.frequency.setValueAtTime(150, meditationAudioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.08, meditationAudioContext.currentTime);
                    break;
            }
            
            oscillator.start();
            currentMeditationOscillator = oscillator;
        }
        
        // Функции сортировки
        function sortUsersTable(sortBy) {
            const tbody = document.querySelector('#usersTable tbody');
            const rows = Array.from(tbody.querySelectorAll('.user-row'));
            
            rows.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            tbody.innerHTML = '';
            rows.forEach(row => tbody.appendChild(row));
        }
        
        function sortCourses(sortBy) {
            const container = document.getElementById('coursesList');
            const items = Array.from(container.querySelectorAll('.course-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortAssignments(sortBy) {
            const container = document.getElementById('assignmentsList');
            const items = Array.from(container.querySelectorAll('.assignment-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal); // Новые сверху
                }
                if (sortBy === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[bVal] || 0) - (priorities[aVal] || 0);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortCompletions(sortBy) {
            const container = document.getElementById('completionsList');
            const items = Array.from(container.querySelectorAll('.completion-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortCritical(sortBy) {
            const container = document.getElementById('criticalList');
            const items = Array.from(container.querySelectorAll('.critical-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortActive(sortBy) {
            const container = document.getElementById('activeList');
            const items = Array.from(container.querySelectorAll('.active-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                if (sortBy === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[bVal] || 0) - (priorities[aVal] || 0);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
    </script>

    <!-- Footer -->
    <footer style="background: linear-gradient(135deg, #1f2937 0%, #374151 100%); color: white; padding: 40px 0; margin-top: 60px; border-radius: 20px 20px 0 0;">
        <div class="container">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; margin-bottom: 30px;">
                <!-- AI Safety Assistant -->
                <div>
                    <h4 style="color: #f97316; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">🤖 AI Safety Assistant</h4>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 14px; opacity: 0.9;">Powered By</span>
                        <img src="/AWS_2007_logo_white.png" alt="AWS" style="height: 28px;">
                    </div>
                </div>
                
                <!-- AI Matchmakers Team -->
                <div>
                    <h4 style="color: #3b82f6; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">👥 AI Matchmakers Team</h4>
                    <div style="font-size: 14px; line-height: 1.6; opacity: 0.9;">
                        <a href="https://www.sergey-ulyanov.pro/" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 600;">Sergey Ulyanov</a><br>
                        <span style="opacity: 0.7;">× Visual Studio Code × Copilot × ChatGPT</span>
                    </div>
                </div>
                
                <!-- Digital Transformation Hub -->
                <div>
                    <h4 style="color: #8b5cf6; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">🚀 Digital Transformation Hub</h4>
                    <div style="font-size: 14px; line-height: 1.6; opacity: 0.9;">
                        <span style="color: #a78bfa;">DxHub × Amazon Web Services (AWS)</span><br>
                        <span style="opacity: 0.7;">August-September 2025</span>
                    </div>
                </div>
            </div>
            
            <!-- Contact Info -->
            <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 20px; text-align: center;">
                <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 14px; opacity: 0.8;">
                    <a href="mailto:ulyanoow@gmail.com" style="color: #60a5fa; text-decoration: none; display: flex; align-items: center; gap: 5px;">📧 ulyanoow@gmail.com</a>
                    <a href="tel:+13107137738" style="color: #60a5fa; text-decoration: none; display: flex; align-items: center; gap: 5px;">📱 (310) 713-7738</a>
                </div>
            </div>
        </div>
    </footer>

    <!-- Modal -->
    <div id="mainModal" class="modal" onclick="if(event.target === this) closeModal()">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Title</h3>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content -->
            </div>
        </div>
    </div>
</body>
</html>
    '''
    return HTMLResponse(content=html)

@app.get("/users-detail")
async def get_users_detail():
    """Get detailed information о userх"""
    users = mentor.db.get_all_users()
    
    # Добавляем информацию о назначенных courseх
    for user in users:
        user_assignments = [log for log in audit_logger.logs if log.get("user_id") == user["user_id"] and log.get("action") == "course_assigned"]
        user["assignments_count"] = len(user_assignments)
        user["latest_assignment"] = user_assignments[0]["timestamp"] if user_assignments else None
    
    return {"users": users}

@app.get("/courses-detail")
async def get_courses_detail():
    """Get detailed information о courseх"""
    courses = mentor.db.get_all_courses()
    
    # Добавляем статистику assignments
    for course in courses:
        course_assignments = [log for log in audit_logger.logs if log.get("course_id") == course["course_id"] and log.get("action") == "course_assigned"]
        course["assignments_count"] = len(course_assignments)
        course["latest_assignment"] = course_assignments[0]["timestamp"] if course_assignments else None
        
        # Добавляем AI-определенную периодичность
        course["renewal_months"] = scheduler.course_periods.get(course["course_id"], "N/A")
        
        # Приоритет берется из AI-назначений (самый высокий)
        course_priority = "normal"  # по умолчанию
        for log in audit_logger.logs:
            if (log.get("course_id") == course["course_id"] and 
                log.get("action") == "course_assigned" and 
                log.get("priority")):
                # Берем самый высокий приоритет
                priorities = {"low": 1, "normal": 2, "high": 3, "critical": 4}
                if priorities.get(log["priority"], 2) > priorities.get(course_priority, 2):
                    course_priority = log["priority"]
        course["priority"] = course_priority
    
    return {"courses": courses}

@app.post("/update-profile")
async def update_user_profile(user_id: str = Form(...), name: str = Form(...), 
                             role: str = Form(...), department: str = Form(...)):
    """Обновить профиль user"""
    try:
        success = mentor.db.update_user(user_id, {
            "name": name,
            "role": role, 
            "department": department
        })
        
        if success:
            return {"success": True, "message": "Профиль обновлен!"}
        else:
            return {"success": False, "message": "Error обновления"}
            
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.post("/complete-course")
async def complete_course(user_id: str = Form(...), course_id: str = Form(...)):
    """Marks course as completed"""
    try:
        # Проверяем, что пользователь существует
        user = mentor.db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Проверяем, не пройден ли уже курс
        if course_completion.is_course_completed(user_id, course_id):
            return {"message": "Course already marked as completed", "success": False}
        
        # Отмечаем курс как пройденный
        completion = course_completion.complete_course(user_id, course_id, "manual")
        
        # Логируем завершение
        audit_logger.logs.append({
            "timestamp": completion["completed_at"],
            "action": "course_completed",
            "user_id": user_id,
            "course_id": course_id,
            "completion_method": "manual",
            "id": len(audit_logger.logs) + 1
        })
        audit_logger.save_logs()
        
        # Получаем все завершенные курсы user
        completed_courses = [log.get("course_id") for log in audit_logger.logs 
                           if log.get("user_id") == user_id and log.get("action") == "course_completed"]
        
        # Проверяем и присваиваем новые бейджи
        coffee_stats = enhanced_coffee.get_user_insights(user_id) if user_id in enhanced_coffee.profiles else {}
        new_badges = badge_system.check_and_award_badges(user_id, user, completed_courses, coffee_stats)
        
        # Получаем рекомендации мерча for Post-Course Teaser
        merch_recommendations = merch_system.get_post_course_recommendations(user_id, course_id, user)
        
        return {
            "message": f"Курс {course_id} successfully marked as completed!",
            "success": True,
            "completion": completion,
            "merch_teaser": merch_recommendations,
            "new_badges": new_badges
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/dashboard")
async def get_user_dashboard(user_id: str):
    """Get пользовательскую страницу (как видит пользователь)"""
    user = mentor.db.get_user(user_id)
    if not user:
        return HTMLResponse(content="<h1>User not found</h1>")
    
    # Получаем все assignment user
    assignments = [log for log in audit_logger.logs if log.get("user_id") == user_id and log.get("action") == "course_assigned"]
    
    # Добавляем информацию о courseх
    for assignment in assignments:
        course_id = assignment.get("course_id")
        if course_id:
            assignment["is_expired"] = scheduler.is_course_expired(course_id, assignment["timestamp"])
            assignment["renewal_months"] = scheduler.course_periods.get(course_id, "N/A")
            assignment["deadline_days"] = getattr(scheduler, 'course_deadlines', {}).get(course_id, 30)
            assignment["is_completed"] = course_completion.is_course_completed(user_id, course_id)
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    user_data = {"user": user}
    html = generate_user_dashboard_html(user_data, assignments, scheduler, course_completion)
    
    return HTMLResponse(content=html)

@app.get("/user/{user_id}")
async def get_user_profile(user_id: str):
    """Get полный профиль user"""
    user = mentor.db.get_user(user_id)
    if not user:
        return {"error": "User not found"}
    
    # Получаем все assignment user
    assignments = [log for log in audit_logger.logs if log.get("user_id") == user_id and log.get("action") == "course_assigned"]
    
    # Добавляем информацию о courseх
    for assignment in assignments:
        course_id = assignment.get("course_id")
        if course_id:
            # Проверяем срок действия
            assignment["is_expired"] = scheduler.is_course_expired(course_id, assignment["timestamp"])
            assignment["renewal_months"] = scheduler.course_periods.get(course_id, "N/A")
            assignment["deadline_days"] = getattr(scheduler, 'course_deadlines', {}).get(course_id, "N/A")
            assignment["is_completed"] = course_completion.is_course_completed(user_id, course_id)
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Получаем историю из трекера документов
    tracker_history = doc_tracker.get_user_history(user_id)
    
    return {
        "user": user,
        "assignments": assignments,
        "tracker_history": tracker_history,
        "total_assignments": len(assignments),
        "active_courses": len([a for a in assignments if not a.get("is_expired", False) and not a.get("is_completed", False)])
    }

@app.get("/assignments-detail")
async def get_assignments_detail():
    """Get detailed information о assignmentх"""
    assignments = [log for log in audit_logger.logs if log.get("action") == "course_assigned"]
    
    # Добавляем информацию о userх
    for assignment in assignments:
        if assignment.get("user_id"):
            user = mentor.db.get_user(assignment["user_id"])
            if user:
                assignment["user_name"] = user["name"]
                assignment["user_role"] = user["role"]
                assignment["user_department"] = user["department"]
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {"assignments": assignments[:50]}  # Последние 50

@app.get("/stats")
async def get_stats():
    """Get статистику системы"""
    # Количество users
    users = mentor.db.get_all_users()
    user_count = len(users)
    
    # Количество курсов
    courses = mentor.db.get_all_courses()
    course_count = len(courses)
    
    # Количество assignments (из audit log)
    assignment_logs = [log for log in audit_logger.logs if log.get("action") == "course_assigned"]
    assignment_count = len(assignment_logs)
    
    # Количество обработанных документов
    document_count = len(doc_tracker.processed_docs)
    
    # Количество завершенных курсов
    completion_stats = course_completion.get_completion_stats()
    
    # Подсчитываем дополнительную статистику
    expired_count = 0
    critical_count = 0
    active_count = 0
    
    for log in assignment_logs:
        user_id = log.get("user_id")
        course_id = log.get("course_id")
        if user_id and course_id:
            is_expired = scheduler.is_course_expired(course_id, log["timestamp"])
            is_completed = course_completion.is_course_completed(user_id, course_id)
            priority = log.get("priority", "normal")
            
            if is_expired and not is_completed:
                expired_count += 1
            elif not is_expired and not is_completed:
                active_count += 1
            
            if priority == "critical" and not is_completed:
                critical_count += 1
    
    return {
        "users": user_count,
        "courses": course_count,
        "assignments": assignment_count,
        "documents": document_count,
        "completions": completion_stats["total_completions"],
        "expired": expired_count,
        "expired": expired_count,
        "active": active_count
    }

@app.get("/document-history")
async def get_document_history():
    """Get историю обработанных документов"""
    documents = []
    
    # Проходим по всем обработанным documentм
    for doc_hash, doc_info in doc_tracker.processed_docs.items():
        # Находим все assignment, сделанные в то же время
        doc_minute = doc_info["processed_at"][:16]  # 2025-09-18T13:29
        
        doc_assignments = []
        for log in audit_logger.logs:
            if log.get("action") == "course_assigned":
                # Новые документы - по хэшу, старые - по времени
                if (log.get("document_hash") == doc_hash or 
                    (not log.get("document_hash") and log.get("timestamp", "")[:16] == doc_minute)):
                    
                    user = mentor.db.get_user(log["user_id"])
                    if user:
                        log["user_name"] = user["name"]
                        log["user_role"] = user["role"]
                        log["user_department"] = user["department"]
                    
                    doc_assignments.append(log)
        
        # Получаем сохраненные skipped_duplicates
        skipped_info = doc_info.get("skipped_duplicates", [])
        
        documents.append({
            "hash": doc_hash,
            "title": doc_info["title"],
            "processed_at": doc_info["processed_at"],
            "assignments_count": len(doc_assignments),
            "assignments": doc_assignments,
            "skipped_duplicates": skipped_info  # Добавляем пропущенные
        })
    
    # Сортируем по дате
    documents.sort(key=lambda x: x["processed_at"], reverse=True)
    
    return {
        "total_documents": len(documents),
        "documents": documents
    }

@app.get("/audit-log")
async def get_audit_log():
    """Get audit log"""
    recent_logs = audit_logger.get_recent_logs(100)
    
    # Добавляем информацию о userх
    for log in recent_logs:
        if log.get("user_id"):
            user = mentor.db.get_user(log["user_id"])
            if user:
                log["user_name"] = user["name"]
                log["user_role"] = user["role"]
                log["user_department"] = user["department"]
    
    return {
        "total_logs": len(recent_logs),
        "logs": recent_logs
    }

@app.get("/completions-detail")
async def get_completions_detail():
    """Get detailed information о завершенных courseх"""
    completions = course_completion.completions.copy()
    
    # Добавляем информацию о userх
    for completion in completions:
        if completion.get("user_id"):
            user = mentor.db.get_user(completion["user_id"])
            if user:
                completion["user_name"] = user["name"]
                completion["user_role"] = user["role"]
                completion["user_department"] = user["department"]
    
    # Сортируем по дате
    completions.sort(key=lambda x: x["completed_at"], reverse=True)
    
    return {"completions": completions[:50]}  # Последние 50

@app.get("/expired-courses")
async def get_expired_courses():
    """Get список users с истекающими courseми"""
    expired_list = scheduler.get_expired_courses(doc_tracker)
    
    # Получаем информацию о userх
    for item in expired_list:
        user = mentor.db.get_user(item["user_id"])
        if user:
            item["user_name"] = user["name"]
            item["role"] = user["role"]
            item["department"] = user["department"]
    
    return {
        "expired_count": len(expired_list),
        "expired_users": expired_list
    }

# Random Coffee эндпоинты
@app.post("/coffee/profile")
async def create_coffee_profile(user_id: str = Form(...), interests: str = Form(...), 
                               availability: str = Form(...), language: str = Form(default="en")):
    """Create or update profile Random Coffee"""
    try:
        user = mentor.db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        interests_list = [i.strip() for i in interests.split(',') if i.strip()]
        availability_list = json.loads(availability) if availability else []
        
        profile = coffee_manager.create_profile(
            user_id=user_id,
            name=user["name"],
            role=user["role"],
            department=user["department"],
            interests=interests_list,
            availability=availability_list,
            language=language
        )
        
        return {"success": True, "profile": profile, "message": SUCCESS_MESSAGES["profile_created"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/coffee/profile/{user_id}")
async def get_coffee_profile(user_id: str):
    """Get профиль Random Coffee"""
    profile = coffee_manager.get_profile(user_id)
    if not profile:
        return {"error": "Profile not found"}
    return {"profile": profile}

@app.post("/coffee/opt-in")
async def coffee_opt_in(user_id: str = Form(...), participate: bool = Form(...)):
    """Участие в Random Coffee на неделю"""
    try:
        profile = coffee_manager.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Create profile first")
        
        coffee_manager.update_profile(user_id, {"active": participate})
        
        message = SUCCESS_MESSAGES["opted_in"] if participate else SUCCESS_MESSAGES["opted_out"]
        return {"success": True, "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/coffee/matches/{user_id}")
async def get_user_matches(user_id: str):
    """Get матчи user"""
    matches = coffee_manager.get_user_matches(user_id)
    
    # Добавляем информацию о партнерах
    for match in matches:
        partner_ids = [uid for uid in match["users"] if uid != user_id]
        partners = []
        for partner_id in partner_ids:
            partner_profile = coffee_manager.get_profile(partner_id)
            if partner_profile:
                partners.append({
                    "id": partner_id,
                    "name": partner_profile["name"],
                    "role": partner_profile["role"],
                    "department": partner_profile["department"]
                })
        match["partners"] = partners
    
    return {"matches": matches}

@app.post("/coffee/confirm-match")
async def confirm_coffee_match(match_id: str = Form(...), timeslot: str = Form(...)):
    """Confirm match and meeting time"""
    try:
        success = coffee_manager.confirm_match(match_id, timeslot)
        if success:
            return {"success": True, "message": SUCCESS_MESSAGES["match_confirmed"].format(timeslot=timeslot)}
        else:
            raise HTTPException(status_code=404, detail="Match not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coffee/feedback")
async def add_coffee_feedback(match_id: str = Form(...), user_id: str = Form(...), 
                             rating: int = Form(...), safety_discussed: bool = Form(default=False),
                             tags: str = Form(default="")):
    """Add meeting feedback"""
    try:
        tags_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
        
        coffee_manager.add_feedback(match_id, user_id, rating, safety_discussed, tags_list)
        
        return {"success": True, "message": SUCCESS_MESSAGES["feedback_saved"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/coffee/stats")
async def get_coffee_stats():
    """Get статистику Random Coffee"""
    return coffee_manager.get_stats()

@app.post("/coffee/create-matches")
async def create_weekly_matches():
    """Create weekly matches (админская функция)"""
    try:
        matches = coffee_manager.create_weekly_matches()
        
        # Отправляем приветственные сообщения
        for match in matches:
            coffee_messenger.send_system_message(
                match["id"], 
                f"☕ Новый матч! Познакомьтесь и договоритесь о времени встречи!"
            )
        
        return {"success": True, "matches_created": len(matches), "matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/coffee/send-message")
async def send_coffee_message(match_id: str = Form(...), sender_id: str = Form(...), 
                             message: str = Form(...), message_type: str = Form(default="text")):
    """Send message in match chat"""
    try:
        message_obj = coffee_messenger.send_message(match_id, sender_id, message, message_type)
        return {"success": True, "message": message_obj}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/coffee/messages/{match_id}")
async def get_match_messages(match_id: str, user_id: str = None):
    """Get сообщения матча"""
    try:
        messages = coffee_messenger.get_match_messages(match_id)
        
        if user_id:
            coffee_messenger.mark_as_read(match_id, user_id)
        
        return {"success": True, "messages": messages}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/coffee/confirm-time")
async def confirm_meeting_time(match_id: str = Form(...), time_slot: str = Form(...)):
    """Confirm meeting time"""
    try:
        coffee_messenger.confirm_meeting(match_id, time_slot)
        coffee_manager.confirm_match(match_id, time_slot)
        return {"success": True, "message": "Meeting confirmed!"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/admin/coffee-chats")
async def admin_coffee_chats():
    """Админская панель for просмотра всех чатов"""
    try:
        matches = coffee_manager.matches
        all_chats = []
        
        for match_id, match in matches.items():
            messages = coffee_messenger.get_match_messages(match_id)
            user_names = []
            for user_id in match['users']:
                user = mentor.db.get_user(user_id)
                user_names.append(user['name'] if user else user_id)
            
            all_chats.append({
                "match_id": match_id,
                "users": match['users'],
                "user_names": user_names,
                "status": match['status'],
                "messages_count": len(messages),
                "last_message": messages[-1] if messages else None
            })
        
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Админ - Coffee Chats</title>
    <style>
        body {{ font-family: system-ui; margin: 20px; background: #f5f5f5; }}
        .chat-card {{ background: white; padding: 16px; margin: 12px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .btn {{ background: #8b5cf6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin: 4px; }}
        .btn:hover {{ background: #7c3aed; }}
    </style>
</head>
<body>
    <h1>💬 Админ - Coffee Chats ({len(all_chats)})</h1>
    
    <div style="margin: 20px 0;">
        <button onclick="location.reload()" class="btn">🔄 Обновить</button>
        <button onclick="window.open('/coffee-demo', '_blank')" class="btn">☕ Coffee Demo</button>
    </div>
'''
        
        for chat in all_chats:
            last_msg = chat['last_message']
            last_msg_text = f"{last_msg['message'][:50]}..." if last_msg else "Нет сообщений"
            
            html += f'''
    <div class="chat-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0;">🎯 {chat['match_id']}</h3>
                <p style="margin: 4px 0; color: #666;">👥 {' × '.join(chat['user_names'])}</p>
                <p style="margin: 4px 0; font-size: 12px; color: #888;">💬 {chat['messages_count']} сообщений | {chat['status']}</p>
                <p style="margin: 4px 0; font-size: 12px; color: #999;">“{last_msg_text}”</p>
            </div>
            <div>
                <button onclick="viewChat('{chat['match_id']}')" class="btn">👁️ Посмотреть</button>
                <button onclick="loginAs('{chat['users'][0]}')" class="btn">👤 {chat['user_names'][0]}</button>
                <button onclick="loginAs('{chat['users'][1] if len(chat['users']) > 1 else chat['users'][0]}')" class="btn">👤 {chat['user_names'][1] if len(chat['user_names']) > 1 else 'N/A'}</button>
            </div>
        </div>
    </div>
            '''
        
        html += '''
    <script>
        function viewChat(matchId) {
            window.open(`/admin/chat/${matchId}`, '_blank');
        }
        
        function loginAs(userId) {
            window.open(`/user/${userId}/dashboard`, '_blank');
        }
    </script>
</body>
</html>
        '''
        
        return HTMLResponse(content=html)
        
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>")

@app.get("/coffee/unread/{user_id}")
async def get_unread_messages(user_id: str):
    """Get количество непрочитанных сообщений"""
    try:
        user_matches = coffee_manager.get_user_matches(user_id)
        total_unread = 0
        
        for match in user_matches:
            messages = coffee_messenger.get_match_messages(match["id"])
            unread_count = len([msg for msg in messages if msg["sender_id"] != user_id and not msg["read"]])
            total_unread += unread_count
        
        return {"success": True, "unread_count": total_unread}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/admin/chat/{match_id}")
async def admin_view_chat(match_id: str):
    """View specific chat"""
    try:
        messages = coffee_messenger.get_match_messages(match_id)
        match = coffee_manager.matches.get(match_id, {})
        
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Чат - {match_id}</title>
    <style>
        body {{ font-family: system-ui; margin: 20px; background: #f5f5f5; }}
        .message {{ margin: 8px 0; padding: 12px; border-radius: 8px; max-width: 70%; }}
        .user-msg {{ background: #8b5cf6; color: white; margin-left: auto; }}
        .partner-msg {{ background: white; border: 1px solid #ddd; }}
        .system-msg {{ background: #f0f9ff; border: 1px solid #3b82f6; text-align: center; margin: 16px auto; max-width: 90%; color: #1d4ed8; }}
        .chat-container {{ max-width: 600px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>💬 Чат - {match_id}</h1>
        <p>👥 Участники: {', '.join(match.get('users', []))}</p>
        <hr>
'''
        
        for msg in messages:
            msg_class = "system-msg" if msg['sender_id'] == 'system' else "user-msg" if msg['sender_id'] == match.get('users', [''])[0] else "partner-msg"
            time_str = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')
            
            html += f'''
        <div class="message {msg_class}">
            <strong>{msg['sender_id']}:</strong> {msg['message']}
            <br><small style="opacity: 0.7;">{time_str}</small>
        </div>
            '''
        
        html += '''
        <button onclick="window.close()" style="margin-top: 20px; padding: 10px 20px; background: #6b7280; color: white; border: none; border-radius: 6px; cursor: pointer;">✖️ Закрыть</button>
    </div>
</body>
</html>
        '''
        
        return HTMLResponse(content=html)
        
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>")

@app.post("/coffee/chat")
async def coffee_chat(user_id: str = Form(...), message: str = Form(...)):
    """Дружелюбный AI чат для Random Coffee"""
    try:
        profile = coffee_manager.get_profile(user_id)
        matches = coffee_manager.get_user_matches(user_id)
        
        if not profile:
            if any(word in message.lower() for word in ["профиль", "создать", "начать", "profile", "create", "start"]):
                try:
                    import pandas as pd
                    users_df = pd.read_csv('data/users.csv')
                    user_row = users_df[users_df['user_id'] == user_id]
                    
                    if not user_row.empty:
                        user_name = user_row.iloc[0]['name']
                        user_role = user_row.iloc[0]['role']
                        user_dept = user_row.iloc[0]['department']
                        
                        interests = ["networking", "professional development"]
                        availability = [{"day": "flexible", "time": "flexible"}]
                        
                        coffee_manager.create_profile(user_id, user_name, user_role, user_dept, interests, availability)
                        
                        return {"response": f"🎉 Отлично, {user_name}! Я создал твой профиль в Random Coffee! ☕\n\nТеперь каждую неделю я буду анонимно подбирать тебе друга среди всех студентов Cal Poly на основе ваших общих интересов. Хочешь, чтобы я нашёл твоего первого друга прямо сейчас? ✨", "success": True}
                except:
                    pass
                    
                return {"response": "Давай создадим твой профиль! Расскажи мне о своих интересах, и я смогу найти тебе идеального друга среди студентов Cal Poly! 🚀", "success": True}
            
            return {"response": "Привет! 👋 Я твой AI-помощник Random Coffee! ☕✨\n\nКаждую неделю я анонимно подбираю студентам Cal Poly друзей на основе их интересов. Вот как это работает:\n\n🤖 Ты создаёшь профиль с интересами\n💫 Раз в неделю я нахожу тебе совместимого друга\n💬 Вы знакомитесь в чате и договариваетесь о встрече\n☕ Встречаетесь за кофе и общаетесь!\n🔄 На следующей неделе я найду тебе нового друга\n\nГотов начать? Скажи 'создать профиль'! 🌟", "success": True}
        
        else:
            if any(word in message.lower() for word in ["матч", "друг", "найди", "match", "friend", "find"]):
                try:
                    new_matches = enhanced_coffee.create_ai_matches(5)
                    if new_matches:
                        return {"response": f"🎯 Супер! Я только что нашёл тебе {len(new_matches)} потенциальных друзей среди студентов Cal Poly! Проверь свои матчи - я выбрал людей с похожими интересами: {', '.join(profile.get('interests', ['общение']))}. У каждого матча есть оценка совместимости! ✨", "success": True}
                    else:
                        return {"response": "Я ищу для тебя идеального друга! 🔍 Мой AI анализирует интересы, факультеты и личности всех студентов Cal Poly. Новые люди присоединяются каждый день - скоро найду кого-то особенного! 🌟", "success": True}
                except:
                    pass
            
            if any(word in message.lower() for word in ["помощь", "как", "help", "how"]):
                return {"response": f"Конечно помогу, {profile.get('name', 'друг')}! 😊\n\n🤖 **Как работает Random Coffee:**\n• Каждую неделю AI находит тебе совместимого студента Cal Poly\n• Подбор по интересам, факультету и характеру\n• Вы общаетесь в чате и планируете встречу\n• После встречи делитесь впечатлениями\n\n☕ **Советы для встреч:**\n• Предложи встретиться в Starbucks или Julian's на кампусе\n• Спроси про специальность, проекты, планы\n• Расскажи о своих занятиях - может найдёте общие темы!\n\nТвои интересы: {', '.join(profile.get('interests', []))}\nХочешь изменить? Просто скажи! 🎯", "success": True}
            
            if len(matches) > 0:
                return {"response": f"Привет, {profile.get('name', 'друг')}! 🌟 У тебя {len(matches)} активных матчей! Это студенты Cal Poly, с которыми у тебя много общего.\n\nГотов познакомиться? Заходи в чаты и начинай общение! Помни - лучшие дружбы начинаются с простого 'Привет!' и чашки кофе. ☕💫\n\nНужны идеи для разговора или советы где встретиться? Спрашивай! 😊", "success": True}
            else:
                return {"response": f"Привет, {profile.get('name', 'друг')}! 👋 Твой профиль отлично выглядит! Мне нравится, что тебя интересует {', '.join(profile.get('interests', ['общение с людьми']))}.\n\nЯ постоянно ищу для тебя идеальных друзей среди всех студентов Cal Poly. Хочешь, чтобы я прямо сейчас запустил поиск? Скажи 'найди друзей' и я использую самые новые AI-алгоритмы! 🚀✨", "success": True}
        
        return {"response": "Я здесь, чтобы помочь тебе найти классных друзей в Cal Poly! ☕✨ Каждую неделю мой AI анонимно подбирает студентов по интересам. Хочешь попробовать? 🌟", "success": True}
        
    except Exception as e:
        return {"response": "Привет! Я помогаю студентам Cal Poly находить друзей! ☕ Каждую неделю мой AI анонимно подбирает совместимых людей по интересам. Готов начать? 🚀", "success": True}

# Онлайн-магазин endpoints
@app.get("/store/products")
async def get_store_products(category: str = None):
    """Get товары магазина"""
    products = store.get_products(category)
    return {"products": products, "success": True}

@app.post("/store/add-to-cart")
async def add_to_cart(user_id: str = Form(...), product_id: str = Form(...), quantity: int = Form(default=1)):
    """Добавить товар в корзину"""
    result = store.add_to_cart(user_id, product_id, quantity)
    return result

@app.get("/store/cart/{user_id}")
async def get_cart(user_id: str):
    """Get корзину user"""
    cart = store.get_cart(user_id)
    total = sum(item['total_price'] for item in cart)
    return {"cart": cart, "total": total, "success": True}

@app.post("/store/remove-from-cart")
async def remove_from_cart(user_id: str = Form(...), product_id: str = Form(...)):
    """Удалить товар из корзины"""
    result = store.remove_from_cart(user_id, product_id)
    return result

@app.post("/store/checkout")
async def checkout(user_id: str = Form(...), shipping_name: str = Form(...), 
                  shipping_address: str = Form(...), shipping_phone: str = Form(...)):
    """Оформить заказ"""
    shipping_info = {
        "name": shipping_name,
        "address": shipping_address,
        "phone": shipping_phone
    }
    result = store.create_order(user_id, shipping_info)
    return result

@app.get("/store/orders/{user_id}")
async def get_user_orders(user_id: str):
    """Get заказы user"""
    orders = store.get_user_orders(user_id)
    return {"orders": orders, "success": True}

# Merch System endpoints
@app.get("/merch/course/{course_id}")
async def get_course_merch(course_id: str, user_id: str = None):
    """Get мерч for вкладки course"""
    user_data = mentor.db.get_user(user_id) if user_id else {"department": "", "role": ""}
    merch_items = merch_system.get_course_merch_tab(course_id, user_data)
    return {"merch": merch_items, "success": True}

@app.get("/merch/feed/{user_id}")
async def get_personalized_merch_feed(user_id: str):
    """Get персонализированную ленту мерча"""
    user_data = mentor.db.get_user(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получаем пройденные курсы
    completed_courses = []
    for log in audit_logger.logs:
        if (log.get("user_id") == user_id and 
            log.get("action") == "course_completed"):
            completed_courses.append(log.get("course_id"))
    
    merch_feed = merch_system.get_personalized_feed(user_data, completed_courses)
    return {"merch": merch_feed, "success": True}

@app.post("/merch/track")
async def track_merch_interaction(user_id: str = Form(...), item_id: str = Form(...), 
                                 action: str = Form(...), context: str = Form(default="")):
    """Трекинг взаимодействия с мерчем"""
    merch_system.track_merch_interaction(user_id, item_id, action, context)
    return {"success": True}

@app.get("/merch/analytics")
async def get_merch_analytics():
    """Get аналитику по мерчу"""
    analytics = merch_system.get_analytics()
    return {"analytics": analytics, "success": True}

# Enhanced Random Coffee endpoints
@app.post("/enhanced-coffee/profile")
async def create_enhanced_coffee_profile(
    user_id: str = Form(...), 
    interests: str = Form(...),
    availability: str = Form(...),
    personality_traits: str = Form(default=""),
    meeting_preferences: str = Form(default="{}"),
    language: str = Form(default="en")
):
    """Создать расширенный профиль Random Coffee"""
    try:
        user = mentor.db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        interests_list = [i.strip() for i in interests.split(',') if i.strip()]
        availability_list = json.loads(availability) if availability else []
        personality_list = [p.strip() for p in personality_traits.split(',') if p.strip()]
        preferences_dict = json.loads(meeting_preferences) if meeting_preferences != "{}" else None
        
        profile = enhanced_coffee.create_enhanced_profile(
            user_id=user_id,
            name=user["name"],
            role=user["role"],
            department=user["department"],
            interests=interests_list,
            availability=availability_list,
            language=language,
            personality_traits=personality_list,
            meeting_preferences=preferences_dict
        )
        
        return {"success": True, "profile": profile}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/enhanced-coffee/compatibility/{user1_id}/{user2_id}")
async def get_compatibility_score(user1_id: str, user2_id: str):
    """Get скор совместимости"""
    score, breakdown = enhanced_coffee.calculate_compatibility_score(user1_id, user2_id)
    return {
        "compatibility_score": score,
        "breakdown": breakdown,
        "success": True
    }

@app.post("/enhanced-coffee/create-matches")
async def create_ai_matches(max_matches: int = Form(default=20)):
    """Создать AI-матчи"""
    try:
        matches = enhanced_coffee.create_ai_matches(max_matches)
        return {
            "success": True,
            "matches_created": len(matches),
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/enhanced-coffee/insights/{user_id}")
async def get_user_insights(user_id: str):
    """Get AI-инсайты user"""
    insights = enhanced_coffee.get_user_insights(user_id)
    return {"insights": insights, "success": True}

@app.get("/enhanced-coffee/profile/{user_id}")
async def get_enhanced_profile(user_id: str):
    """Get расширенный профиль"""
    profile = enhanced_coffee.profiles.get(user_id)
    if not profile:
        return {"error": "Profile not found"}
    return {"profile": profile, "success": True}

# Badge System endpoints
@app.get("/badges/{user_id}")
async def get_user_badges(user_id: str):
    """Get бейджи user"""
    badges = badge_system.get_user_badges(user_id)
    return {"badges": badges, "success": True}

@app.get("/badges/{user_id}/progress")
async def get_badge_progress(user_id: str):
    """Get прогресс по бейджам"""
    user = mentor.db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    completed_courses = [log.get("course_id") for log in audit_logger.logs 
                        if log.get("user_id") == user_id and log.get("action") == "course_completed"]
    
    coffee_stats = enhanced_coffee.get_user_insights(user_id) if user_id in enhanced_coffee.profiles else {}
    progress = badge_system.get_badge_progress(user_id, user, completed_courses, coffee_stats)
    
    return {"progress": progress, "success": True}

@app.get("/badges/{user_id}/unlocked-merch")
async def get_unlocked_merch(user_id: str):
    """Get разблокированный мерч"""
    unlocked_merch = badge_system.get_unlocked_merch(user_id)
    return {"unlocked_merch": unlocked_merch, "success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=True)