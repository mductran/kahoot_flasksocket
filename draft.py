form = {'socketid': 'asdfqwer', 'q1-question': '345', 'q1-answer-1': 'asd', 'q1-answer-2': 'xc', 'q1-answer-3': 'rew', 'q1-answer-4': 'sdf', 'q1-correct': '1',
        'q2-question': '7465', 'q2-answer-1': 'drty', 'q2-answer-2': 'dfer', 'q2-answer-3': 'yter', 'q2-answer-4': 'dhfg', 'q2-correct': '2'}
questions = []
question = {}

form.pop("socketid")

for index in enumerate(form, 1):
    question[index[1]] = form[index[1]]
    if len(question) == 6:
        questions.append(question)
        question = {}

for i in questions:
    print(i)
    print()

# room = {
#     "room_id": room_id,
#     "questions": questions,
#     "host_id": request.socket,
#     "players": []
# }
# room_collection.insert_one(room)