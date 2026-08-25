class FeedbackLoop:
    def __init__(self):
        print("🔍 [FEEDBACK LOOP MODULE] Initialized.")

    def evaluate_action(self, vlm_response, current_phase):
        print("\n🔍 [MODULE 4: FEEDBACK LOOP] Evaluating action outcome...")

        if current_phase == "verify_cart":
            if vlm_response.get("success"):
                print("   ↳ ✅ Success: Cart shows 5 (socks×1 + basketball×2 + t-shirt×2)! Next: checkout.")
                return {"status": "SUCCESS", "task_complete": False, "next_phase": "click_cart"}
            return {"status": "FAILURE", "task_complete": False, "next_phase": "add_tshirt"}

        elif current_phase == "verify_delivery":
            if vlm_response.get("success"):
                print("   ↳ ✅ Success: All 3 items have DIFFERENT delivery dates! Next: place the order.")
                return {"status": "SUCCESS", "task_complete": False, "next_phase": "click_place_order"}
            return {"status": "FAILURE", "task_complete": False, "next_phase": "delivery_tshirt"}

        elif current_phase == "verify_order":
            if vlm_response.get("success"):
                print("   ↳ ✅ Success: Order visible on the hardcoded Orders page!")
                return {"status": "SUCCESS", "task_complete": True, "next_phase": "done"}
            return {"status": "FAILURE", "task_complete": False, "next_phase": "click_place_order"}

        return {"status": "PENDING", "task_complete": False}