import csv
import json

data = []


with open('./drug_details.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

results = []
for row in data:
    final_data = {}
    names = row[7].strip().split('\n')
    other_info = row[8].split('\n')
    try:
        final_data['name'] = names[0].strip()
        final_data['common_brands'] = [brand.strip()
                                       for brand in names[1].split(':')[1].strip().split(',')]
        final_data['generic_names'] = [name.strip()
                                       for name in names[2].split(':')[1].strip().split(',')]
        final_data['uses'] = other_info[1].split('Uses')[1].strip()
        results.append(final_data)
    except Exception:
        continue

with open('./webmd_data.json', 'w') as f:
    json.dump(results, f, indent=4)
