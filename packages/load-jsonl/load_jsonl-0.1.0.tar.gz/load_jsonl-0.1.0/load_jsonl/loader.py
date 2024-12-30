import json

def load_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        cnt = 0
        for line in f.readlines():
            try:
                data.append(json.loads(line.strip()))
            except:
                print(f"Encounter Error in Line {cnt}\n")
            cnt += 1
    return data
