import json

if __name__ == "__main__":
    problems = None
    with open("problems.json", "r") as file:
        problems = json.load(file)
    
    # for each problem in the list then go to ./clean_transcripts and get the transcript using the Video ID
    for problem in problems:
        try:
            with open(f"./clean_transcripts/{problem['Video']}.en.txt", "r") as file:
                # read the transcript
                transcript = file.read()
                # add the transcript to the problem dictionary
                problem["Transcript"] = transcript
        except FileNotFoundError:
            problem["Transcript"] = ""
        
    # save the updated problems list
    with open("problems_transcripts.json", "w") as file:
        json.dump(problems, file, indent=4)