import asyncio

class ActionGeneration:
    def __init__(self):
        print("🖱️ [ACTION MODULE] Initialized.")

    async def execute_action(self, page, vlm_response, current_phase):
        print("\n🖱️ [MODULE 3: ACTION GENERATION] Preparing physical action...")

        # Skip physical actions for verification phases
        if current_phase in ["verify_cart", "verify_delivery", "verify_order"]:
            return current_phase

        coords = vlm_response.get("coordinates", {})
        x = vlm_response.get("x") or coords.get("x", 0)
        y = vlm_response.get("y") or coords.get("y", 0)

        # ==========================================
        # DOM CLICKS FOR ADDING ITEMS
        # ==========================================
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

        # ==========================================
        # CART NAVIGATION (Two-Tier Motor Recovery)
        # ==========================================
        elif current_phase == "click_cart":
            print("   ↳ 🛒 Attempting Cart Link click...")

            # 🆕 Tier 1: VLM coordinates (Vision-first)
            if 0 < x <= 1280 and 0 < y <= 800:
                print(f"   ↳ 🎯 VLM trying Cart Link at X={x}, Y={y}")
                await page.mouse.move(x, y, steps=15)
                await page.mouse.click(x, y)
                await asyncio.sleep(1.5)

            # Tier 2: Motor Recovery (Playwright native click)
            if "checkout" not in page.url:
                print("   ↳ 🔄 VLM missed. Engaging Motor Recovery (Playwright native click)...")
                try:
                    await page.click('.cart-link', timeout=3000)
                    await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"   ↳ ⚠️ Native click failed: {str(e)[:50]}")

            # Final check
            if "checkout" in page.url:
                print("   ↳ ✅ Successfully navigated to checkout via UI interaction!")
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(1)
                return "delivery_tshirt"
            else:
                print("   ↳ ⚠️ Still not on checkout. Retrying phase...")
                return "click_cart"

        # ==========================================
        # DOM CLICKS FOR DELIVERY OPTIONS
        # ==========================================
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

        # ==========================================
        # PLACE ORDER (Two-Tier Motor Recovery)
        # ==========================================
        elif current_phase == "click_place_order":
            
            # Tier 1: VLM Coordinates
            if 0 < x <= 1280 and 0 < y <= 800:
                print(f"   ↳ 🎯 VLM trying Place Order at X={x}, Y={y}")
                await page.mouse.move(x, y, steps=15)
                await page.mouse.click(x, y)
                await asyncio.sleep(1.5)

            # Tier 2: Motor Recovery (Playwright native click)
            if "orders" not in page.url:
                print("   ↳ 🔄 VLM missed. Engaging Motor Recovery (Playwright native click)...")
                try:
                    await page.click('.place-order-button', timeout=3000)
                    await asyncio.sleep(1.5)
                except Exception as e:
                    print(f"   ↳ ⚠️ Native click failed: {str(e)[:50]}")

            # Final Check
            if "orders" in page.url:
                print("   ↳ ✅ Successfully navigated to orders via UI interaction!")
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(1)
                return "verify_order"
            else:
                print("   ↳ ⚠️ Still not on orders page. Retrying phase...")
                return "click_place_order"

        # ==========================================
        # FALLBACK: Scroll if VLM found nothing
        # ==========================================
        print("   ↳ ⚠️ Target not found. Scrolling slowly...")
        await page.mouse.wheel(0, 400)
        await asyncio.sleep(3)
        return current_phase