# 🤖 VLA E-commerce Agent

An autonomous Vision-Language Agent (VLA) that shops on a mock Amazon website:
adds items to the cart, navigates to checkout, selects different delivery dates,
places the order, and visually verifies every step.

## 🏗️ Architecture (4 Modules)

| Module | File | Role |
|---|---|---|
| 👁️ Visual Perception | `modules/perception.py` | Screenshots the screen and queries Mistral Pixtral-12B for coordinates & verification |
| 🧠 State Tracking | `modules/state_manager.py` | Tracks current phase, attempts, and completion |
| 🖱️ Action Generation | `modules/action.py` | Executes mouse clicks and deterministic DOM actions via Playwright |
| 🔍 Feedback Loop | `modules/feedback.py` | Evaluates outcomes and decides the next phase |

##  Agent Workflow

1. Add Socks ×1, Basketball ×2, T-Shirt ×2 to the cart
2. Visually verify the cart badge shows **5**
3. Click the Cart link → checkout page
4. Select **3 different delivery dates** (FREE / $4.99 / $9.99)
5. Verify 3 unique delivery dates
6. Click **"Place your order"**
7. Verify the order on the Orders page → 🏆 SUCCESS

## 🛠️ Tech Stack

- Python 3.10 + Playwright (browser automation)
- Mistral Pixtral-12B (vision-language model, OpenAI-compatible API)
- python-dotenv (secret management)
- Vanilla JS mock e-commerce site with `localStorage` persistence

##  Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 3. Create a .env file with your API key
#    VLM_PROVIDER=mistral
#    MISTRAL_API_KEY=your_key_here

# 4. Serve the mock website (from the website folder)
python -m http.server 5500

# 5. Run the agent
python main.py
```

##  Project Structure

```
VLA-Ecommerce-Agent/
├── main.py               # Orchestrates the agentic loop
├── modules/
│   ├── perception.py     # Module 1: Vision
│   ├── state_manager.py  # Module 2: State
│   ├── action.py         # Module 3: Action
│   └── feedback.py       # Module 4: Feedback
├── agent_brain/
│   ├── vlm_client.py     # Mistral API client (reads .env)
│   └── prompts.py        # Phase-specific VLM prompts
└── website/              # Mock Amazon site (HTML/JS)
```

##  Key Engineering Decisions

- **Hybrid AI + RPA:** VLM handles visual navigation & verification; deterministic DOM clicks handle repetitive UI to guarantee accuracy.
- **Prompt hygiene:** Ambiguous verbs (e.g. "Return") caused VLM hallucinations — replaced with precise instructions.
- **Page-lifecycle handling:** `context.add_init_script()` keeps DOM helpers alive across page navigation.
- **Security:** API key stored in `.env`, excluded from GitHub via `.gitignore`.