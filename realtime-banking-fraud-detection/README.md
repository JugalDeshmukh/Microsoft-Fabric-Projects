# Real-Time Banking Fraud Detection using Microsoft Fabric

> End-to-end real-time fraud detection platform using Microsoft Fabric,
> KQL, Eventstream, Lakehouse, Spark ML, Data Activator and Power BI.

## 🚀 Project Overview

This project implements a Lambda-style architecture consisting of:

Python → Eventstream → Hot Path + Cold Path → Fraud Alerts → Dashboards

## 🏗️ Architecture

![Architecture](architecture/architecture-diagram.png)

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Synthetic transaction generation |
| Azure Event Hubs | Streaming ingestion |
| Microsoft Fabric Eventstream | Real-time ingestion |
| Eventhouse / KQL | Hot-path analytics |
| KQL | Fraud detection |
| Fabric Lakehouse | Historical storage |
| Spark | ML processing |
| Scikit-learn | Fraud/anomaly detection |
| Data Activator | Automated alerts |
| Power BI | Executive analytics |
| Real-Time Dashboard | Operational monitoring |

## 🔍 Fraud Detection Rules

### 1. Velocity Attack

Detects unusually frequent transactions.

### 2. Impossible Travel

Detects geographically inconsistent transactions.

### 3. Spending Spree

Detects unusually large purchases.

### 4. Account Takeover

Detects suspicious micro-transactions.

## 🤖 Machine Learning

Describe your actual model here.

## 📊 Dashboards

### Power BI

![Dashboard](screenshots/06_powerbi_dashboard.png)

### Real-Time Dashboard

![Dashboard](screenshots/07_realtime_dashboard.png)

## ⚡ Real-Time Flow

...

## 📁 Repository Structure

...

## 🚀 Setup

See [Setup Guide](docs/setup-guide.md)

## 🔐 Security

No credentials are stored in this repository.

## 📌 Limitations

This project uses synthetic banking data and is intended for
educational/portfolio purposes.

## 👨‍💻 Author

Jugal Deshmukh
