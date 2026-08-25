import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

from modules.perception import VisualPerception
from modules.action import ActionGeneration
from modules.state_manager import StateManager
from modules.feedback import FeedbackLoop

BASE_URL = "http://127.0.0.1:5500"
TARGET_URL = f"{BASE_URL}/amazon.html"

async def main():
    print("🚀 Starting Autonomous Visual Agent...")

    state = StateManager()
    perception = VisualPerception()
    action = ActionGeneration()
    feedback = FeedbackLoop()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})

        # 🌟 GLOBAL SCRIPT: Persists across ALL pages
        await context.add_init_script("""
            window.clickAddToCart = function(productName, quantity) {
                const buttons = document.querySelectorAll('.add-to-cart-button');
                for (let btn of buttons) {
                    const container = btn.closest('.product-container');
                    if (container && container.textContent.includes(productName)) {
                        for (let i = 0; i < quantity; i++) { btn.click(); }
                        return true;
                    }
                }
                return false;
            };

            window.selectDelivery = function(productName, optionText) {
                const containers = document.querySelectorAll('.cart-item-container');
                for (let container of containers) {
                    if (container.textContent.includes(productName)) {
                        const options = container.querySelectorAll('.js-delivery-option');
                        for (let option of options) {
                            if (option.textContent.includes(optionText)) {
                                option.click();
                                return true;
                            }
                        }
                    }
                }
                return false;
            };

            window.clickCartLink = function() {
                const link = document.querySelector('.cart-link');
                if (link) { link.click(); return true; }
                return false;
            };

            // 🆕 BULLETPROOF VERIFICATION: Reads the DOM to count unique delivery dates
            window.verifyThreeDifferentDates = function() {
                const dates = document.querySelectorAll('.delivery-date');
                const uniqueDates = new Set();
                dates.forEach(d => {
                    const text = d.textContent.trim().replace('Delivery date:', '').trim();
                    if(text) uniqueDates.add(text);
                });
                return uniqueDates.size >= 3;
            };
        """)

        page = await context.new_page()

        print(f"🌍 Loading: {TARGET_URL}")
        try:
            await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_selector('text=Adults Plain Cotton T-Shirt', timeout=15000)
            await page.evaluate("window.scrollTo(0, 0)")
        except Exception as e:
            print(f"   ↳ Loading warning: {e}")

        print("Waiting 4 seconds for images to render...")
        await asyncio.sleep(4)
        print("🧠 Entering Autonomous Agentic Loop...\n")

        try:
            while not state.get_state()["task_complete"] and state.get_state()["attempts"] < 12:
                current_phase = state.get_state()["current_phase"]

                # 1. PERCEIVE
                vlm_data = await perception.analyze_environment(page, current_phase)

                # 4. FEEDBACK on verification phases
                if current_phase in ["verify_cart", "verify_delivery", "verify_order"]:
                    eval_result = feedback.evaluate_action(vlm_data, current_phase)
                    state.set_feedback(eval_result)
                    if eval_result["task_complete"]:
                        state.set_task_complete(True)
                        break
                    else:
                        state.update_phase(eval_result["next_phase"])
                        state.increment_attempts()
                        continue

                # 3. ACT
                next_phase = await action.execute_action(page, vlm_data, current_phase)

                # 2. UPDATE STATE
                state.update_phase(next_phase)
                await asyncio.sleep(2)
        except Exception as e:
            print(f"\n⚠️ Agent interrupted: {e}")

        if state.get_state()["task_complete"]:
            print("\n🏆 SUCCESS: Agent achieved the goal autonomously!")
        else:
            print("\n💀 FAILURE: Agent reached max attempts.")

        print("🏁 Agent Loop Finished.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())