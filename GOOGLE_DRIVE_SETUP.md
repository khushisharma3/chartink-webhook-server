# 🔗 Google Drive Integration Setup Guide

## 🎯 Overview

This guide shows you how to integrate your Chartink webhook server with Google Drive so that:
- ✅ **Excel file is stored in Google Drive** (accessible from anywhere)
- ✅ **Webhook automatically downloads** the file before updating
- ✅ **Webhook automatically uploads** the updated file back to Google Drive
- ✅ **Works perfectly with cloud hosting** (Railway, Render, etc.)
- ✅ **No file persistence issues** on cloud servers

---

## 📋 Step 1: Create Google Cloud Project

### 1.1 Create Project
1. Go to **console.cloud.google.com**
2. Click **"Select a project"** → **"New Project"**
3. **Project name:** `chartink-webhook`
4. Click **"Create"**

### 1.2 Enable Google Drive API
1. In your project dashboard, click **"APIs & Services"** → **"Library"**
2. Search for **"Google Drive API"**
3. Click on it → Click **"Enable"**

---

## 📋 Step 2: Create Service Account

### 2.1 Create Service Account
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"Service Account"**
3. **Service account name:** `chartink-webhook-service`
4. **Service account ID:** `chartink-webhook-service` (auto-filled)
5. Click **"Create and Continue"**

### 2.2 Grant Permissions
1. **Role:** Select **"Editor"** or **"Storage Admin"**
2. Click **"Continue"** → **"Done"**

### 2.3 Generate Key File
1. Click on your newly created service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"**
4. Choose **"JSON"** format
5. Click **"Create"**
6. **Download the JSON file** and keep it safe!

---

## 📋 Step 3: Prepare Your Excel File

### 3.1 Upload to Google Drive
1. Go to **drive.google.com**
2. Click **"New"** → **"File upload"**
3. Upload your `Chartink_Workflow.xlsx` file
4. **Note the file name** (must match exactly in your code)

### 3.2 Share with Service Account
1. **Right-click** on your uploaded Excel file
2. Click **"Share"**
3. **Add the service account email** (from the JSON file, looks like: `chartink-webhook-service@chartink-webhook.iam.gserviceaccount.com`)
4. Give it **"Editor"** permissions
5. Click **"Send"**

---

## 📋 Step 4: Configure Your Deployment

### 4.1 For Railway Deployment

#### Environment Variables:
1. In Railway dashboard, go to your project
2. Click **"Variables"** tab
3. Add these variables:

```
USE_GOOGLE_DRIVE=true
GOOGLE_CREDENTIALS=<paste entire JSON content here>
```

#### How to get JSON content:
1. Open the downloaded JSON file in a text editor
2. **Copy the entire content** (including { and })
3. **Paste it as the value** for GOOGLE_CREDENTIALS

### 4.2 For Render Deployment

#### Environment Variables:
1. In Render dashboard, go to your service
2. Click **"Environment"** tab
3. Add the same variables as above

### 4.3 For Local Testing

#### Create .env file:
```bash
# Create .env file in your project folder
echo "USE_GOOGLE_DRIVE=true" > .env
echo "GOOGLE_CREDENTIALS='$(cat path/to/your/credentials.json)'" >> .env
```

---

## 📋 Step 5: Test the Integration

### 5.1 Local Test
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export USE_GOOGLE_DRIVE=true
export GOOGLE_CREDENTIALS='<your-json-content>'

# Run the server
python chartink_webhook_server.py
```

### 5.2 Test Webhook
```bash
# Send test request
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "stocks": "TESTSTOCK1,TESTSTOCK2",
    "trigger_prices": "100.50,200.75",
    "triggered_at": "3:30 pm",
    "scan_name": "Test Scan",
    "alert_name": "Test Alert",
    "scan_url": "test-scan"
  }'
```

### 5.3 Verify Results
1. **Check your Google Drive** - the Excel file should be updated
2. **Download and open** the file to verify new data was added
3. **Check server logs** for any error messages

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. "File not found in Google Drive"
- **Solution:** Make sure the Excel file is uploaded to Google Drive
- **Check:** File name matches exactly (case-sensitive)

#### 2. "Permission denied"
- **Solution:** Share the file with your service account email
- **Check:** Service account has "Editor" permissions

#### 3. "Invalid credentials"
- **Solution:** Verify the JSON content is correct
- **Check:** No extra quotes or formatting issues in environment variable

#### 4. "API not enabled"
- **Solution:** Enable Google Drive API in Google Cloud Console
- **Check:** Project is selected correctly

### Debug Mode:
Add this to your webhook server for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✅ Benefits of Google Drive Integration

- ✅ **Cloud Storage:** Excel file accessible from anywhere
- ✅ **Automatic Sync:** Updates happen automatically
- ✅ **No File Loss:** Cloud hosting file persistence solved
- ✅ **Backup:** Google Drive provides automatic backups
- ✅ **Collaboration:** Multiple people can access the file
- ✅ **Version History:** Google Drive tracks file changes

---

## 🚀 Next Steps

1. **Complete this setup**
2. **Deploy to Railway/Render** with environment variables
3. **Set up Chartink alerts** with your webhook URL
4. **Test with real alerts**
5. **Monitor your Google Drive** for automatic updates

Your webhook server will now automatically manage the Excel file in Google Drive! 🎉
