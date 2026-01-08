let socket = null;
let token = null;
let roomName = "";

const SERVER = "https://nebula-backend-6co0.onrender.com";

/* =====================
   REGISTER
===================== */
async function register() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("https://nebula-backend-6co0.onrender.com/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail);
    return;
  }

  alert("Registration successful. Please login.");
}
/* =====================
   LOGIN
===================== */
async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("https://nebula-backend-6co0.onrender.com/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    alert("Invalid credentials");
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.token);
  localStorage.setItem("username", data.username);

  connectWS();
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
function logout() {
  if (ws) ws.close();
  localStorage.clear();
  location.reload();
}


document.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
