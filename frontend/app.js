const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const roomInput = document.getElementById("room");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const error = document.getElementById("error");


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
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();
  const room = roomInput.value.trim();

  if (!username || !password || !room) {
    error.innerText = "Username, password and room are required";
    return;
  }

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

  // Switch UI
  document.getElementById("login").hidden = true;
  document.getElementById("chat").hidden = false;
  document.getElementById("room-title").innerText = `Room: ${room}`;

  connectWS(room);
}

function sendMessage() {
  const msg = messageInput.value.trim();
  if (!msg || !ws || ws.readyState !== WebSocket.OPEN) return;

  ws.send(msg);
  messageInput.value = "";
}

function connectWS(room) {
  const token = localStorage.getItem("token");

  console.log("Connecting WS with token:", token);
  console.log("Room:", room);

  if (!token) {
    alert("No token found. Please login again.");
    return;
  }

  const wsUrl = `wss://nebula-backend-6co0.onrender.com/ws/${room}?token=${token}`;
  console.log("WS URL:", wsUrl);

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  ws.onmessage = (e) => {
    console.log("📩 WS message:", e.data);
    addMessage(e.data);
  };

  ws.onerror = (e) => {
    console.error("❌ WebSocket error", e);
    alert("WebSocket connection failed");
  };

  ws.onclose = (e) => {
    console.warn("⚠️ WebSocket closed", e.code, e.reason);
  };
}
function addMessage(text) {
  // Ignore presence messages for now
  if (text.startsWith("__PRESENCE__")) {
    return;
  }

  const div = document.createElement("div");
  div.innerText = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}
function logout() {
  console.log("Logout clicked");

  if (ws) {
    ws.close();
    ws = null;
  }

  localStorage.clear();

  messages.innerHTML = "";
  messageInput.value = "";
  roomInput.value = "";

  document.getElementById("chat").hidden = true;
  document.getElementById("login").hidden = false;
}