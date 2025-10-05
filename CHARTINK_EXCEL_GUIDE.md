# 📊 Chartink Excel Workflow - Complete Setup Guide

## 🎯 Overview

This guide shows you how to create an automated Excel workflow for managing Chartink screener results with:
- ✅ Automatic merging of multiple iterations
- ✅ Duplicate removal and unique stock tracking
- ✅ First appearance date and iteration tracking
- ✅ TradingView-ready export format

## 📁 Files Created

- `Chartink_Workflow.xlsx` - Main Excel template with all sheets and automation
- This guide explains how to set up and use the workflow

---

## 🚀 Step-by-Step Setup

### **Step 1: Open the Excel File**

1. Open `Chartink_Workflow.xlsx` in Microsoft Excel
2. You'll see these sheets:
   - **Master_List** - Deduplicated final list
   - **TradingView_Export** - Ready for TradingView import
   - **Iteration_1, 2, 3** - Sample data sheets
   - **New_Iteration_Template** - Template for new data

---

### **Step 2: Set Up Power Query (One-time Setup)**

#### **2.1 Create the Master Query**

1. Go to **Data** tab → **Get Data** → **From Other Sources** → **Blank Query**

2. In Power Query Editor, paste this M code:

```m
let
    // Get all iteration sheets
    Iteration1 = Excel.CurrentWorkbook(){[Name="Iteration1"]}[Content],
    Iteration2 = Excel.CurrentWorkbook(){[Name="Iteration2"]}[Content],
    Iteration3 = Excel.CurrentWorkbook(){[Name="Iteration3"]}[Content],
    
    // Combine all iterations
    CombinedData = Table.Combine({Iteration1, Iteration2, Iteration3}),
    
    // Change data types
    TypedData = Table.TransformColumnTypes(CombinedData,{
        {"Sr_No", Int64.Type},
        {"Stock_Symbol", type text},
        {"Close_Price", type number},
        {"Volume", Int64.Type},
        {"Market_Cap", type number},
        {"Sector", type text},
        {"Date_Added", type date},
        {"Iteration", Int64.Type}
    }),
    
    // Sort by Stock_Symbol and Iteration to keep first occurrence
    SortedData = Table.Sort(TypedData,{{"Stock_Symbol", Order.Ascending}, {"Iteration", Order.Ascending}}),
    
    // Remove duplicates based on Stock_Symbol (keeps first occurrence)
    DeduplicatedData = Table.Distinct(SortedData, {"Stock_Symbol"}),
    
    // Add calculated columns
    AddFirstAppearance = Table.AddColumn(DeduplicatedData, "First_Appearance_Date", each [Date_Added]),
    AddFirstIteration = Table.AddColumn(AddFirstAppearance, "First_Iteration", each [Iteration]),
    
    // Count total appearances for each stock
    GroupedCount = Table.Group(TypedData, {"Stock_Symbol"}, {{"Total_Appearances", each Table.RowCount(_), Int64.Type}}),
    
    // Merge count back to main table
    MergedWithCount = Table.NestedJoin(AddFirstIteration, {"Stock_Symbol"}, GroupedCount, {"Stock_Symbol"}, "CountData", JoinKind.LeftOuter),
    ExpandedCount = Table.ExpandTableColumn(MergedWithCount, "CountData", {"Total_Appearances"}, {"Total_Appearances"}),
    
    // Rename and reorder columns
    FinalColumns = Table.SelectColumns(ExpandedCount, {
        "Stock_Symbol", 
        "First_Appearance_Date", 
        "First_Iteration", 
        "Total_Appearances", 
        "Close_Price", 
        "Volume", 
        "Market_Cap", 
        "Sector"
    }),
    
    // Rename columns for clarity
    RenamedColumns = Table.RenameColumns(FinalColumns, {
        {"Close_Price", "Latest_Price"},
        {"Volume", "Latest_Volume"}
    }),
    
    // Add last updated column
    AddLastUpdated = Table.AddColumn(RenamedColumns, "Last_Updated", each DateTime.LocalNow())

in
    AddLastUpdated
```

3. Name this query **"MasterList"**
4. Click **Close & Load To** → **Existing worksheet** → Select **Master_List** sheet, cell **A1**

#### **2.2 Create TradingView Export Query**

1. Create another **Blank Query**
2. Paste this M code:

```m
let
    Source = Excel.CurrentWorkbook(){[Name="MasterList"]}[Content],
    AddTVFormat = Table.AddColumn(Source, "TradingView_Symbols", each "NSE:" & [Stock_Symbol]),
    SelectTVColumn = Table.SelectColumns(AddTVFormat, {"TradingView_Symbols"})
in
    SelectTVColumn
```

3. Name this query **"TradingViewExport"**
4. Click **Close & Load To** → **Existing worksheet** → Select **TradingView_Export** sheet, cell **A1**

---

### **Step 3: Set Up Automatic Refresh**

1. Go to **Data** tab → **Queries & Connections**
2. Right-click on **MasterList** query → **Properties**
3. Check ✅ **Refresh every** and set to **1 minutes** (optional)
4. Check ✅ **Refresh data when opening the file**
5. Repeat for **TradingViewExport** query

