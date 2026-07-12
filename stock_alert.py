import feedparser
from twilio.rest import Client
import yfinance as yf
import google.generativeai as genai
import os
import sys

# Windows default encoding fix for GitHub Actions
sys.stdout.reconfigure(encoding='utf-8')

# ----------------- CONFIGURATIONS -----------------
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC8d63e90a0dd194800c0ef145f81b250c") 
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "fd74e9a12253ba66b807e36f6cd8cb55")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"                  
MY_WHATSAPP_NUMBER = "whatsapp:+919585181937"             

# Configure Gemini AI
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# === INGA PUTHU STOCKS ADD PANNALAM ===
MY_STOCKS = {
    "CUPID.NS": "Cupid Limited",
    "KALYANKJIL.NS": "Kalyan Jewellers",
    "HDFCBANK.NS": "HDFC Bank"
}
# =======================================

def generate_ai_analysis(company_name, price, news):
    if not model:
        return "⚠️ Gemini API Key illatha kaaranathinala AI analysis generate panna mudiyala."
    
    prompt = f"""
    You are an expert stock market analyst who speaks in 'Thanglish' (Tamil + English).
    Analyze the following stock data for {company_name}:
    Current Price: {price}
    Latest News Headlines: {news}
    
    Provide a very short and punchy analysis in Thanglish covering exactly these 3 points using bullet points:
    ✅ *Advantage (Gethu):* [1 sentence Thanglish]
    ⚠️ *Disadvantage (Risk):* [1 sentence Thanglish]
    📉/📈 *Yen Eruthu/Eranguthu (Trend):* [1 sentence Thanglish reason based on news/price]
    
    Do not add any other text or headers. Just these 3 points.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ AI Error: {e}"

def get_stock_data(ticker, company_name):
    # 1. Fetch Current Price
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            price_val = round(data['Close'].iloc[0], 2)
            price_text = f"₹{price_val}"
            display_price = f"💰 *Live Price:* {price_text}"
        else:
            price_text = "Data illai"
            display_price = "💰 *Live Price:* Market update aagavillai."
    except Exception:
        price_text = "Data illai"
        display_price = "💰 *Live Price:* Data kedaikkavillai."

    # 2. Fetch Live News
    query = company_name.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    news_text = ""
    for entry in feed.entries[:2]:
        news_text += f"📰 {entry.title}\n"
        
    if not news_text:
        news_text = "📰 Inaiku entha puthu news-um illai."
        
    # 3. Get AI Analysis
    ai_analysis = generate_ai_analysis(company_name, price_text, news_text)
    
    # If AI fails, make the error shorter and cleaner
    if "❌ AI Error" in ai_analysis:
        ai_analysis = "⚠️ AI Server Error: Ippo AI thalapathy busy-ah irukaaru, later try pannunga."
    
    return f"{display_price}\n\n*Puthu News (Live):*\n{news_text}\n*AI Analysis (Thanglish):*\n{ai_analysis}"

def send_thanglish_stock_report():
    print("Fetching live data and generating AI analysis...")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    # 1. Send Header Message
    header = "🤖 *LIVE AI STOCK REPORT (THANGLISH)* 🔥\n-----------------------------------------"
    try:
        client.messages.create(body=header, from_=TWILIO_WHATSAPP_NUMBER, to=MY_WHATSAPP_NUMBER)
    except Exception as e:
        print(f"❌ Twilio Header Error: {e}")
    
    # 2. Send Each Stock as a Separate Message
    counter = 1
    for ticker, company_name in MY_STOCKS.items():
        stock_data = get_stock_data(ticker, company_name)
        msg_body = f"🎯 *{counter}. {company_name.upper()}*\n{stock_data}"
        try:
            message = client.messages.create(
                body=msg_body,
                from_=TWILIO_WHATSAPP_NUMBER,
                to=MY_WHATSAPP_NUMBER
            )
            print(f"✨ {company_name} message delivered! SID: {message.sid}")
        except Exception as e:
            print(f"❌ Twilio Error for {company_name}: {e}")
        counter += 1
        
    # 3. Send Footer
    footer = "-----------------------------------------\n🤝 _Automated Gemini AI Tracker_"
    try:
        client.messages.create(body=footer, from_=TWILIO_WHATSAPP_NUMBER, to=MY_WHATSAPP_NUMBER)
    except Exception as e:
        print(f"❌ Twilio Footer Error: {e}")

if __name__ == "__main__":
    send_thanglish_stock_report()
