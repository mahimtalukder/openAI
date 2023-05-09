import json

input_file = 'dataset.json'

# Read and parse multiple JSON objects
data_list = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        data_list.append(json.loads(line.strip()))

# Combine the data from all JSON objects
all_data = {'words': []}
for data in data_list:
    all_data['words'].extend(data['words'])

# Transform the dataset
transformed_data = []

for word_pair in all_data['words']:
    transformed_data.append({
        'prompt': f'Translate from English to Bengali: {word_pair["en"]}',
        'completion': word_pair['bn']
    })

# Save the transformed dataset to a new file
with open('your_transformed_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(transformed_data, f, ensure_ascii=False, indent=4)
