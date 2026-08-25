class PromptManager:
    @staticmethod
    def get_prompt(phase):
        prompts = {
            "add_socks": (
                "Look at this Amazon search results page. Find the product with the title 'Black and Gray Athletic Cotton Socks - 6 Pairs'. "
                "Locate the yellow 'Add to Cart' button that belongs to THIS specific product. "
                "Respond with the exact X and Y pixel coordinates of the CENTER of that yellow button, in raw JSON only. "
                "Example: {\"x\": 450, \"y\": 600, \"found\": true}"
            ),
            "add_basketball": (
                "Look at this Amazon search results page. Find the product with the title 'Intermediate Size Basketball'. "
                "Locate the yellow 'Add to Cart' button that belongs to THIS specific product. "
                "Respond with the exact X and Y pixel coordinates of the CENTER of that yellow button, in raw JSON only. "
                "Example: {\"x\": 700, \"y\": 600, \"found\": true}"
            ),
            "add_tshirt": (
                "Look at this Amazon search results page. Find the product with the title 'Adults Plain Cotton T-Shirt - 2 Pack'. "
                "Locate the yellow 'Add to Cart' button that belongs to THIS specific product. "
                "Respond with the exact X and Y pixel coordinates of the CENTER of that yellow button, in raw JSON only. "
                "Example: {\"x\": 450, \"y\": 750, \"found\": true}"
            ),
            "verify_cart": (
                "Look at the top-right corner of the page showing the shopping cart icon. "
                "Is there a number 5 or higher displayed on the cart badge? "
                "Respond in raw JSON only. Example: {\"success\": true, \"reason\": \"cart shows 5\"}"
            ),
            "click_cart": (
                "Look at the dark header bar at the top of the page. "
                "Find the cart link on the top-right (the cart icon next to the word 'Cart'). "
                "Respond with the exact X and Y pixel coordinates of the center of that cart link, in raw JSON only. "
                "Example: {\"x\": 1200, \"y\": 60, \"found\": true}"
            ),
            "delivery_tshirt": (
                "You are on an Amazon Checkout page with multiple items. "
                "Look at the LAST product section (usually at the bottom of the item list). "
                "Find the radio button or text that says '$9.99 - Shipping' (this is the fastest delivery). "
                "Respond with the exact X and Y pixel coordinates of that option in raw JSON only. "
                "Example: {\"x\": 300, \"y\": 600, \"found\": true}"
            ),
            "delivery_basketball": (
                "You are on an Amazon Checkout page with multiple items. "
                "Look for the product section that contains a basketball image. "
                "Find the radio button or text that says '$4.99 - Shipping' (this is the middle delivery option). "
                "Respond with the exact X and Y pixel coordinates of that option in raw JSON only. "
                "Example: {\"x\": 300, \"y\": 600, \"found\": true}"
            ),
            "delivery_socks": (
                "You are on an Amazon Checkout page with multiple items. "
                "Look for the product section that contains socks image. "
                "Find the radio button or text that says 'FREE' shipping. "
                "Respond with the exact X and Y pixel coordinates of that option in raw JSON only. "
                "Example: {\"x\": 300, \"y\": 600, \"found\": true}"
            ),
            "verify_delivery": (
                "You are on the Amazon Checkout page. "
                "Look at the 'Delivery date:' line at the top of each item box. "
                "Are there three different delivery dates visible (one per item)? "
                "Respond in raw JSON only. Example: {\"success\": true, \"reason\": \"three different dates visible\"}"
            ),
            "click_place_order": (
                "You are on the Amazon Checkout page. Find the yellow 'Place your order' button inside the Order Summary box on the right side. "
                "Respond with the exact X and Y pixel coordinates of the center of that button, in raw JSON only. "
                "Example: {\"x\": 900, \"y\": 650, \"found\": true}"
            ),
            "verify_order": (
                "You are on the 'Your Orders' page. Is there an order box that contains the product 'Adults Plain Cotton T-Shirt - 2 Pack'? "
                "Respond in raw JSON only. Example: {\"success\": true, \"reason\": \"order with t-shirt visible\"}"
            ),
        }
        # 🆕 Robust fallback: if phase is unknown, give a safe JSON response
        return prompts.get(phase, "{\"found\": false, \"reason\": \"unknown phase\"}")