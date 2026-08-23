import json
import random
import time
from datetime import datetime, timezone
from azure.eventhub import EventData, EventHubProducerClient

# Replace real keys with placeholders:
CONN_STR = "Endpoint=sb://<your-namespace>.servicebus.windows.net/;SharedAccessKeyName=<key-name>;SharedAccessKey=<your-secret-key>;"
EH_NAME = "<your-event-hub-name>"

locations = ["NYC", "PAR", "LDN", "TOK", "MUM", "High_Risk_Zone"]
drugs = ["Oxycodone 30mg", "Hydrocodone 10mg", "Fentanyl 50mcg", "Adderall 20mg", "Amoxicillin 500mg"]

producer = EventHubProducerClient.from_connection_string(conn_str=CONN_STR, eventhub_name=EH_NAME)

def generate_rx_event():
    rx_id = random.randint(100000, 999999)
    patient_id = f"PATIENT_{random.randint(1, 50)}"
    hcp_dea_id = f"DEA_{random.randint(100, 999)}"
    location = random.choice(locations)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Anomaly distribution (~5% diversion)
    roll = random.random()
    if roll < 0.02:
        anomaly_type = "Doctor_Shopping_Velocity"
        units_dispensed = random.randint(120, 240)
        risk_score = round(random.uniform(85.0, 99.0), 2)
    elif roll < 0.035:
        anomaly_type = "Cross_State_Translocation"
        units_dispensed = random.randint(30, 90)
        risk_score = round(random.uniform(75.0, 95.0), 2)
    elif roll < 0.05:
        anomaly_type = "Excessive_Dosage_Spike"
        units_dispensed = random.randint(300, 600)
        risk_score = round(random.uniform(90.0, 100.0), 2)
    else:
        anomaly_type = "None"
        units_dispensed = random.randint(10, 60)
        risk_score = round(random.uniform(1.0, 25.0), 2)

    return {
        "rx_id": rx_id,
        "patient_id": patient_id,
        "hcp_dea_id": hcp_dea_id,
        "drug_name": random.choice(drugs),
        "units_dispensed": units_dispensed,
        "location": location,
        "timestamp": timestamp,
        "anomaly_type": anomaly_type,
        "risk_score": risk_score
    }

print("Streaming real-time pharmaceutical dispensing events to Fabric...")
try:
    while True:
        event = generate_rx_event()
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(event)))
        producer.send_batch(batch)
        print(f"Sent: Rx {event['rx_id']} | {event['patient_id']} | Anomaly: {event['anomaly_type']}")
        time.sleep(0.5)
except KeyboardInterrupt:
    producer.close()