const API = "https://nebula-backend-6co0.onrender.com";
let ws = null;

async function register() {
  const username = usernameInput.value;
  const password = passwordInput.value;

  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (!res.ok) {
    error.innerText = data.detail;
    return;
  }

  alert("Registration successful. Please login.");
}

async function login() {
  const username = usernameInput.value;
  const password = passwordInput.value;
  const room = roomInput.value;

  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    error.innerText = "Invalid credentials";
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.token);

  document.getElementById("login").hidden = true;
  document.getElementById("chat").hidden = false;
  document.getElementById("room-title").innerText = `Room: ${room}`;

  connectWS(room);
}

function connectWS(room) {
  const token = localStorage.getItem("token");
  ws = new WebSocket(
    `wss://nebula-backend-6co0.onrender.com/ws/${room}?token=${token}`
  );

  ws.onmessage = (e) => {
    const div = document.createElement("div");
    div.innerText = e.data;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  };
}

function sendMessage() {
  const msg = messageInput.value.trim();
  if (!msg) return;
  ws.send(msg);
  messageInput.value = "";
}

function logout() {
  if (ws) ws.close();
  localStorage.clear();
  location.reload();
}
