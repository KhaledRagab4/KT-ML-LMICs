import json

record = {
    "country": "Ethiopia",
    "study_design": "before_after"
}

print(json.dumps(record, indent=2))
