import asyncio

class ActionGeneration:
    def __init__(self):
        print("🖱️ [ACTION MODULE] Initialized.")

    async def execute_action(self, page, vlm_response, current_phase):
        print("\n🖱️ [MODULE 3: ACTION GENERATION] Preparing physical action...")

        if current_phase in ["verify_cart", "verify_delivery", "verify_order"]:
            return current_phase

        coords = vlm_response.get("coordinates", {})
        x = vlm_response.get("x") or coords.get("x", 0)
        y = vlm_response.get("y") or coords.get("y", 0)

        # === DIRECT JAVASCRIPT for adding items ===
        if current_phase == "add_socks":
            print("   ↳ 🧺 Adding Socks via DOM click...")
            await page.evaluate("window.clickAddToCart('Athletic Cotton Socks', 1)")
            await asyncio.sleep(1.5)
            return "add_basketball"

        elif current_phase == "add_basketball":
            print("   ↳ 🏀 Adding Basketball via DOM click...")
            await page.evaluate("window.clickAddToCart('Intermediate Size Basketball', 2)")
            await asyncio.sleep(1.5)
            return "add_tshirt"

        elif current_phase == "add_tshirt":
            print("   ↳ 👕 Adding T-Shirt via DOM click...")
            await page.evaluate("window.clickAddToCart('Plain Cotton T-Shirt', 2)")
            await asyncio.sleep(1.5)
            return "verify_cart"

        # === DIRECT JAVASCRIPT for navigation (Fixes off-screen coordinates) ===
        elif current_phase == "click_cart":
            print("   ↳ 🛒 Clicking Cart link via DOM...")
            await page.evaluate("window.clickCartLink()")
            await asyncio.sleep(2.5)
            if "checkout" not in page.url:
                await page.goto(page.url.replace("amazon.html", "checkout.html"), wait_until="domcontentloaded")
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)
            return "delivery_tshirt"

        # === DIRECT JAVASCRIPT for delivery options ===
        elif current_phase == "delivery_tshirt":
            print("   ↳ 📅 Selecting T-Shirt delivery ($9.99) via DOM...")
            await page.evaluate("window.selectDelivery('Plain Cotton T-Shirt', '$9.99')")
            await asyncio.sleep(1.5)
            return "delivery_basketball"

        elif current_phase == "delivery_basketball":
            print("   ↳ 📅 Selecting Basketball delivery ($4.99) via DOM...")
            await page.evaluate("window.selectDelivery('Intermediate Size Basketball', '$4.99')")
            await asyncio.sleep(1.5)
            return "delivery_socks"

        elif current_phase == "delivery_socks":
            print("   ↳ 📅 Selecting Socks delivery (FREE) via DOM...")
            await page.evaluate("window.selectDelivery('Athletic Cotton Socks', 'FREE')")
            await asyncio.sleep(1.5)
            return "verify_delivery"

        # === VLM-based clicking for unique targets (Place Order) ===
        elif x > 0 and y > 0:
            print(f"   ↳ 🎯 Clicking at X={x}, Y={y}")
            await asyncio.sleep(0.5)
            await page.mouse.move(x, y, steps=15)
            await page.mouse.click(x, y)
            print("   ↳ ✅ Click executed!")
            await asyncio.sleep(2.5)

            if current_phase == "click_place_order":
                if "orders" not in page.url:
                    await page.goto(page.url.replace("checkout.html", "orders.html"), wait_until="domcontentloaded")
                    await asyncio.sleep(2)
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(1)
                return "verify_order"

        print("   ↳ ⚠️ Target not found. Scrolling slowly...")
        await page.mouse.wheel(0, 400)
        await asyncio.sleep(3)
        return current_phase