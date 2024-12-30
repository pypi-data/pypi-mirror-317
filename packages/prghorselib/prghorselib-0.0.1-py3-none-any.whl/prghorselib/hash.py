import hashlib

class HashUtils:
    async def create_hash(self, text) -> str:
        text = str(text)
        text += "3886go@fcbE7QukKNxXNWNkxfndsZUxLh9sZjNg82VDWCN_2.se39g4JN*hmieJBg8kkovY_EeyKTi3DDJhaLmJA*pQsQxFP9CynwA3a"
        text_bytes = text.encode("utf-8")
        return hashlib.sha256(text_bytes).hexdigest()

    async def verify_hash(self, original, hash) -> bool:
        generated = await self.create_hash(original)
        return generated == hash
