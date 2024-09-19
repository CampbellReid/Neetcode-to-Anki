import os
from openai import OpenAI
import json
import pickle

if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    organisation_id = os.getenv('OPENAI_ORG_ID')
    if organisation_id is None:
        raise ValueError("OPENAI_ORG_ID environment variable is not set")

    project_id = os.getenv('OPENAI_PROJECT_ID')
    if project_id is None:
        raise ValueError("OPENAI_PROJECT_ID environment variable is not set")

    client = OpenAI(
        organization=organisation_id,
        project=project_id,
        api_key=api_key
    )

    # load the system prompt
    with open("system_prompt.txt", "r") as file:
        system_prompt = file.read()
        print(system_prompt)

    # load the problems from the file
    with open("problems_transcripts.json", "r") as file:
        problems = json.load(file)
    
    # make the directory if it doesn't exist
    if not os.path.exists("./explanations"):
        os.makedirs("./explanations")
    
    for problem in problems:
        # get the transcript from the problem dictionary
        transcript = problem["Transcript"]
        description = problem["Description"]
        solution = problem["PythonSolution"]
        id = problem["Video"]
        
        # Check if the explanation already exists
        completion_file = f"./explanations/{id}.pkl"
        if os.path.exists(completion_file):
            print(f"Skipping {id} as it already exists")
            continue
        
        user_prompt = f"Problem:\n{description}\nTranscript:\n{transcript}\nSolution:\n{solution}"
        
        print(f"Getting explanation for {id}")
        
        completion = client.chat.completions.create(
            model="gpt-4o",
            max_completion_tokens=700,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format = {
                "type": "json_object"
            }
        )
        
        print(f"Saving explanation for {id} to {completion_file}")
        
        # save the whole completion to a file
        completion_file = f"./explanations/{id}.pkl"
        with open(completion_file, "wb") as file:
            pickle.dump(completion, file)
        