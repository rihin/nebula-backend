let socket = null;
let token = null;
let roomName = "";

const SERVER = "https://nebula-backend-6co0.onrender.com";

/* =====================
   LOGIN
===================== */
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

/* =====================
   WEBSOCKET
===================== */
function connectWebSocket() {
  document.getElementById("login").hidden = true;
  document.getElementById("chat").hidden = false;
  document.getElementById("room-title").innerText = `Room: ${roomName}`;

  const wsUrl =
    SERVER.startsWith("https")
      ? SERVER.replace("https", "wss")
      : SERVER.replace("http", "ws");

  socket = new WebSocket(`${wsUrl}/ws/${roomName}?token=${token}`);

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    const data = event.data;

    /* 🔥 PRESENCE UPDATE */
    if (data.startsWith("__PRESENCE__:")) {
      const users = data.replace("__PRESENCE__:", "").split(",");
      const list = document.getElementById("users");
      list.innerHTML = "";

      users.filter(Boolean).forEach(user => {
        const li = document.createElement("li");
        li.innerText = user;
        list.appendChild(li);
      });
      return;
    }

    /* 💬 CHAT MESSAGE */
    const messages = document.getElementById("messages");
    messages.innerHTML += `<div>${data}</div>`;
    messages.scrollTop = messages.scrollHeight;
  };

  socket.onerror = () => {
    console.error("WebSocket error");
  };

  socket.onclose = () => {
    console.warn("WebSocket disconnected");
  };
}

/* =====================
   SEND MESSAGE
===================== */
function sendMessage() {
  const input = document.getElementById("message");
  const text = input.value.trim();

  if (!text || !socket || socket.readyState !== WebSocket.OPEN) return;

  socket.send(text);
  input.value = "";
}



async function register() {
  const u = username.value;
  const p = password.value;

  const res = await fetch(`${SERVER}/auth/register?username=${u}&password=${p}`, {
    method: "POST"
  });

  if (!res.ok) {
    error.innerText = "Registration failed";
    return;
  }

  error.innerText = "Registered. Now login.";
}

async function login() {
  const u = username.value;
  const p = password.value;

  const res = await fetch(`${SERVER}/auth/login?username=${u}&password=${p}`, {
    method: "POST"
  });

  if (!res.ok) {
    error.innerText = "Login failed";
    return;
  }

  const data = await res.json();
  token = data.token;
  connectWS();
}

/* =====================
   ENTER KEY SUPPORT
===================== */
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
