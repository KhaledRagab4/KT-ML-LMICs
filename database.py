import json

def save_record(record, filepath):
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

def load_records(filepath):
    records = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            records.append(json.loads(line))
    return records

if __name__ == "__main__":
    test_record = {"pmid": "123", "country": "Ethiopia"}
    save_record(test_record, "data/evidence.jsonl")
    loaded = load_records("data/evidence.jsonl")
    print(loaded)
