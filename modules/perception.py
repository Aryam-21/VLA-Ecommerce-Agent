import asyncio
from agent_brain.vlm_client import VLMClient
from agent_brain.prompts import PromptManager

class VisualPerception:
    def __init__(self):
        self.vlm_client = VLMClient()
        self.prompt_manager = PromptManager()
        print("👁️ [PERCEPTION MODULE] Initialized.")

    async def analyze_environment(self, page, current_phase):
        print("\n👁️ [MODULE 1: VISUAL PERCEPTION] Analyzing current screen...")

        # 🆕 Skip VLM for DOM-handled phases (including verification)
        if current_phase in [
            "add_socks", "add_basketball", "add_tshirt",
            "click_cart",
            "delivery_tshirt", "delivery_basketball", "delivery_socks",
            "verify_delivery"
        ]:
            if current_phase == "verify_delivery":
                print("   ↳ Using DOM/JavaScript to verify 3 different delivery dates...")
                has_three = await page.evaluate("window.verifyThreeDifferentDates()")
                return {"success": has_three, "reason": "DOM verified 3 unique dates"}
            
            print(f"   ↳ Using DOM/JavaScript for {current_phase} (100% reliable)")
            return {"found": True, "x": 0, "y": 0}

        # Neutral mouse position
        await page.mouse.move(640, 750)
        await asyncio.sleep(0.3)

        # Crop top-right corner only when checking the cart number
        clip_area = None
        if current_phase == "verify_cart":
            clip_area = {"x": 1000, "y": 0, "width": 280, "height": 100}

        screenshot_bytes = await page.screenshot(clip=clip_area)
        prompt = self.prompt_manager.get_prompt(current_phase)
        return await self.vlm_client.analyze(screenshot_bytes, prompt)