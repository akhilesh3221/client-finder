# 🚀 AVA TENDERS | AI-Powered Lead Finder & GeM Scraper

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-Automation-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue.svg)

**AVA TENDERS** is a high-performance Business Intelligence (BI) platform designed for the Indian government procurement ecosystem. It automates the discovery of local business leads and monitors live government tenders across multiple portals (GeM, Railways, and more).

---

## 🌟 Key Features

### 1. 🔍 Automated GeM Scraper
A sophisticated Selenium engine that navigates the **Government e-Marketplace (GeM)**.
- **Deep Pagination:** Clicks through 50+ pages automatically to pull every live bid.
- **Auto-Trigger:** Scraper launches in the background as soon as you visit the dashboard.
- **Smart Throttling:** Mimics human behavior to bypass bot detection.

### 2. 📍 Google Maps Lead Generator
Find potential B2B clients in specific regions like **Raipur, Chhattisgarh**.
- Search by industry keywords (e.g., "TMT Bar Manufacturers", "Solar Installers").
- Scrapes contact details, addresses, and ratings directly into your CRM.

### 3. 📊 Premium CRM Dashboard
A responsive interface for managing your business growth.
- **Live Feed:** Real-time table of new tenders.
- **Lead Status:** Track leads from "Pending" to "Closed."
- **One-Click Actions:** Open Google Maps or start a WhatsApp chat instantly from the table.

---

## 🏗️ Technical Architecture



The system uses an **Asynchronous Background Task** architecture. When a user loads the dashboard, FastAPI returns the existing database results instantly, while a separate thread launches the Selenium WebDriver to fetch new updates.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/akhilesh3221/client-finder.git](https://github.com/akhilesh3221/client-finder.git)
cd client-finder