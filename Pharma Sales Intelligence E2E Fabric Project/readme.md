# End-to-End Pharmaceutical Commercial & Sales Analytics (Microsoft Fabric)

A scalable, production-grade Medallion Architecture implementation built on **Microsoft Fabric** to ingest, transform, validate, and report on enterprise-scale pharmaceutical sales, dispensing transactions, and commercial revenue.

---

## 🏗️ Architecture Overview

The platform uses a medallion data movement strategy within Microsoft Fabric:

1. **Landing Zone (OneLake / Lakehouse)**: Ingestion point for raw monthly prescription Parquet batches and dimensional CSV lookup files.
2. **Staging Layer (Warehouse - `stg`)**: Initial ingestion layer where raw data lands before undergoing stored-procedure-driven outlier detection, data hygiene checks, and audit logging.
3. **Presentation Layer (Warehouse - `dbo`)**: Star/Snowflake-aligned fact table enriched with product classifications, therapeutic areas, distributor profiles, and normalized payer channels.
4. **Semantic Model & Reporting (Direct Lake)**: Direct Lake mode Power BI semantic model featuring dynamic DAX KPIs for executive and commercial portfolio tracking.

---