---

## 📋 How to Use the Workflow

### **Adding New Chartink Data**

#### **Method 1: Create New Iteration Sheet**

1. **Right-click** on **New_Iteration_Template** sheet → **Move or Copy**
2. Check ✅ **Create a copy** → Name it **Iteration_4** (or next number)
3. **Clear sample data** and paste your Chartink export
4. **Update the Iteration column** to the correct number (4, 5, etc.)
5. **Fill Date_Added** with today's date
6. **Refresh queries**: Data → **Refresh All**

#### **Method 2: Update Existing Sheet**

1. Go to any **Iteration_X** sheet
2. **Clear old data** and paste new Chartink export
3. **Update Date_Added** and **Iteration** columns
4. **Refresh queries**: Data → **Refresh All**

### **Updating Power Query for New Sheets**

When you add **Iteration_4, Iteration_5**, etc., update the Power Query:

1. Go to **Data** → **Queries & Connections** → **MasterList** → **Edit**
2. Update the M code to include new sheets:

```m
// Add new iteration sheets
Iteration4 = Excel.CurrentWorkbook(){[Name="Iteration4"]}[Content],
Iteration5 = Excel.CurrentWorkbook(){[Name="Iteration5"]}[Content],

// Update the combine statement
CombinedData = Table.Combine({Iteration1, Iteration2, Iteration3, Iteration4, Iteration5}),
```

---

## 📊 Understanding the Output

### **Master_List Sheet Columns**

| Column | Description |
|--------|-------------|
| **Stock_Symbol** | Unique stock ticker |
| **First_Appearance_Date** | When stock first appeared |
| **First_Iteration** | Which iteration it first appeared in |
| **Total_Appearances** | How many times it appeared across all iterations |
| **Latest_Price** | Most recent price from latest iteration |
| **Latest_Volume** | Most recent volume |
| **Market_Cap** | Market capitalization |
| **Sector** | Stock sector |
| **Last_Updated** | When data was last refreshed |

### **TradingView_Export Sheet**

- Contains **NSE:SYMBOL** format ready for TradingView import
- Copy the entire column and paste into TradingView watchlist

---

## 🔄 Advanced Automation

### **Conditional Formatting**

1. Select **Master_List** data range
2. **Home** → **Conditional Formatting** → **New Rule**
3. **Use a formula**: `=$D2>2` (highlights stocks appearing more than twice)
4. Set **green fill** for frequently appearing stocks

---

## 🎯 TradingView Import Process

### **Step 1: Copy Symbols**
1. Go to **TradingView_Export** sheet
2. **Select column A** (all NSE:SYMBOL entries)
3. **Copy** (Ctrl+C)

### **Step 2: Import to TradingView**
1. Open **TradingView** → Go to **Watchlist**
2. Click **"+"** → **Import List**
3. **Paste** the symbols
4. Click **Import**

### **Step 3: Verify Import**
- Check that all symbols are imported correctly
- Remove any invalid symbols if needed

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **Power Query Not Refreshing**
- **Solution**: Go to Data → Queries & Connections → Right-click query → Refresh

#### **New Iteration Sheet Not Included**
- **Solution**: Update Power Query M code to include new sheet names

#### **Date Format Issues**
- **Solution**: Ensure Date_Added column is formatted as Date in Excel

#### **TradingView Symbols Not Working**
- **Solution**: Verify NSE: prefix is correct for Indian stocks

### **Data Validation**

Add these checks to ensure data quality:

```excel
// Check for missing stock symbols
=COUNTBLANK(A:A)

// Check for duplicate symbols (should be 0)
=SUMPRODUCT(--(COUNTIF(A:A,A:A)>1))

// Verify date formats
=COUNTIF(G:G,"<"&TODAY()-365)
```

---

## 📈 Best Practices

### **Data Management**
1. **Consistent naming**: Use Iteration_1, Iteration_2, etc.
2. **Date format**: Use YYYY-MM-DD format
3. **Regular backups**: Save copies of your Excel file
4. **Clean data**: Remove empty rows before processing

### **Performance Optimization**
1. **Limit data**: Keep only necessary columns
2. **Regular cleanup**: Archive old iterations
3. **Efficient queries**: Optimize Power Query M code
4. **Manual refresh**: Turn off auto-refresh for large datasets

### **Workflow Tips**
1. **Test with sample data** before using real Chartink exports
2. **Document changes** when modifying Power Query
3. **Version control**: Save different versions of your Excel file
4. **Regular validation**: Check Master_List for accuracy

---

## 🎯 Summary

You now have a complete automated workflow that:

✅ **Automatically merges** multiple Chartink iterations  
✅ **Removes duplicates** while tracking first appearances  
✅ **Maintains history** of when stocks first appeared  
✅ **Exports to TradingView** in the correct format  
✅ **Scales easily** as you add more iterations  

**Next Steps:**
1. Open `Chartink_Workflow.xlsx`
2. Set up the Power Query as described above
3. Start adding your Chartink exports
4. Enjoy automated stock list management! 🚀

---

**💡 Pro Tip**: Bookmark this guide and keep the Excel file as your master template for all future Chartink screening workflows!

