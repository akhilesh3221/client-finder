import pymysql
import pywhatkit
import time
from datetime import datetime

DB_CONFIG = {'host': 'localhost', 'user': 'root', 'password': 'YOUR_PASSWORD', 'database': 'gem_ai'}

def get_message(count, company, product):
    if count == 0:
        return f"Hello {company}, I'm Akhilesh from AVA TENDERS Raipur. We specialize in GeM Portal services for {product} manufacturers. Would you like to see a proposal?"
    elif count == 1:
        return f"Hi {company}, just following up on my previous message regarding Govt Tenders for {product}. Do you have 2 minutes for a quick call?"
    elif count == 2:
        return f"Final follow-up for {company}: We noticed several new tenders for {product} on the GeM portal today. Let us know if you want to bid!"
    return None

def run_automation():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Pick leads where count < 3
    cursor.execute("SELECT * FROM vendors WHERE message_count < 3 LIMIT 5")
    leads = cursor.fetchall()

    for lead in leads:
        msg = get_message(lead['message_count'], lead['company'], lead['product'])
        if msg:
            phone = lead['phone'] # Ensure +91 is added logic here
            print(f"Sending Message #{lead['message_count'] + 1} to {lead['company']}")
            
            # Send via WhatsApp Web
            pywhatkit.sendwhatmsg_instantly(phone, msg, 15, True, 3)
            
            # Update DB
            cursor.execute("UPDATE vendors SET message_count = message_count + 1, last_contacted = %s WHERE id = %s", 
                           (datetime.now(), lead['id']))
            conn.commit()
            time.sleep(10)

    conn.close()

if __name__ == "__main__":
    run_automation()