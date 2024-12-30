#!/usr/bin/env python3

import argparse
import subprocess
import yaml

# Load the values from a YAML file (handles multiple documents)
def load_values(values_file):
    with open(values_file, 'r') as f:
        return list(yaml.safe_load_all(f)) 

# Substitute values into the template
def substitute_values(scroll_book_path, manifest_file_values):
    with open(scroll_book_path, 'r') as f:
        scroll_book_content = yaml.safe_load(f)

    for doc in manifest_file_values:
        if isinstance(doc, dict):
            
            if 'jutsu' in scroll_book_content:
                jutsu = scroll_book_content['jutsu']

                doc = replace_placeholder(doc, "<:CLUSTER_NAME>", str(jutsu['clusterName']))
                if 'database' in jutsu:
                    doc = replace_placeholder(doc, "<:DB_USERNAME>", str(jutsu['database']['username']))
                    doc = replace_placeholder(doc, "<:DB_PASSWORD>", str(jutsu['database']['password']))
                if 'azureOpenAI' in jutsu:
                    doc = replace_placeholder(doc, "<:OPEN_AI_ENDPOINT>", str(jutsu['azureOpenAI']['deploymentEndpoint']))
                    doc = replace_placeholder(doc, "<:OPEN_AI_API_KEY>", str(jutsu['azureOpenAI']['apiKey']))
                    doc = replace_placeholder(doc, "<:OPEN_AI_VERSION>", str(jutsu['azureOpenAI']['apiVersion']))
                    doc = replace_placeholder(doc, "<:OPEN_AI_DEPLOYMENT_NAME>", str(jutsu['azureOpenAI']['deploymentName']))
                if 'alertManager' in jutsu:
                    doc = replace_placeholder(doc, "<:TEAMS_WEBHOOK_URL>", str(jutsu['alertManager']['teamsWebhookURL']))
                    doc = replace_placeholder(doc, "<:KIMS_UI_ENDPOINT>", str(jutsu['alertManager']['kimsUIURL']))
    return manifest_file_values


def replace_placeholder(doc, placeholder, value):
    if isinstance(doc, str):
        return doc.replace(placeholder, value)
    elif isinstance(doc, list):
        return [replace_placeholder(item, placeholder, value) for item in doc]
    elif isinstance(doc, dict):
        for k, v in doc.items():
            doc[k] = replace_placeholder(v, placeholder, value)
    return doc

# Save the substituted content into a new file
def save_modified_yaml(output_file, content):
    with open(output_file, 'w') as f:
        yaml.dump_all(content, f)

def execute_rendered_manifest(rendered_manifest_file):
    k8s_log_command = f"kubectl apply -f {rendered_manifest_file}"
    log_output = subprocess.check_output(k8s_log_command, shell=True)
    print(f'\u001b[36m {log_output}')



def main():
    try:
        print(f'\u001b[35m ################################################################################################################################')
        print(f'\u001b[35m PERFORMING JUTSU FROM SCROLL...')
        print(f'\u001b[35m ################################################################################################################################')
        print('\n')
        print(f'\u001b[36m ################################################################################################################################')
        print('\n')
        print(f'\u001b[36m READING SCROLL...')
        parser = argparse.ArgumentParser()
        parser.add_argument('--scroll', required=True, help="Path to the YAML template to substitute values")
        args = parser.parse_args()
        scroll_book = args.scroll 
        values_file = '/usr/local/Lib/kaizen-deploy/templates/manifest.yaml'  
        rendered_manifest_file = 'render.yaml' 
        print(f'\u001b[36m LOADING TEMPLATES...')
        manifest_file_values = load_values(values_file)
        print(f'\u001b[36m RENDERING MANIFEST FILE...')
        modified_content = substitute_values(scroll_book, manifest_file_values)
        print(f'\u001b[36m MANIFEST RENDERING COMPLETED...')
        print(f'\u001b[36m SAVING RENDERED FILE...')
        save_modified_yaml(rendered_manifest_file, modified_content)
        print(f'\u001b[36m SAVED SUCCESSFULLY...')
        print('\n')
        print('\n')
        print(f'\u001b[36m EXECUTING RENDERED MANIFEST FILE...')
        execute_rendered_manifest(rendered_manifest_file)
        print('\n')
        print(f'\u001b[36m RENDER MANIFEST FILE EXECUTED SUCCESSFULLY...')
        print('\n')
        

        print('\n')
        print(f'\u001b[36m ################################################################################################################################')
    except Exception as e:
        exception_message = f"Exception caught while processing failed pod data: {e}"
        print(f'\u001b[35m ################################################################################################################################')
        print(f'\u001b[35m JUTSU FAILED: {exception_message}')
        print(f'\u001b[35m ################################################################################################################################')
        print('\n')
        raise ValueError(exception_message)
    else:
        print(f'\u001b[35m ################################################################################################################################')
        print(f'\u001b[35m JUTSU PERFORMED SUCCESSFULLY...')
        print(f'\u001b[35m ################################################################################################################################')
        print('\n')


if __name__ == "__main__":
    main()
