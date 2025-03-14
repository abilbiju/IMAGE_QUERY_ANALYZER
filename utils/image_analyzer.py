import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def analyze_image(image_path):
    """
    Analyze image using OpenAI's GPT-4 Vision capabilities
    """
    # Read the image file and encode it as base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    prompt = """Analyze this image in detail. 
    
    Please identify all objects, people, scenes, activities, colors, and other notable elements. 
    Provide a comprehensive analysis, including:
    1. All individual objects and their locations, colors, and approximate sizes
    2. All people/entities and what they appear to be doing
    3. Count of similar objects (e.g., "3 chairs")
    4. Spatial relationships between objects
    5. Overall scene description and context
    6. Any visible text and its content
    7. Prominent colors in the scene
    
    Format your response as JSON with the following structure:
    {
      "objects": [
        {
          "name": "object_name",
          "count": number,
          "description": "detailed description",
          "position": "location in image",
          "features": {
            "color": "color",
            "size": "size estimation"
          }
        }
      ],
      "scene": "overall scene description",
      "activities": ["activity1", "activity2"],
      "entities": [
        {
          "name": "entity_name",
          "type": "person/animal/etc",
          "description": "detailed description",
          "action": "what the entity is doing"
        }
      ],
      "text_content": ["any text found in image"],
      "colors": ["prominent colors in the scene"],
      "spatial_relationships": ["object A is to the left of object B", "object C is on top of object D"]
    }

    Make sure your output is properly formatted JSON.
    """
    
    # Call OpenAI API for image analysis using GPT-4 Vision
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Try to parse the JSON response
        try:
            result = json.loads(content)
            print("Successfully parsed JSON response")
            return result
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {str(e)}")
            # If it's not valid JSON, extract structured data using a more lenient approach
            # We'll return the raw text with a flag indicating it's not properly structured
            return {
                "raw_analysis": content,
                "objects": [],
                "entities": [],
                "scene": "Analysis couldn't be properly structured"
            }
            
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return {"error": str(e), "message": "Failed to analyze image"}