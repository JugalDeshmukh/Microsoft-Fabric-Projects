# Microsoft Fabric Real-Time Pharma Analytics

## Real-Time Prescription Monitoring & Drug Diversion Detection

A Microsoft Fabric data engineering and AI project implementing a dual-path **Lambda Architecture** for real-time detection of fraudulent prescription activity, doctor-shopping velocity, geographic translocation, and potential drug diversion.

> **Note:** This project uses synthetic prescription-stream data for demonstration and learning purposes. It is not intended for real-world clinical or compliance decisions.

---

## 📌 Project Overview

The solution combines real-time streaming analytics, historical Lakehouse processing, machine learning, automated alerting, and Power BI reporting.

### Architecture Layers

- **Bronze / Ingestion:** e-Prescription (eRx) ingestion through Microsoft Fabric Eventstream.
- **Silver Hot Path / Speed Layer:** Real-time KQL analysis in Eventhouse for sub-second pattern detection.
- **Silver Cold Path / Batch Layer:** Lakehouse Delta tables processed with a Spark ML Random Forest model.
- **Gold / Action Layer:** Data Activator alerts and Power BI Direct Lake reporting.

This architecture allows the same incoming data to support both **immediate operational detection** and **historical machine-learning analysis**.

---

## 🏗️ Architecture

```text
Synthetic Prescription Stream
          |
          v
   Fabric Eventstream
          |
     +----+----+
     |         |
     v         v
 Eventhouse  Lakehouse
   KQL       Cold Path
     |         |
     |         v
     |      Spark ML
     |      Random Forest
     |         |
     +----+----+
          |
     +----+----------------+
     |                     |
     v                     v
Data Activator       Power BI Direct Lake
  / Reflex            + KQL Dashboard
