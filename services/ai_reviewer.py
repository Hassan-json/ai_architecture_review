import base64
import os
from openai import OpenAI
from config import Config

class ArchitectureReviewer:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def encode_image(self, image_path):
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def review_architecture(self, image_path):
        """
        Send architecture diagram to OpenAI GPT-4 Vision for review

        Args:
            image_path (str): Path to the architecture diagram image

        Returns:
            dict: Review results with identified issues and recommendations
        """
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)

            # Get file extension to determine MIME type
            ext = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')

            # Create the prompt for architecture review
            prompt = """You are an expert software architect. Analyze this software architecture diagram and provide a comprehensive review.

Return your analysis as a JSON object with this exact structure:

{
  "issues": [
    {
      "title": "Name of the issue",
      "problem": "What's wrong",
      "impact": "Why it matters",
      "mitigation": ["Step 1", "Step 2", "Step 3"]
    }
  ],
  "security": [
    {
      "concern": "Security issue",
      "risk": "What could go wrong",
      "mitigation": ["Solution 1", "Solution 2"]
    }
  ],
  "scalability": [
    {
      "issue": "Scalability problem",
      "impact": "What happens as system grows",
      "mitigation": ["Architectural change 1", "Architectural change 2"]
    }
  ],
  "bestPractices": [
    {
      "practice": "What's missing",
      "whyImportant": "Benefits of this practice",
      "implementation": ["How to implement step 1", "How to implement step 2"]
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "title": "Most important change",
      "description": "Why this is priority 1",
      "steps": ["Implementation step 1", "Implementation step 2"]
    }
  ]
}

Be specific and actionable in all mitigation strategies. Each mitigation should be an array of concrete steps."""

            # Call OpenAI API with JSON mode
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=4000
            )

            # Extract and parse the JSON review
            review_json = response.choices[0].message.content
            import json
            review_data = json.loads(review_json)

            return {
                "success": True,
                "review": review_data,
                "model": Config.OPENAI_MODEL
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "review": None
            }
