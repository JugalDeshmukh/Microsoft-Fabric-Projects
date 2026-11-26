# Microsoft Fabric: OneLake & Lakehouse End-to-End Lab

An introductory hands-on implementation exploring Microsoft Fabric's unified storage layer (**OneLake**) and **Lakehouse** architecture.

## Architecture & Workflow
1. **Workspace & Lakehouse Provisioning:** Created `Retail_Analytics_WS` and initialized `Sales_Lakehouse` with separated `Files` (unstructured landing zone) and `Tables` (managed Delta tables) directories.
2. **Raw Data Ingestion:** Uploaded `orders.csv` (retail order records in INR) into the OneLake `Files` zone.
3. **Delta Lake Conversion:** Loaded `orders.csv` into a managed ACID-compliant Delta Parquet table (`dbo.orders`).
4. **T-SQL Analytics:** Queried the auto-provisioned read-only **SQL Analytics Endpoint** to calculate city-wise order volume and its corresponding gross revenue.
5. **Zero-Copy Data Sharing:** Created a secondary `Reporting_Lakehouse` and linked `dbo.orders` via a **OneLake Shortcut**, enabling downstream Power BI and Spark consumption with zero data duplication.

## Sample T-SQL Query
```sql
SELECT
    city,
    COUNT(order_id) AS total_orders,
    SUM(amount_inr) AS revenue
FROM dbo.orders
GROUP BY city
ORDER BY revenue DESC;
