function count_current_question() {
  return document.getElementsByClassName("question-box").length + 1
}

function add_question(qcount) {
  var question_box = document.createElement("div")
  question_box.setAttribute("name", "question-box-" + qcount)
  question_box.className = "question-box"

  var question = document.createElement("p")
  question.innerHTML = "Question"
  question_box.appendChild(question)

  var question_text = document.createElement("input")
  question_text.className = "question-text"
  question_text.setAttribute("name", "q" + qcount + "-question")
  question_text.type = "text"
  question_text.placeholder = "Enter question text"
  question_box.appendChild(question_text)
  question_box.appendChild(document.createElement("br"))

  for (let i = 1; i < 5; i++) {
    var answer_text = document.createElement("input")
    answer_text.type = "text"
    answer_text.setAttribute("name", "q" + (qcount) + "-answer-" + i)
    answer_text.placeholder = "Enter answer text"
    question_box.appendChild(answer_text)

    if (i == 2) {
      question_box.appendChild(document.createElement("br"))
    }
  }

  question_box.appendChild(document.createElement("br"))

  correct_answer = document.createElement("input")
  correct_answer.className = "correct-answer"
  correct_answer.placeholder = "correct answer"
  correct_answer.type = "number"
  correct_answer.setAttribute("min", 1)
  correct_answer.setAttribute("max", 4)
  correct_answer.setAttribute("required", true)
  correct_answer.setAttribute("name", "q" + qcount + "-correct")
  question_box.appendChild(correct_answer)

  question_box.appendChild(document.createElement("br"))

  delete_button = document.createElement("button")
  delete_button.id = "q-" + (qcount + 1) + "-delete-btn"
  delete_button.setAttribute("onclick", "delete_current_question(this.id)")
  delete_button.innerHTML = "delete question"
  question_box.appendChild(delete_button)

  question_box.appendChild(document.createElement("br"))
  question_box.appendChild(document.createElement("br"))

  var question_div = document.getElementById("question-div")
  question_div.appendChild(question_box)
}

function delete_current_question(id) {
  question = document.getElementById(id).parentNode
  question_box = question.parentNode
  question_box.removeChild(question)
}

