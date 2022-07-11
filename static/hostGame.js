function updateTimer() {
  remaining_time = 5
  timer = setInterval(() => {
    remaining_time = remaining_time - 1
    document.getElementById("time-left").textContent = remaining_time
    if (remaining_time == 0) {
      socket.emit("question-time-up", {
        "id": pathname[3]
      })
    }
  }, 1000)
}

function nextQuestion() {
  document.getElementById("next-question").style.display = "none"

  // document.getElementById('square1').style.display = "none";
  // document.getElementById('square2').style.display = "none";
  // document.getElementById('square3').style.display = "none";
  // document.getElementById('square4').style.display = "none";

  document.getElementById('answer-1').style.filter = "none"
  document.getElementById('answer-2').style.filter = "none"
  document.getElementById('answer-3').style.filter = "none"
  document.getElementById('answer-4').style.filter = "none"

  document.getElementById('answered-player-num').style.display = "block"
  document.getElementById('timer').style.display = "block"
  document.getElementById('time-left').innerHTML = "5"
  socket.emit('next-question', {"id": pathname[3]}) //Tell server to start new question
}

function updateAnsweredPlayers(data) {

  console.log("update data", data)

  players_in_game = data.players_in_game
  answered_players = data.answered_players

  document.getElementById("answered-player-num").innerHTML = "Players answered: " + answered_players + " / " + players_in_game
}

function gameOver(data) {
  document.getElementById("quiz").style.display = "none"
  document.getElementById("result").style.display = "none"
  document.getElementById("ranking").style.display = "block"

  document.getElementById("first").innerHTML = "1." + data.first
  document.getElementById("second").innerHTML = "2." + data.second
  document.getElementById("third").innerHTML = "3." + data.third
}

function questionOver(data) {
  clearInterval(timer)
  document.getElementById("timer").style.display = "none"
  document.getElementById("answered-player-num").style.display = "none"

  var answer1 = 0
  var answer2 = 0
  var answer3 = 0
  var answer4 = 0
  total_answered = 0

  correct = data['correct_answer']

  for (var i = 1; i < 5; i++) {
    if (i == correct) {
      current_answer = document.getElementById("answer-" + i).innerHTML
      document.getElementById("answer-" + i).innerHTML = "&#10004 " + current_answer
    } else {
      document.getElementById("answer-" + i).style.filter = "grayscale(50%)"
    }data['id']
  }

  for (var i = 0; i < data['players'].length; i++) {
    player_choice = data['players'][i]['game_data']['choice']
    if (player_choice == 1) {
      answer1 += 1
    } else if (player_choice == 2) {
      answer2 += 1
    } else if (player_choice == 3) {
      answer3 += 1
    } else if (player_choice == 4) {
      answer4 += 1
    }
    total_answered += 1
  }

  //Gets values for graph
  answer1 = answer1 / total_answered * 100
  answer2 = answer2 / total_answered * 100
  answer3 = answer3 / total_answered * 100
  answer4 = answer4 / total_answered * 100

  document.getElementById('square1').style.display = "inline-block"
  document.getElementById('square2').style.display = "inline-block"
  document.getElementById('square3').style.display = "inline-block"
  document.getElementById('square4').style.display = "inline-block"

  document.getElementById('square1').style.height = answer1 + "px"
  document.getElementById('square2').style.height = answer2 + "px"
  document.getElementById('square3').style.height = answer3 + "px"
  document.getElementById('square4').style.height = answer4 + "px"

  document.getElementById('next-question').style.display = "block"

}


function gameQuestions(data) {

  console.log("next question data", data)

  document.getElementById("question-text").innerHTML = "Question: " + data.question
  document.getElementById("answer-1").innerHTML = data["answers"][0]
  document.getElementById("answer-2").innerHTML = data["answers"][1]
  document.getElementById("answer-3").innerHTML = data["answers"][2]
  document.getElementById("answer-4").innerHTML = data["answers"][3]

  correctAnswer = data['correct']
  document.getElementById("answered-player-num").innerHTML = "Players answered: 0 / " + data['players-in-game']
  updateTimer()
}