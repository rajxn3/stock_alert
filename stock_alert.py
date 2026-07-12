import feedparser
from twilio.rest import Client
import yfinance as yf
import os
import sys

# Windows default encoding fix for GitHub Actions
sys.stdout.reconfigure(encoding='utf-8')

# ----------------- TWILIO WHATSAPP CONFIGURATIONS -----------------
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC8d63e90a0dd194800c0ef145f81b250c") 
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "fd74e9a12253ba66b807e36f6cd8cb55")

TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"                  
MY_WHATSAPP_NUMBER = "whatsapp:+919585181937"             

# === INGA PUTHU STOCKS ADD PANNALAM ===
# Format: "Ticker Symbol": "Company Name"
MY_STOCKS = {
    "CUPID.NS": "Cupid Limited",
    "KALYANKJIL.NS": "Kalyan Jewellers",
    "HDFCBANK.NS": "HDFC Bank"
    
    # Kela irukura maathiri neenga evlo stocks venum naalum add pannalam!
    # "RELIANCE.NS": "Reliance Industries",
    # "TCS.NS": "Tata Consultancy Services"
}
# =======================================

def get_stock_data(ticker, company_name):
    # 1. Fetch Current Price using yfinance
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            price = round(data['Close'].iloc[0], 2)
            price_text = f"💰 *Live Price:* ₹{price}"
        else:
            price_text = "💰 *Live Price:* Market update aagavillai."
    except Exception:
        price_text = "💰 *Live Price:* Data kedaikkavillai."

    # 2. Fetch Live News using Google News RSS
    query = company_name.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={query}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    
    news_text = ""
    for entry in feed.entries[:2]: # Top 2 recent news
        title = entry.title
        news_text += f"📰 {title}\n"
        
    if not news_text:
        news_text = "📰 Inaiku entha puthu news-um illai machii.\n"
        
    return f"{price_text}\n\n*Puthu News (Live):*\n{news_text}"

def send_thanglish_stock_report():
    print("Fetching live data...")
    
    report_lines = [
        "*LIVE STOCK REPORT (THANGLISH)* ",
        "-----------------------------------------\n"
    ]
    
    counter = 1
    for ticker, company_name in MY_STOCKS.items():
        stock_data = get_stock_data(ticker, company_name)
        report_lines.append(f"🎯 *{counter}. {company_name.upper()}*")
        report_lines.append(f"{stock_data}\n")
        counter += 1
        
    report_lines.append("-----------------------------------------")
    report_lines.append("🤝 _Automated Thanglish Stock Tracker Engine_")
    
    thanglish_report = "\n".join(report_lines)
    
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=thanglish_report,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=MY_WHATSAPP_NUMBER
        )
        print(f"✨ Gethu machii! Live Stock Report WhatsApp Alert deliver aairuchu! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Twilio WhatsApp Error: {e}")

if __name__ == "__main__":
    send_thanglish_stock_report()
