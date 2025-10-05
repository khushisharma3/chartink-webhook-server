# 📊 Chartink Excel Workflow with Webhook Automation

A complete automated system for managing Chartink screener results with webhook integration, Excel automation, deduplication, tracking, and TradingView export functionality.

## ✅ Features

### Excel Automation
- Automatic merging of multiple Chartink iterations
- Duplicate removal with unique stock tracking
- First appearance date and iteration tracking
- TradingView-ready export format
- Power Query automation for seamless updates

### Webhook Automation (NEW!)
- **Receives Chartink alerts automatically** via webhooks
- **Official Chartink format support** - handles stocks, trigger prices, scan names
- **No manual copy-paste** - stocks added to Excel automatically
- **Real-time processing** of alerts as they come in
- **Simple and clean** - focused on core functionality
- **Complete end-to-end automation** from Chartink to TradingView

## 🚀 Quick Start

1. **Set Up Webhook Server**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   python chartink_webhook_server.py
   ```

2. **Configure Chartink Alerts**
   - Set webhook URL: `http://your-server:5000/webhook`

3. **Set Up Excel Power Query** (One-time)
   - Follow instructions in `CHARTINK_EXCEL_GUIDE.md`


## 📊 Excel Output Structure

```
Chartink_Workflow.xlsx
├── Master_List         (Deduplicated final stock list)
├── TradingView_Export  (NSE:SYMBOL format for TradingView)
├── Iteration_1         (First Chartink export)
├── Iteration_2         (Second Chartink export)
├── Iteration_3         (Third Chartink export)
└── New_Iteration_Template (Template for new exports)
```

## 📋 Master List Columns

| Column | Description |
|--------|-------------|
| Stock_Symbol | Unique stock ticker |
| First_Appearance_Date | When stock first appeared |
| First_Iteration | Which iteration it first appeared in |
| Total_Appearances | How many times it appeared |
| Latest_Price | Most recent price |
| Latest_Volume | Most recent volume |
| Market_Cap | Market capitalization |
| Sector | Stock sector |


## 📁 Project Files (Clean Structure)

### Core Files
- `chartink_webhook_server.py` - Main webhook server for Chartink alerts
- `Chartink_Workflow.xlsx` - Excel template with automation
- `google_drive_handler.py` - Google Drive integration for cloud sync

### Documentation  
- `CHARTINK_EXCEL_GUIDE.md` - Complete Excel setup guide
- `CHARTINK_WEBHOOK_SETUP.md` - Webhook server deployment guide
- `GOOGLE_DRIVE_SETUP.md` - Google Drive integration setup
- `README.md` - This overview file

### Deployment
- `requirements.txt` - Python dependencies
- `Procfile` - For Railway/Heroku deployment
- `runtime.txt` - Python version specification
- `.gitignore` - Git ignore rules

**🎯 Automated Chartink to TradingView workflow**
