import base64
import json
import os
import re
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True) 

class VLMClient:
    def __init__(self):
        self.provider = os.getenv("VLM_PROVIDER", "mistral").lower()
        self.client = None
        self.model = ""

        if self.provider == "mistral":
            api_key = os.getenv("MISTRAL_API_KEY", "").strip()
            
            if not api_key:
                raise ValueError("❌ MISTRAL_API_KEY not found in your .env file!")
            
            print(f"   ↳ 🔑 Using Mistral key starting with: {api_key[:6]}...")
            
            # Connect to Mistral's OpenAI-compatible API
            self.client = OpenAI(api_key=api_key, base_url="https://api.mistral.ai/v1")
            self.model = "pixtral-12b-2409"
            print(f"🧠 [VLM CLIENT] Initialized Mistral {self.model} (FREE tier).")
            # Connect to Mistral's OpenAI-compatible API
            self.client = OpenAI(api_key=api_key, base_url="https://api.mistral.ai/v1")
            # Pixtral is Mistral's Vision-Language Model, perfect for UI coordinates
            self.model = "pixtral-12b-2409"
            print(f"🧠 [VLM CLIENT] Initialized Mistral {self.model} (FREE tier).")

        elif self.provider == "ollama":
            self.client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
            self.model = os.getenv("OLLAMA_MODEL", "llama3.2-vision")
            print(f"🧠 [VLM CLIENT] Initialized local Ollama ({self.model}).")

        elif self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("❌ GEMINI_API_KEY not found in .env!")
            self.client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            print(f"🧠 [VLM CLIENT] Initialized Gemini {self.model}.")
            
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _encode_image(self, image_bytes):
        return base64.b64encode(image_bytes).decode('utf-8')

    def _extract_json(self, raw_text):
        """Rescues JSON even if the model wraps it in markdown or cuts it off."""
        if not raw_text: return None
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        # Regex rescue for coordinates (e.g. if the model just outputs {"x": 450, "y": 200)
        x = re.search(r'["\']?x["\']?\s*:\s*(\d+)', cleaned)
        y = re.search(r'["\']?y["\']?\s*:\s*(\d+)', cleaned)
        if x and y:
            return {"x": int(x.group(1)), "y": int(y.group(1)), "found": True}

        s = re.search(r'["\']?success["\']?\s*:\s*(true|false)', cleaned, re.I)
        if s:
            return {"success": s.group(1).lower() == "true", "reason": "parsed via regex"}

        return None

    async def analyze(self, image_bytes, prompt, max_retries=2):
        base64_image = self._encode_image(image_bytes)

        for attempt in range(max_retries):
            try:
                # Mistral uses the exact same OpenAI SDK format!
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    max_tokens=300,
                    temperature=0.1,
                )

                raw_text = response.choices[0].message.content
                print(f"   ↳ 🤖 Mistral Raw Reply: {raw_text[:150]}...") 
                
                parsed = self._extract_json(raw_text)

                if parsed is not None:
                    return parsed
                else:
                    print(f"   ↳ ⚠️ Could not parse JSON. Raw: {raw_text[:100]}")
                    return {"found": False, "error": "unparseable"}

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "rate limit" in error_str.lower():
                    wait_time = 15 * (attempt + 1)
                    print(f"   ↳ ⏳ Rate limit hit. Waiting {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    print(f"   ↳ ❌ VLM API Error: {error_str[:150]}")
                    return {"error": error_str, "found": False}

        return {"error": "max_retries", "found": False}