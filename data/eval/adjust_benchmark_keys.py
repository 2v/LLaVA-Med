import json

def modify_json_keys_path_vqa(file_path, output_file_path):
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        new_entry = {}
        # Modify the keys as required
        new_entry['id'] = entry['qid']
        new_entry['image'] = entry['image_name']

        new_entry['conversations'] = [
            {"from": "human", "value": entry['question']},
            {"from": "gpt", "value": entry['answer']}
        ]

        modified_data.append(new_entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
        json.dump(modified_data, file)
        file.write('\n')

        # for entry in modified_data:
        #     json.dump(entry, file)
        #     file.write('\n')

modify_json_keys_path_vqa('../VQA_RAD/VQA_RAD Dataset Public.json', '../VQA_RAD/vqa_rad_qa.jsonl')


