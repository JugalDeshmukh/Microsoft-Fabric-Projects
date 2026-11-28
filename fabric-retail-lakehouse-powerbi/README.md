# End-to-End Retail Analytics with Microsoft Fabric & Power BI (Direct Lake)

An end-to-end data engineering and business intelligence mini-project built on **Microsoft Fabric**, demonstrating unified storage with **OneLake**, dimensional modeling in a **Lakehouse**, and zero-copy reporting using a **Direct Lake Semantic Model**.

## Problem Statement
Retail sales records and regional city mappings are often stored in disconnected spreadsheets, causing duplicate data storage, manual aggregation errors, and delayed reporting. The goal is to build a single-copy analytical pipeline from raw CSV ingestion to an interactive executive dashboard without moving or duplicating data.

## Architecture & Approach
1. **Unified Storage (OneLake & Lakehouse):** Ingested raw `orders.csv` and `cities.csv` into the `Files` zone of `Sales_Lakehouse` and converted them into ACID-compliant **Delta Parquet** tables (`orders` and `cities`).
2. **Dimensional Modeling (Star Schema):** Built `Sales_Semantic_Model` in **Direct Lake** mode, linking the `cities` dimension table to the `orders` fact table via a `1:*` relationship on `city`.
3. **Business Logic (DAX):** Standardized key KPIs (`Total Revenue`, `Total Orders`, `Average Order Value`, and `Electronics Revenue`) directly inside the semantic model.
4. **Visualization (Power BI):** Created an interactive executive report querying OneLake Delta files directly with Import-level speed and zero data duplication.

## Key Results
* **Total Revenue Analyzed:** ₹1,49,300 across 12 orders and 5 Tier-1 cities.
* **Top Performing City:** Bengaluru (₹39,100) followed by Mumbai (₹38,100).
* **Category Insights:** Electronics drives ~80% of total revenue (₹1,19,100).
* **Zero Data Duplication:** Eliminated scheduled import refreshes by leveraging Direct Lake over OneLake Delta tables.

## Project Screenshots
### (Included in screenshots folder)

## What I Would Do Next
* **Automated Ingestion:** Replace manual CSV uploads with **Dataflows Gen2** or a **Fabric Pipeline** to ingest daily order drops automatically.
* **Date Dimension Table:** Add a dedicated `DimDate` table using DAX or PySpark to enable Time Intelligence metrics (MoM growth, YTD revenue).
* **Security & Governance:** Implement **Row-Level Security (RLS)** on `cities[region]` so South and West regional managers only view their respective territories.
* **Cross-Workspace Sharing:** Expose curated tables to downstream finance teams using **OneLake Shortcuts**.
