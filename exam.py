import json

def check_json_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            records = json.loads(content)
            if isinstance(records, list):
                for record in records:
                    print(record.keys())
            else:
                print(records.keys())
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")

if __name__ == "__main__":
    check_json_structure("./20171204tr/20171204_001.json")