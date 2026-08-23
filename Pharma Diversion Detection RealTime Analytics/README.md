# Microsoft Fabric Real-Time Pharma Analytics

## Real-Time Prescription Monitoring & Drug Diversion Detection

A Microsoft Fabric data engineering and AI project implementing a
dual-path **Lambda Architecture** for real-time detection of fraudulent
prescription activity, doctor-shopping velocity, geographic
translocation, and potential drug diversion.

> **Note:** This project uses synthetic prescription-stream data for
> demonstration and learning purposes. It is not intended for real-world
> clinical or compliance decisions.

## Project Overview

The solution combines real-time streaming analytics, historical
Lakehouse processing, machine learning, automated alerting, and Power BI
reporting.

### Architecture Layers

-   **Bronze / Ingestion:** e-Prescription (eRx) ingestion through
    Fabric Eventstream.
-   **Silver Hot Path / Speed Layer:** Real-time KQL analysis in
    Eventhouse for sub-second pattern detection.
-   **Silver Cold Path / Batch Layer:** Lakehouse Delta tables processed
    with a Spark ML Random Forest model.
-   **Gold / Action Layer:** Data Activator alerts and Power BI Direct
    Lake reporting.

## Architecture

``` text
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
```

## Project Objectives

1.  Monitor prescription activity in real time.
2.  Detect rapid multi-pharmacy dispensing patterns.
3.  Identify suspicious geographic translocation.
4.  Apply machine learning to historical prescription data.
5.  Generate automated compliance alerts.
6.  Provide executive and operational dashboards.
7.  Demonstrate Lambda-style streaming and batch processing in Microsoft
    Fabric.

## Microsoft Fabric Resources

  Component         Resource
  ----------------- ---------------------------------------
  Workspace         `RealTime_Pharma_Diversion_Detection`
  Lakehouse         `Pharma_Compliance_Ops`
  Eventhouse        `RealTime_Pharma_DB`
  Eventstream       `Rx_Dispense_Stream`
  Custom Endpoint   `PharmacyGatewayConnector`
  ML                Spark Random Forest
  Alerting          Data Activator / Reflex
  Reporting         Power BI Direct Lake
  Monitoring        Real-Time KQL Dashboard

## Data Model

The primary KQL table is `RawPrescriptions`.

  Column              Type       Description
  ------------------- ---------- ---------------------------------
  `rx_id`             long       Prescription identifier
  `patient_id`        string     Patient identifier
  `hcp_dea_id`        string     Healthcare provider identifier
  `drug_name`         string     Drug name
  `units_dispensed`   real       Quantity dispensed
  `location`          string     Dispensing location
  `timestamp`         datetime   Prescription event timestamp
  `anomaly_type`      string     Existing anomaly classification
  `risk_score`        real       Risk score

## Hot Path --- Real-Time KQL Detection

### Rule 1: Doctor Shopping & Rapid Multi-Pharmacy Dispensing

The first rule uses a **10-second window** and flags patients with more
than three prescription events within that window.

``` kusto
RawPrescriptions
| where units_dispensed > 0
| summarize rx_count = count(), total_units = sum(units_dispensed)
    by patient_id, bin(timestamp, 10s)
| where rx_count > 3
| project timestamp, patient_id, rx_count, total_units,
    AlertReason = "Doctor Shopping Velocity Attack";
```

### Rule 2: Impossible Travel & Geographic Translocation

The second rule compares consecutive locations for the same patient and
flags location changes occurring within **1--120 seconds**.

``` kusto
RawPrescriptions
| order by patient_id asc, timestamp desc
| extend prev_location = prev(location),
         prev_time = prev(timestamp),
         prev_patient = prev(patient_id)
| where patient_id == prev_patient and location != prev_location
| extend time_diff_sec = datetime_diff('second', prev_time, timestamp)
| where time_diff_sec between (1 .. 120)
| project timestamp, patient_id,
    CurrentLocation = location,
    PreviousLocation = prev_location,
    time_diff_sec,
    AlertReason = "Cross-State Geographic Translocation";
```

## Cold Path --- Spark Machine Learning

Eventstream data is routed to the Lakehouse as a Delta table. A
**20-tree Random Forest classifier** is trained using:

-   `units_dispensed`
-   `risk_score`
-   encoded `location`
-   encoded `drug_name`

The label is derived from `anomaly_type`:

``` text
anomaly_type != "None"  ->  1
anomaly_type == "None"  ->  0
```

The resulting alerts are written to:

``` text
Pharma_Compliance_Ops.diversion_alerts
```

### ML Workflow

``` text
RawPrescriptions
      |
      v
String Indexing
(location + drug)
      |
      v
VectorAssembler
      |
      v
Random Forest
(20 trees)
      |
      v
Predictions
      |
      v
diversion_alerts
```

