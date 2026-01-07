let socket = null;
let token = null;
let roomName = "";

const SERVER = "https://nebula-backend-6co0.onrender.com";

/* =====================
   REGISTER
===================== */
async function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const error = document.getElementById("error");

  if (!username || !password) {
    error.innerText = "Username and password required";
    return;
  }

  const res = await fetch(`${SERVER}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    error.innerText = "Registration failed";
    return;
  }

  error.innerText = "Registered. Now login.";
}

/* =====================
   LOGIN
===================== */
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const room = document.getElementById("room").value.trim();
  const error = document.getElementById("error");

  if (!username || !password || !room) {
    error.innerText = "Username, password and room required";
    return;
  }

  const res = await fetch(`${SERVER}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    error.innerText = "Login failed";
    return;
  }

  const data = await res.json();
  token = data.token;
  roomName = room;

  connectWebSocket();
}

/* =====================
   WEBSOCKET
===================== */
function connectWebSocket() {
  document.getElementById("login").hidden = true;
  document.getElementById("chat").hidden = false;
  document.getElementById("room-title").innerText = `Room: ${roomName}`;

  const wsUrl = SERVER.startsWith("https")
    ? SERVER.replace("https", "wss")
    : SERVER.replace("http", "ws");

  socket = new WebSocket(`${wsUrl}/ws/${roomName}?token=${token}`);

  socket.onmessage = (event) => {
    const data = event.data;

    if (data.startsWith("__PRESENCE__:")) {
      const users = data.replace("__PRESENCE__:", "").split(",");
      const list = document.getElementById("users");
      list.innerHTML = "";

      users.filter(Boolean).forEach(u => {
        const li = document.createElement("li");
        li.innerText = u;
        list.appendChild(li);
      });
      return;
    }

    const messages = document.getElementById("messages");
    messages.innerHTML += `<div>${data}</div>`;
    messages.scrollTop = messages.scrollHeight;
  };
}

/* =====================
   SEND MESSAGE
===================== */
function sendMessage() {
  const input = document.getElementById("message");
  const text = input.value.trim();
  if (!text || !socket) return;

  socket.send(text);
  input.value = "";
}

document.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
