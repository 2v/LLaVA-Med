import json

# Copied from llava-med benchmark script
detail_describe_instructions = [
    "Describe the following image in detail.",
    "Provide a detailed description of the given image.",
    "Give an elaborate explanation of the image you see.",
    "Share a comprehensive rundown of the presented image.",
    "Offer a thorough analysis of the image.",
    "Explain the various aspects of the image before you.",
    "Clarify the contents of the displayed image with great detail.",
    "Characterize the image using a well-detailed description.",
    "Break down the elements of the image in a detailed manner.",
    "Walk through the important details of the image.",
    "Portray the image with a rich, descriptive narrative.",
    "Narrate the contents of the image with precision.",
    "Analyze the image in a comprehensive and detailed manner.",
    "Illustrate the image through a descriptive explanation.",
    "Examine the image closely and share its details.",
    "Write an exhaustive depiction of the given image.",
]

def modify_json_keys_image_challenge(file_path, output_file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        new_entry = {'id': entry['date']}

        new_entry['image'] = entry['image_path'].split('\\')[1]

        new_entry['conversations'] = [
            {"from": "human", "value": detail_describe_instructions[0]},
            {"from": "gpt", "value": str(entry['answer'])}
        ]

        modified_data.append(new_entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
        json.dump(modified_data, file)
        file.write('\n')


# generate the image challenge benchmark
modify_json_keys_image_challenge('../benchmark_image_challenge/benchmark_high_res.json',
                                 '../benchmark_image_challenge/benchmark_describe.json')
