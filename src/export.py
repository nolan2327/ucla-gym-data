import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient

uri = os.environ.get("MONGO_URI")
if not uri:
    raise Exception("MONGO_URI not set")

client = MongoClient(uri)
db = client["test"]

collections = [
    ("clean_backup_krec", "KREC/krec_data.json"),
    ("clean_backup_bfit", "BFit/bfit_data.json"),
    ("clean_backup_jwc",  "JWC/jwc_data.json"),
]

for coll_name, filename in collections:
    docs = []
    for doc in db[coll_name].find():
        # Remove top-level _id
        doc.pop("_id", None)

        # Convert time_collected to ISO string
        if "time_collected" in doc and isinstance(doc["time_collected"], datetime):
            doc["time_collected"] = doc["time_collected"].strftime("%Y-%m-%dT%H:%M:%S")

        # Clean zones - remove _id from each zone
        if "zones" in doc:
            for zone in doc["zones"]:
                zone.pop("_id", None)

        docs.append(doc)

    with open(filename, "w") as f:
        json.dump(docs, f, indent=2)
    
    folder = os.path.dirname(filename)

    latest = docs[-1] if docs else {}

    meta = {
        "last_updated": latest.get("last_updated"),
        "record_count": len(docs),
        "source_collection": coll_name,
        "schema_version": "1.0",
        "latest": {
            "time_collected": latest.get("time_collected"),
            "weekday": latest.get("weekday"),
            "total_population": latest.get("total_population"),
            "total_percentage": latest.get("total_percentage"),
            "zones": latest.get("zones", [])
        }
    }

    with open(f"{folder}/meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Written {len(docs)} documents to {filename}")