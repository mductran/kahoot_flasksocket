function playerAnswer(choice) {
  if (answered == false) {
    answered = true

    console.log("player choose answer number", choice)
    socket.emit("player-answer", {'choice': choice, "id": socket.id})

    // after player choose an answer, lock the buttons
    buttons = document.getElementsByClassName("answer-button")

    for (var i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true
    }

    textNode = document.createTextNode("Submitted. Waiting for other players to answer...")
    document.getElementById("answer-submitted-message").appendChild(textNode)
  }

}
