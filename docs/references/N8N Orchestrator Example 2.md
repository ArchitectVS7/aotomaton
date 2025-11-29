

# 📘 **Claude Code — n8n Orchestrator (Docker + Windows 10 Edition)**

**Version:** 1.1
**Target OS:** Windows 10
**Author:** ChatGPT (Thursian Mode)

This orchestrator allows **n8n running inside Docker** to send text **directly into Claude Code** inside Claude Desktop on your Windows 10 machine.

Because Claude Code has **no API**, integration works by running a Windows-side automation script that:

1. Activates Claude Desktop
2. Opens the Claude Code input box
3. Pastes text
4. Presses Enter

n8n simply triggers that script.

---

# 1. 🧱 Architecture Overview (Windows 10)

```
n8n (Docker)
   ↓ Execute Command
Host Windows Script (AutoHotKey)
   ↓
Claude Desktop → Claude Code
```

Key requirement:
🔹 Windows host must have **AutoHotKey v1.1** or **v2** installed (v1 script is included below).

---

# 2. 🐳 Docker Setup (Windows 10)

Place this file in your project directory as:

```
docker-compose.yml
```

```yaml
version: "3.8"

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    ports:
      - "5678:5678"
    environment:
      - TZ=America/Chicago
      - N8N_BASIC_AUTH_ACTIVE=false
    volumes:
      - ./n8n_data:/home/node/.n8n
      - ./claude-bridge:/claude-bridge
    restart: unless-stopped
```

Directory structure to create:

```
project-root/
│
├─ docker-compose.yml
├─ n8n_data/
└─ claude-bridge/
       ├─ claude-code-win.ahk
       └─ run-claude-win.cmd
```

Bring n8n online:

```
docker compose up -d
```

Open n8n at:

```
http://localhost:5678
```

---

# 3. 🪄 Claude Bridge (Windows Scripts)

All scripts below go in:

```
project-root/claude-bridge/
```

---

# **3A. AutoHotKey script (Windows 10)**

File: `claude-code-win.ahk`

```ahk
#SingleInstance Force
SendMode Input

; Receive argument from CMD
FullText := ""
Loop %0%
{
    Param := %A_Index%
    FullText := FullText . Param . " "
}

; Copy text to clipboard
Clipboard := FullText
ClipWait, 0.5

; Launch or activate Claude Desktop
Run, % "C:\Users\" A_UserName "\AppData\Local\Programs\Claude\Claude.exe"
WinWaitActive, ahk_exe Claude.exe, , 3

Sleep, 400

; Open Claude Code panel (Ctrl+I)
Send ^i
Sleep, 250

; Paste text
Send ^v
Sleep, 300

; Press Enter
Send {Enter}
```

> If Claude Desktop is in a non-standard location, update the `Run` line.

---

# **3B. Command Wrapper (n8n → Windows script)**

File: `run-claude-win.cmd`

```cmd
@echo off
set TEXT=%*
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%~dp0claude-code-win.ahk" %TEXT%
```

This ensures n8n can call a CMD file instead of trying to invoke AutoHotKey directly.

---

# 4. 📡 n8n Workflow JSON (Windows-ready)

Create a workflow in n8n → **Import from File** → paste this:

```json
{
  "name": "Claude Code Windows Orchestrator",
  "nodes": [
    {
      "id": "1",
      "name": "Receive Prompt",
      "type": "n8n-nodes-base.webhook",
      "position": [300, 250],
      "parameters": {
        "path": "send-to-claude",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "responseData": {
          "responseBody": "OK"
        }
      }
    },
    {
      "id": "2",
      "name": "Send To Claude Code",
      "type": "n8n-nodes-base.executeCommand",
      "position": [650, 250],
      "parameters": {
        "command": "cmd.exe /c \"C:\\\\path\\\\to\\\\project-root\\\\claude-bridge\\\\run-claude-win.cmd\" \"{{$json[\"text\"]}}\""
      }
    }
  ],
  "connections": {
    "Receive Prompt": {
      "main": [
        [
          {
            "node": "Send To Claude Code",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

🔧 **Update the command path** so it points to your local `run-claude-win.cmd`.

Example:

```
cmd.exe /c "C:\Users\You\Documents\claude-orchestrator\claude-bridge\run-claude-win.cmd" "{{$json["text"]}}"
```

---

# 5. 🔌 Webhook → Claude Code Trigger

Send a POST request:

```
POST http://localhost:5678/webhook/send-to-claude
```

Body:

```json
{
  "text": "Write a Python function to flatten nested dictionaries."
}
```

Claude Code should:

1. Activate
2. Open the Code input panel
3. Paste the text
4. Hit Enter

You’ll see the message appear exactly as though you typed it.

---

# 6. 🧪 Test Command (PowerShell or CMD)

```
curl -X POST http://localhost:5678/webhook/send-to-claude ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"Hello from Windows + n8n Docker!\"}"
```

---

# 7. 🧰 Optional Enhancements (Windows Edition)

You can extend this orchestrator:

### Idea A — Add a queue

Write a tiny Node.js file logger:

```
claude-bridge/queue.js
```

And change the Execute Command to:

```
node C:\path\to\queue.js "{{$json["text"]}}"
```

### Idea B — Add STOP gates

Block or allow messages based on JSON flags before sending to Claude.

### Idea C — Add Claude API validation

Use the Anthropic API to pre-check or refine the text before sending it into Claude Code.

---

# 8. 🎉 Done — You Now Have a Full Windows 10 Claude-Code Orchestrator

**From outside your PC** (webhook, mobile, browser, GitHub Actions),
you can now do:

```
Send → n8n → Windows script → Claude Code → Runs the action
```


---
