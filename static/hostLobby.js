function updateLobby(playerList) {
  console.log("player list", playerList)

  lobby = document.getElementById("players")
  lobby.innerHTML = ""

  for (var i = 0; i < playerList.length; i++) {
    player = document.createElement("p")
    player.className = "player-lobby"
    player.id = "player-" + i

    console.log(playerList[i])

    textNode = document.createTextNode(playerList[i]['name'])
    player.appendChild(textNode)

    lobby.appendChild(player)
  }
}

function startGame() {
  pin = document.getElementById("room-id").value
  socket.emit("start-game", {"pin": pin})
}
