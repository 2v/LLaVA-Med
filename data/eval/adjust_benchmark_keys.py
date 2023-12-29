import json

def modify_json_keys_path_vqa(file_path, output_file_path):
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        # Modify the keys as required
        entry['question_id'] = entry.pop('qid')
        entry['image'] = entry.pop('image_name')
        entry['text'] = entry.pop('question')

        modified_data.append(entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
        for entry in modified_data:
            json.dump(entry, file)
            file.write('\n')

modify_json_keys_path_vqa('../VQA_RAD/VQA_RAD Dataset Public.json', '../VQA_RAD/vqa_rad_qa.jsonl')