## Data Activator / Reflex

The project uses Data Activator for automated response.

**Alert:** `Doctor_Shopping_Reflex_Trigger`

**Subject:**

``` text
CRITICAL PHARMA COMPLIANCE: Rapid Opioid Dispensing Detected
```

The alert can dynamically include:

-   `patient_id`
-   `total_units`

## Power BI Direct Lake Report

The executive reporting layer uses:

``` text
Gold_Pharma_Compliance_Semantic_Model
```

with:

-   `diversion_alerts`
-   `RawPrescriptions`

### Recommended Visuals

-   **Total Incidents:** `COUNT(rx_id)`
-   **Loss Exposure:** `SUM(FlaggedUnits)`
-   **Attack Types:** Donut chart using `DiversionType` and
    `COUNT(rx_id)`
-   **Geographic Threat Exposure:** Bar chart using `location` and
    `FlaggedUnits`

## Real-Time KQL Dashboard

The operational dashboard surfaces:

1.  Live Velocity Attacks
2.  Live Geographic Translocations

The dashboard uses live refresh for dynamic operational monitoring.

## End-to-End Workflow

``` text
1. Generate synthetic prescription events
2. Send events through Eventstream
3. Process events in Eventhouse
4. Apply real-time KQL detection rules
5. Trigger Data Activator alerts
6. Route data to Lakehouse
7. Train/apply Random Forest model
8. Store diversion_alerts as Delta
9. Expose results through Power BI Direct Lake
10. Monitor live events through KQL Dashboard
```

## Suggested GitHub Structure

``` text
Microsoft-Fabric-Pharma-RealTime-Analytics/
|
├── README.md
├── KQL/
│   ├── RawPrescriptions_Table.kql
│   ├── Doctor_Shopping_Rule.kql
│   └── Geographic_Translocation_Rule.kql
├── Spark/
│   └── Pharma_Diversion_RandomForest.py
├── Data/
│   └── synthetic_prescription_sample.csv
├── Eventstream/
│   └── eventstream_configuration.md
├── Data_Activator/
│   └── reflex_alert_configuration.md
├── PowerBI/
│   └── dashboard_documentation.md
└── docs/
    └── architecture.png
```

## Setup

### 1. Create Workspace

``` text
RealTime_Pharma_Diversion_Detection
```

### 2. Create Fabric Resources

``` text
Lakehouse:   Pharma_Compliance_Ops
Eventhouse:  RealTime_Pharma_DB
Eventstream: Rx_Dispense_Stream
Endpoint:    PharmacyGatewayConnector
```

### 3. Configure Authentication

Use the Event Hub SAS authentication settings to obtain the required
Event Hub name and primary connection string.

**Never commit connection strings, SAS keys, API keys, passwords, or
other secrets to GitHub.**

### 4. Create the KQL Table

Run the `RawPrescriptions` DDL in the Eventhouse Queryset.

### 5. Configure Hot-Path Rules

Add the doctor-shopping and geographic-translocation KQL queries.

### 6. Configure Cold Path

Route Eventstream data to the Lakehouse and execute the Spark Random
Forest workflow.

### 7. Configure Alerts

Create the Data Activator / Reflex trigger for rapid dispensing
activity.

### 8. Build Power BI Report

Create the Direct Lake semantic model and add the executive KPIs and
charts.

### 9. Create Operational Dashboard

Pin the real-time KQL queries and enable live refresh.

## Security & Privacy

This repository should contain **only synthetic or anonymized
demonstration data**.

Do not commit:

-   Patient-identifiable information
-   Real healthcare records
-   DEA identifiers from real systems
-   API keys
-   SAS tokens
-   Connection strings
-   Passwords
-   Production credentials

A real healthcare deployment would require appropriate security,
privacy, governance, auditability, and regulatory controls.

## Skills Demonstrated

-   Microsoft Fabric
-   Fabric Eventstream
-   Eventhouse
-   KQL
-   Lakehouse
-   Delta Tables
-   PySpark
-   Machine Learning
-   Random Forest Classification
-   Real-Time Analytics
-   Lambda Architecture
-   Data Activator / Reflex
-   Power BI Direct Lake
-   Real-Time Dashboards
-   Data Engineering
-   AI / Compliance Analytics

## Project Outcome

This project demonstrates a complete **real-time + batch analytics
pipeline** in Microsoft Fabric, connecting streaming ingestion, KQL
anomaly detection, Spark machine learning, automated alerting, and Power
BI visualization.

It provides a practical demonstration of how modern data platforms can
combine **real-time operational monitoring with historical ML-based
analysis** in one Fabric environment.

## Author

**Jugal Deshmukh**

Data & AI Professional \| Microsoft Fabric \| Power BI \| Python \| SQL
\| Generative AI
