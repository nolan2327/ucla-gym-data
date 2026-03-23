# UCLA Recreation Occupancy Dataset

Public occupancy data for UCLA Recreation facilities, updated weekly via GitHub Actions. Use this data to track gym traffic patterns, build applications, or analyze occupancy trends.

---

## Facilities

| ID | Facility | File |
|----|----------|------|
| 1  | JWC (John Wooden Center) | `JWC/jwc_data.json` |
| 2  | BFit (Bruin Fitness Center) | `BFit/bfit_data.json` |
| 3  | KREC (Kinross Recreation Center) | `KREC/krec_data.json` |

---

## Update Schedule

Data is collected every **Saturday night at 2:00 AM PST** and committed automatically. Each JSON file contains the full historical record for that facility, ordered oldest to newest.

---

## File Structure

Each facility folder contains two files:

```
JWC/
  jwc_data.json   # Full historical records
  meta.json       # Latest snapshot + metadata
```

---

## Schema

### `*_data.json`

An array of records, oldest to newest. The number of zones from each gym is different. Within jwc_data.json, the zones change on line 110185 due to construction.

```json
[
  {
    "facility":         1,
    "total_population": 24,
    "total_percentage": 8,
    "time_collected":   "2026-03-20T18:01:02Z",
    "last_updated":     "03/20/2026 05:45 PM",
    "weekday":          "Friday",
    "zones": [
      {
        "place_name":  "Cardio Zones 1&2",
        "population":  5,
        "percentage":  5
      }
    ]
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `facility` | integer | Facility ID (1 = JWC, 2 = BFit, 3 = KREC) |
| `total_population` | integer | Total number of people in the facility |
| `total_percentage` | integer | Facility occupancy as a percentage of capacity |
| `time_collected` | string (ISO 8601) | When the data was recorded |
| `last_updated` | string | Human-readable timestamp from the source system |
| `weekday` | string | Day of the week the record was collected |
| `zones` | array | Breakdown by zone (see below) |

#### Zone Object

| Field | Type | Description |
|-------|------|-------------|
| `place_name` | string | Name of the zone |
| `population` | integer | Number of people in this zone |
| `percentage` | integer | Zone occupancy as a percentage of its capacity |

---

### `meta.json`

A lightweight file containing the most recent snapshot. Useful for checking current occupancy without downloading the full dataset.

```json
{
  "last_updated":      "03/23/2026 10:27 AM",
  "record_count":      48,
  "source_collection": "clean_backup_bfit",
  "schema_version":    "1.0",
  "latest": {
    "time_collected":   "2026-03-23T10:31:02Z",
    "weekday":          "Monday",
    "total_population": 40,
    "total_percentage": 10,
    "zones": [...]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | string | Timestamp of the latest record from the source system |
| `record_count` | integer | Total number of records in the full dataset |
| `source_collection` | string | MongoDB collection this data was exported from |
| `schema_version` | string | Schema version for this file |
| `latest` | object | Most recent occupancy snapshot (same schema as a single record) |

---

 
## Usage

### JavaScript — latest snapshot (meta.json)

```js
const res = await fetch("https://raw.githubusercontent.com/nolan2327/ucla-gym-data/main/JWC/meta.json");
const data = await res.json();
console.log(data.latest.total_percentage); // e.g. 8
```

### JavaScript — full dataset

```js
const res = await fetch("https://raw.githubusercontent.com/nolan2327/ucla-gym-data/main/JWC/jwc_data.json");
const records = await res.json();
const latest = records[records.length - 1];
console.log(latest.total_percentage);
```

### Python — latest snapshot (meta.json)

```python
import requests

meta = requests.get(
    "https://raw.githubusercontent.com/nolan2327/ucla-gym-data/main/JWC/meta.json"
).json()

print(meta["latest"]["total_percentage"])
```

### Python — full dataset

```python
import requests

records = requests.get(
    "https://raw.githubusercontent.com/nolan2327/ucla-gym-data/main/JWC/jwc_data.json"
).json()

latest = records[-1]
print(latest["total_percentage"])
```

---

## Notes

- `percentage` values are rounded integers representing occupancy relative to each zone's or facility's max capacity
- Zone capacity differs per zone — a 10% reading in one zone is not directly comparable to 10% in another
- Records reflect a point-in-time snapshot, not a continuous average