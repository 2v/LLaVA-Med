import json

from data.benchmark_image_challenge.prompts import prompt_multimodal_fixed, prompt_image_only_fixed, \
    prompt_text_only_fixed


def modify_json_keys_path_vqa(file_path, output_file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        new_entry = {}
        # Modify the keys as required
        new_entry['id'] = entry['qid']
        new_entry['image'] = entry['image_name']

        question = entry['question']

        answer_type = entry['answer_type']
        if answer_type == 'CLOSED':
            question = question + ' (Answer with either "Yes" or "No").'

        new_entry['answer_type'] = answer_type

        new_entry['conversations'] = [
            {"from": "human", "value": question},
            {"from": "gpt", "value": str(entry['answer'])}
        ]

        modified_data.append(new_entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
        json.dump(modified_data, file)
        file.write('\n')


def modify_json_keys_image_challenge(file_path, output_file_path, prompt_type):
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        new_entry = {}
        new_entry['id'] = entry['date']
        new_entry['image'] = entry['image_path'].split('\\')[1]

        question = entry['question']
        options = list(map(lambda x: x['label'], entry['options']))

        if prompt_type == 'mm_fixed':
            formatted_question = prompt_multimodal_fixed.format(question=question, options=options)
        elif prompt_type == 'image_only_fixed':
            formatted_question = prompt_image_only_fixed.format(options=options)
        elif prompt_type == 'text_only_fixed':
            formatted_question = prompt_text_only_fixed.format(question=question, options=options)
            new_entry['image'] = []
        else:
            print('Please select one of: \'mm_fixed\', \'image_only_fixed\', or \'text_only_fixed\'')
            return

        new_entry['conversations'] = [
            {"from": "human", "value": formatted_question},
            {"from": "gpt", "value": str(entry['answer'])}
        ]

        modified_data.append(new_entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
        json.dump(modified_data, file)
        file.write('\n')


# generate the updated VQA RAD benchmark
modify_json_keys_path_vqa('../VQA_RAD/VQA_RAD Dataset Public.json', '../VQA_RAD/vqa_rad_qa.json')

# generate the image challenge benchmark
modify_json_keys_image_challenge('../benchmark_image_challenge/benchmark_high_res.json',
                                 '../benchmark_image_challenge/benchmark_high_res_formatted.json',
                                 'mm_fixed')


