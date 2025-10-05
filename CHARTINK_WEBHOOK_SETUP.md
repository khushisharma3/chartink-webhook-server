# 🚀 Chartink Webhook Automation Setup

## 🎯 Overview

This guide shows you how to set up **complete automation** from Chartink alerts directly to your Excel workflow using webhooks.

**Complete Flow:**
```
Chartink Alert → Webhook → Python Server → Excel Update → Auto-refresh
```

## ✅ What This Automates

- ✅ **Receives Chartink alerts** automatically via webhooks
- ✅ **Extracts stock symbols** from alert data
- ✅ **Adds to Excel iteration sheets** automatically
- ✅ **Maintains iteration tracking** and numbering
- ✅ **Simple and clean** - focused on core functionality
- ✅ **No manual copy-paste** required!

---

## 🔧 Setup Instructions

### **Step 1: Install Dependencies**

```bash
# Activate virtual environment
source venv/bin/activate

# Install Flask for webhook server
pip install -r requirements.txt
```

### **Step 2: Start the Webhook Server**

```bash
python chartink_webhook_server.py
```

**You'll see:**
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

### **Step 3: Configure Chartink Alerts**

1. **Go to Chartink** → Create/Edit your screener
2. **Set up Alert** → Choose "Webhook" option
3. **Webhook URL**: `http://your-server-ip:5000/webhook`
4. **Method**: POST
5. **Content-Type**: application/json

### **Step 4: Test the Setup**

1. **Trigger a Chartink alert** to see it in action
2. **Check Excel file** for new iteration sheets

---

## 📊 Chartink Webhook Data Format

The server is optimized for the official Chartink webhook format:

### **Official Chartink Format**
```json
{
    "stocks": "SEPOWER,ASTEC,EDUCOMP,KSERASERA,IOLCP,GUJAPOLLO,EMCO",
    "trigger_prices": "3.75,541.8,2.1,0.2,329.6,166.8,1.25",
    "triggered_at": "2:34 pm",
    "scan_name": "Short term breakouts",
    "scan_url": "short-term-breakouts",
    "alert_name": "Alert for Short term breakouts",
    "webhook_url": "http://your-web-hook-url.com"
}
```

### **Field Descriptions**
- **stocks**: Comma-separated string of stock symbols
- **trigger_prices**: Comma-separated string of trigger prices (matches stock order)
- **triggered_at**: Time when alert was triggered
- **scan_name**: Name of the Chartink scan
- **scan_url**: URL slug of the scan
- **alert_name**: Custom name for the alert
- **webhook_url**: Your webhook endpoint URL

### **Fallback Formats** (for compatibility)
```json
{
  "stocks": ["RELIANCE", "TCS"],
  "symbol": "RELIANCE",
  "name": "RELIANCE"
}
```

---


### **Manual Testing:**
- Send POST requests to test webhook
- Verify Excel file updates
- Check iteration numbering

---

## 🔄 Complete Automation Workflow

### **1. Chartink Side:**
```
Create Screener → Set Alert → Configure Webhook URL → Save
```

### **2. Server Side (Automatic):**
```
Receive Alert → Extract Stocks → Add to Excel → Update Iteration
```

### **3. Excel Side (Automatic):**
```
New Iteration Sheet → Power Query Refresh → Master List Update → TradingView Export Ready
```

### **4. Your Side:**
```
Check Excel File → Copy TradingView Export → Import to TradingView
```

---


**🎯 Automated Chartink to TradingView workflow setup complete!**
