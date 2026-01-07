import asyncio
import websockets
import requests
import sys

SERVER = "https://your-app-name.onrender.com"  # change to Render URL later

async def chat():
    try:
        username = input("Username: ").strip()
        room = input("Room (general / tech / random): ").strip()

        # 🔐 LOGIN
        res = requests.post(
            f"{SERVER}/auth/login",
            json={"username": username},
            timeout=5
        )

        if res.status_code != 200:
            print("Login failed:", res.text)
            input("Press Enter to exit...")
            return

        token = res.json().get("token")
        if not token:
            print("No token received")
            input("Press Enter to exit...")
            return

        ws_url = SERVER.replace("http", "ws") + f"/ws/{room}?token={token}"

        async with websockets.connect(ws_url):
            print(f"Connected to room '{room}' 🔐")
            print("Type messages and press Enter.\n")

            async with websockets.connect(ws_url) as ws:

                async def send():
                    while True:
                        msg = await asyncio.to_thread(input)
                        await ws.send(msg)

                async def receive():
                    while True:
                        msg = await ws.recv()
                        print(msg)

                await asyncio.gather(send(), receive())

    except KeyboardInterrupt:
        print("\nBye 👋")
    except Exception as e:
        print("Error:", e)
        input("Press Enter to exit...")

def main():
    asyncio.run(chat())

if __name__ == "__main__":
    main()
