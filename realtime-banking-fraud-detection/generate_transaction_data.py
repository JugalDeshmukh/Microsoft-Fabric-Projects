import time
import json
import random
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData

# ==============================================================================
# STUDENT TASK: Fill in your SAS Key Authentication credentials from Step 2
# ==============================================================================
import os

CONN_STR = os.getenv("EVENT_HUB_CONNECTION_STRING")
EH_NAME = os.getenv("EVENT_HUB_NAME")

# Track a small pool of customers to force stateful pattern overlap
CUSTOMER_POOL = [f"USER_{i}" for i in range(1, 51)]

def create_transaction():
    """Generates synthetic banking events mimicking clean and advanced fraud profiles."""
    dice_roll = random.random()
    current_time_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    cust_id = random.choice(CUSTOMER_POOL)
    tx_id = random.randint(100000, 999999)

    if dice_roll < 0.02:
        # Velocity / Swiping Attack: Massive amounts flagged for high velocity rules
        return {
            "tx_id": tx_id, 
            "cust_id": cust_id,
            "amount": round(random.uniform(3000.00, 8000.00), 2),
            "location": "High_Risk_Zone", 
            "timestamp": current_time_iso,
            "fraud_type": "Velocity_Attack"
        }
    elif 0.02 <= dice_roll < 0.04:
        # Impossible Travel: Simulates rapid geographic translocation
        return {
            "tx_id": tx_id, 
            "cust_id": cust_id,
            "amount": round(random.uniform(50.00, 500.00), 2),
            "location": random.choice(["TOKYO", "SYDNEY", "MUMBAI"]), 
            "timestamp": current_time_iso,
            "fraud_type": "Impossible_Travel"
        }
    elif 0.04 <= dice_roll < 0.06:
        # Spending Spree: Extreme financial anomaly to be isolated by Spark ML
        return {
            "tx_id": tx_id, 
            "cust_id": cust_id,
            "amount": round(random.uniform(12000.00, 25000.00), 2),
            "location": random.choice(["NEW YORK", "LONDON", "PARIS"]),
            "timestamp": current_time_iso,
            "fraud_type": "Spending_Spree"
        }
    elif 0.06 <= dice_roll < 0.08:
        # Account Takeover / Smurfing: Repetitive tiny micro-charges to evade standard rule limits
        return {
            "tx_id": tx_id, 
            "cust_id": cust_id,
            "amount": round(random.uniform(0.10, 4.99), 2),
            "location": "Online_Gateway",
            "timestamp": current_time_iso,
            "fraud_type": "Account_Takeover"
        }
    else:
        # Baseline: 92% Legitimate Consumer Transactions
        return {
            "tx_id": tx_id, 
            "cust_id": cust_id,
            "amount": round(random.uniform(10.00, 600.00), 2),
            "location": random.choice(["NEW YORK", "LONDON", "PARIS"]),
            "timestamp": current_time_iso,
            "fraud_type": "None"
        }

# Initialize connection client to Fabric Eventstream
producer = EventHubProducerClient.from_connection_string(CONN_STR, eventhub_name=EH_NAME)

print("🚀 [START] Connecting and preparing telemetry feed...")

# --- Executing Context Manager Loop ---
with producer:
    print("Streaming multi-vector transactional telemetry into Fabric...")
    while True:
        try:
            batch = producer.create_batch()
            payload = create_transaction()
            
            # Serialize payload to JSON text format
            json_data = json.dumps(payload)
            batch.add(EventData(json_data))
            
            # Push batch to the active Eventstream topic
            producer.send_batch(batch)
            
            print(f"Sent: {payload['tx_id']} | User: {payload['cust_id']} | Amt: ${payload['amount']} | Loc: {payload['location']} | Profile: {payload['fraud_type']}")
            time.sleep(0.5)  # Accelerated pacing to guarantee rule trigger overlaps
            
        except Exception as e:
            print(f"❌ Connection Interrupted: {str(e)}")
            time.sleep(5)