import genanki
import random

# found using python -c "import random; print(random.randrange(1 << 30, 1 << 31))"
unique_model_id = 1160519191
unique_deck_id = 2047665655

leetcode_model = genanki.Model(
    unique_model_id,
    "Leetcode",
    fields=[
        {"name": "Id"},
        {"name": "Description"},
        {"name": "Solution"},
        {"name": "Explanation"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Description}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Solution}}<br>{{Explanation}}',
        },
    ],
)

deck = genanki.Deck(unique_deck_id, "Leetcode Problems")

# import the problems
import json

with open("problems_with_explanations.json", "r") as file:
    problems = json.load(file)


class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


import markdown
import html


for problem in problems:
    note = MyNote(
        model=leetcode_model,
        fields=[
            problem["Video"],
            markdown.markdown(problem["Description"]),
            problem["PythonSolution"],
            markdown.markdown(problem["Explanation"]),
        ],
    )

    deck.add_note(note)

genanki.Package(deck).write_to_file("leetcode.apkg")
