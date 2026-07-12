import feedparser
from twilio.rest import Client
import os
import sys

# Windows default encoding fix for GitHub Actions
sys.stdout.reconfigure(encoding='utf-8')

# ----------------- TWILIO WHATSAPP CONFIGURATIONS -----------------
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC8d63e90a0dd194800c0ef145f81b250c") 
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "fd74e9a12253ba66b807e36f6cd8cb55")

TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"                  
MY_WHATSAPP_NUMBER = "whatsapp:+919585181937"             

def get_live_market_headlines_thanglish():
    et_url = "https://economictimes.indiatimes.com/markets/rssfeeds/2146842.cms"
    feed = feedparser.parse(et_url)
    
    relevant_headlines = []
    for entry in feed.entries:
        title = entry.title.lower()
        if any(stock in title for stock in ["cupid", "kalyan", "jeweller"]):
            relevant_headlines.append(entry.title)
            
    if not relevant_headlines:
        return "⚠️ Live Feed Update: Ippo fresh headlines ethuvum ET feed-la match aagala machii. Keela irukura structural analysis report-ah paarunga!\n"
    
    return "📰 LIVE ET FEED NEWS MATCHES:\n" + "\n".join([f"- {h}" for h in relevant_headlines[:2]]) + "\n"

def send_thanglish_stock_report():
    live_feed_status = get_live_market_headlines_thanglish()
    
    # 100% Conversational Thanglish Message Box Layout
    thanglish_report = (
        f"🔥 *WATCHLIST STOCK REPORT (THANGLISH)* 🔥\n"
        f"-----------------------------------------\n"
        f"{live_feed_status}"
        f"-----------------------------------------\n\n"
        
        f"🎯 *1. CUPID LIMITED ANALYSIS*\n"
        f"✅ *Advantage (Gethu):* Global healthcare exports-la ivanga thaan top. Semma strong-ana B2B institutional orders back-up vechurukaanga.\n"
        f"💰 *Current Price Trend:* Net closing rate sub-₹212 range kulla trading volume maintain aahitu iruku machii.\n"
        f"🔻 *Why it Dropped (Yen Koranjidhu):* International order dispatch-la temporary delay aaghi quarter profits konjam tight aanadhala, short-term profit booking pressure thaan karanam.\n\n"
        
        f"🎯 *2. KALYAN JEWELLERS ANALYSIS*\n"
        f"✅ *Advantage (Gethu):* National level-la showroom expansion (FOCO model) over-speed-la poitu iruku. Custom consumer demand semma high-ah iruku.\n"
        f"💰 *Current Price Trend:* Semma structural recovery kaati current trades closing dynamic-ah near ₹476 range-ah touch panni trade aaguthu.\n"
        f"🔻 *Why it Dropped (Yen Koranjidhu):* Global gold bullion import duty changes matrum macro economic market shifts nala healthy range resistance correction vizhundhuchu machii.\n\n"
        f"🤝 _Automated Thanglish Stock Tracker Engine Success!_"
    )
    
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=thanglish_report,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=MY_WHATSAPP_NUMBER
        )
        print(f"✨ Gethu machii! Thanglish Stock Report WhatsApp Alert deliver aairuchu! SID: {message.sid}")
    except Exception as e:
        print(f"❌ Twilio WhatsApp Error: {e}")

if __name__ == "__main__":
    send_thanglish_stock_report()
