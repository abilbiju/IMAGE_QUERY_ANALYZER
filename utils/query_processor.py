from flask import jsonify
from openai import OpenAI
import os
import json
import base64
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

def direct_image_query(image_path, query):
    """
    Send the image and query directly to OpenAI for processing
    """
    # Read the image file and encode it as base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Call OpenAI API for answering the query
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please answer this question about the image as accurately as possible: {query}"
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
        max_tokens=1000
    )
    
    # Return the response content
    return response.choices[0].message.content

class QueryProcessor:
    def __init__(self, analysis_results):
        # Make sure we have a proper dictionary for analysis_results
        if isinstance(analysis_results, str):
            try:
                self.analysis_results = json.loads(analysis_results)
            except json.JSONDecodeError:
                self.analysis_results = {"raw_analysis": analysis_results}
        else:
            self.analysis_results = analysis_results

    def get_object_details(self, query):
        """Get details about objects matching the query"""
        response = {}
        for obj in self.analysis_results.get('objects', []):
            if obj.get('name') and query.lower() in obj.get('name', '').lower():
                response[obj['name']] = obj
        return response

    def get_entity_details(self, query):
        """Get details about entities matching the query"""
        response = {}
        for entity in self.analysis_results.get('entities', []):
            if entity.get('name') and query.lower() in entity.get('name', '').lower():
                response[entity['name']] = entity
        return response
    
    def get_count(self, query):
        """Get count of specific objects"""
        count_terms = []
        
        if any(term in query.lower() for term in count_terms):
            # Look for specific object mentions in the query
            target_object = None
            for obj_type in ["person", "people", "car", "dog", "cat", "chair", "table", "bike", "bicycle"]:
                if obj_type in query.lower():
                    target_object = obj_type
                    break
            
            # If "person" or "people" is mentioned, count people
            if target_object == "people":
                target_object = "person"
                
            # Count objects
            if target_object:
                # Look for objects in the analysis results
                for obj in self.analysis_results.get('objects', []):
                    if obj.get('name') and target_object.lower() in obj.get('name', '').lower():
                        count = obj.get('count', 1)
                        return {
                            "count": count,
                            "object": obj.get('name')
                        }
            
            # Count all objects 
            objects = self.analysis_results.get('objects', [])
            total_objects = sum(obj.get('count', 1) for obj in objects)
            total_entities = len(self.analysis_results.get('entities', []))
            
            return {
                "total_objects": total_objects,
                "total_entities": total_entities
            }
        return {}
    
    def get_structured_response(self, query):
        """Get a structured response based on the query"""
        # Check various types of queries
        object_response = self.get_object_details(query)
        entity_response = self.get_entity_details(query)
        count_response = self.get_count(query)
        
        # Combine all non-empty responses
        combined_response = {}
        for response in [object_response, entity_response, count_response]:
            if response:
                combined_response.update(response)
        
        return combined_response
    
    def process_query(self, query):
        """Process a query and return a Flask response"""
        structured_response = self.get_structured_response(query)
        
        if structured_response:
            return jsonify(structured_response)
        else:
            # For direct image queries, we'll handle this in the main app route
            return jsonify({"message": "No relevant information found for your query."})