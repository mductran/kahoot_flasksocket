// function joinRoom() {
//   console.log("player joining room")
//   player_name = document.getElementById("username").value
//   room_id = document.getElementById("room-id").value
//   socket.emit("player-join", {
//     'player_name': player_name,
//     'room_id': room_id
//   })
// }

function joinRoom() {
  newPath = "/player"
  username = document.getElementById("username").value
  pin = document.getElementById("room-pin").value

  window.location.href = newPath + "/" + username + "/" + pin
}

// function moveToLobby(params) {
//   newPath = "/lobby"
//   Object.keys(params).forEach((key) => {
//     newPath += "/" + params[key]
//   })
//   window.location.href = newPath
// }