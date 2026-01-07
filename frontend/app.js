let socket = null;
let token = null;
let roomName = "";

const SERVER = "https://your-app-name.onrender.com"; 
// change to Render URL later

function login() {
  const username = document.getElementById("username").value.trim();
  const room = document.getElementById("room").value.trim();
  const error = document.getElementById("error");

  if (!username || !room) {
    error.innerText = "Username and room required";
    return;
  }

  fetch(`${SERVER}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username })
  })
  .then(res => res.json())
  .then(data => {
    if (!data.token) {
      error.innerText = "Login failed";
      return;
    }

    token = data.token;
    roomName = room;
    connectWebSocket();
  })
  .catch(() => {
    error.innerText = "Server unreachable";
  });
}

function connectWebSocket() {
  document.getElementById("login").hidden = true;
  document.getElementById("chat").hidden = false;
  document.getElementById("room-title").innerText = `Room: ${roomName}`;

  const wsUrl = SERVER.replace("http", "ws") + `/ws/${roomName}?token=${token}`;
  socket = new WebSocket(wsUrl);

  socket.onmessage = (event) => {
    const messages = document.getElementById("messages");
    messages.innerHTML += `<div>${event.data}</div>`;
    messages.scrollTop = messages.scrollHeight;
  };

  socket.onclose = () => {
    alert("Disconnected from server");
  };
}

function sendMessage() {
  const input = document.getElementById("message");
  if (!input.value) return;
  socket.send(input.value);
  input.value = "";
}
