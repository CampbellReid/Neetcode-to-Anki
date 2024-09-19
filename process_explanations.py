import json
import pickle

# import the problems
with open('problems_transcripts.json', 'r') as file:
    problems = json.load(file)

# for each problem get the Video ID and make a dictionary with the Video ID as the key and the problem as the value
video_id_to_problem = {}
for problem in problems:
    video_id_to_problem[problem['Video']] = problem

errors = []

# get all the pkl files from the explanations folder
import os
for file in os.listdir('explanations'):
    if file.endswith('.pkl'):
        with open(f'explanations/{file}', 'rb') as f:
            completion = pickle.load(f)

            # get the completion from the openai completion
            try:
                explanation = json.loads(completion.choices[0].message.content)["explanation"]
            except:
                errors.append(file)
                continue

            # get the video ID from the file name
            video_id = file.split('.')[0]

            # add the explanation to the problem's dictionary
            video_id_to_problem[video_id]['Explanation'] = explanation

# save the updated problems dictionary
with open('problems_with_explanations.json', 'w') as file:
    json.dump(problems, file, indent=4)

# print the errors
print(errors)
print(len(errors))

errors_file = open('errors.txt', 'w')

for error in errors:
    problem = video_id_to_problem[error.split('.')[0]]

    # get the transcript from the problem dictionary
    transcript = problem["Transcript"]
    description = problem["Description"]
    solution = problem["PythonSolution"]
    id = problem["Video"]
    
    user_prompt = f"Problem:\n{description}\nTranscript:\n{transcript}\nSolution:\n{solution}"

    errors_file.write(user_prompt)
    errors_file.write('\n\n')

errors_file.close()