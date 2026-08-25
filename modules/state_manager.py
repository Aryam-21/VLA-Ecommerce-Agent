class StateManager:
    def __init__(self):
        self.state = {
            "goal": "Add socks, basketball, t-shirt, go to checkout, set 3 delivery dates.",
            "current_phase": "add_socks",  # ← Must start here!
            "attempts": 0,
            "task_complete": False,
            "last_feedback": None
        }
        print("🧠 [STATE TRACKING MODULE] Initialized.")

    def get_state(self): return self.state
    def update_phase(self, new_phase):
        self.state["current_phase"] = new_phase
        print(f"   ↳ 🧠 State updated to: {new_phase}")
    def increment_attempts(self): self.state["attempts"] += 1
    def set_task_complete(self, complete): self.state["task_complete"] = complete
    def set_feedback(self, feedback): self.state["last_feedback"] = feedback