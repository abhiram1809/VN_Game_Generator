import requests
import time
import re


def llama_request(file_path, llama_request_link):
    files = {"file": open(file_path, "rb")}
    result_available = False
    try:
        response = requests.post(
            llama_request_link + "/generate", files=files, timeout=5
        )  # 5 seconds timeout
    except:
        print("Not generated yet")
        response = None

    # Step 2: Poll for the result
    while not result_available:
        response = requests.get(llama_request_link + "/check_result")

        if response.status_code == 200:
            result = response.text
            result_available = True
        else:
            print("Processing not complete. Waiting...")
            time.sleep(60)
    return result


def extract_prompts_and_Process_results(result):
    string_list = result.split("746859")
    Image_prompt_inputs = []
    processed_result = []
    for i in range(len(string_list)):
        lines = string_list[i].split("\n")
        lines = lines[2:]
        result_string = "\n".join(lines)
        if len(result_string) < 750:
            pass
        else:
            processed_result.append(result_string)
            lines = result_string.split("\n")
            lines = lines[:5]
            result_string = "\n".join(lines)
            Image_prompt_inputs.append(result_string)
    return Image_prompt_inputs, processed_result


def process_stars(input_string):
    # Define a regex pattern to match text between asterisks
    pattern = r"\*.*?\*"

    # Use re.sub() to replace matches with an empty string
    output_string = re.sub(pattern, "", input_string)

    return output_string


def delete_lines_with_prefixes(input_string):
    prefixes = ["Note:", "USER:", "ASSISTANT:", "User:", "Assistant:"]
    lines = input_string.split("\n")

    # Initialize an empty list to store non-matching lines
    result_lines = []

    # Iterate through the lines and keep lines that don't start with any of the prefixes
    for line in lines:
        if not any(line.strip().startswith(prefix) for prefix in prefixes):
            result_lines.append(line)

    # Join the filtered lines back into a single string
    result_string = "\n".join(result_lines)

    return result_string


def process_results_further(processed_results):
    for i in range(len(processed_results)):
        processed_results[i] = delete_lines_with_prefixes(processed_results[i])
        processed_results[i] = process_stars(processed_results[i])
    return processed_results


def send_SD_requests(prompt_list, SD_request_link):
    i = 0
    for prompt in prompt_list:
        # Send a POST request to the Colab API
        response = requests.post(SD_request_link + "/generate", json={"prompt": prompt})

        # Save the received image
        with open(f"generated_images/{i}.png", "wb") as f:
            f.write(response.content)
        i += 1
