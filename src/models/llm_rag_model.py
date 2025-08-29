import openai
from typing import Dict, Tuple, Any, List
import json
import os


class LLMRAGModel:
    """
    General-Purpose LLM with RAG for Compliance Detection
    GPT-4/Claude with regulatory database retrieval
    Strength: Handles novel or edge-case scenarios
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.regulatory_database = self._initialize_regulatory_database()
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def _initialize_regulatory_database(self) -> Dict[str, Any]:
        """Initialize a basic regulatory database for RAG"""
        return {
            "general_compliance": {
                "description": "General compliance principles and standards",
                "keywords": ["compliance", "regulation", "standard", "requirement"],
                "examples": [
                    "Organizations must comply with applicable laws and regulations",
                    "Regular audits ensure ongoing compliance",
                    "Documentation must be maintained for compliance purposes"
                ]
            },
            "data_protection": {
                "description": "Data protection and privacy regulations",
                "keywords": ["privacy", "data protection", "GDPR", "personal data"],
                "examples": [
                    "Personal data must be processed lawfully and transparently",
                    "Data subjects have rights to access and control their data",
                    "Data breaches must be reported within 72 hours"
                ]
            },
            "financial_regulations": {
                "description": "Financial and banking regulations",
                "keywords": ["financial", "banking", "SEC", "audit", "reporting"],
                "examples": [
                    "Financial institutions must maintain adequate capital reserves",
                    "Regular financial reporting is required for compliance",
                    "Anti-money laundering procedures must be implemented"
                ]
            },
            "environmental_compliance": {
                "description": "Environmental and safety regulations",
                "keywords": ["environmental", "safety", "EPA", "hazardous", "waste"],
                "examples": [
                    "Environmental impact assessments are required for new projects",
                    "Hazardous waste must be properly disposed of",
                    "Safety protocols must be followed in all operations"
                ]
            }
        }
    
    def _retrieve_relevant_context(self, text: str) -> List[str]:
        """Retrieve relevant regulatory context for the input text"""
        relevant_contexts = []
        text_lower = text.lower()
        
        for category, info in self.regulatory_database.items():
            # Check if any keywords match
            if any(keyword in text_lower for keyword in info["keywords"]):
                relevant_contexts.extend(info["examples"])
        
        # If no specific context found, return general compliance principles
        if not relevant_contexts:
            relevant_contexts = [
                "Compliance requires adherence to applicable laws and regulations",
                "Organizations must establish and maintain compliance programs",
                "Regular monitoring and assessment is essential for ongoing compliance"
            ]
        
        return relevant_contexts[:3]  # Limit to top 3 most relevant
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict compliance status using LLM with RAG
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (decision, confidence_score)
        """
        if not self.api_key:
            return self._fallback_prediction(text)
        
        try:
            # Retrieve relevant regulatory context
            relevant_context = self._retrieve_relevant_context(text)
            
            # Construct prompt with context
            prompt = self._construct_prompt(text, relevant_context)
            
            # Get LLM response
            response = self._call_llm(prompt)
            
            # Parse response
            decision, confidence = self._parse_llm_response(response)
            
            return decision, confidence
            
        except Exception as e:
            print(f"Error in LLM RAG prediction: {e}")
            return self._fallback_prediction(text)
    
    def _construct_prompt(self, text: str, context: List[str]) -> str:
        """Construct the prompt for the LLM with regulatory context"""
        context_str = "\n".join([f"- {ctx}" for ctx in context])
        
        prompt = f"""You are a compliance expert analyzing legal and regulatory text. 

Relevant regulatory context:
{context_str}

Text to analyze:
"{text}"

Based on the regulatory context and the text above, determine if this text indicates:
1. COMPLIANT - The text suggests compliance with regulations
2. NON-COMPLIANT - The text suggests non-compliance or violations
3. UNCLEAR - The compliance status is ambiguous or unclear

Provide your response in this exact JSON format:
{{
    "decision": "COMPLIANT|NON-COMPLIANT|UNCLEAR",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of your decision"
}}

Response:"""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM API"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a compliance expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM API call failed: {e}")
            raise
    
    def _parse_llm_response(self, response: str) -> Tuple[str, float]:
        """Parse the LLM response to extract decision and confidence"""
        try:
            # Clean the response and parse JSON
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            
            parsed = json.loads(response_clean)
            
            decision = parsed.get("decision", "UNCLEAR")
            confidence = float(parsed.get("confidence", 0.5))
            
            # Normalize decision format
            if decision.upper() == "COMPLIANT":
                decision = "Compliant"
            elif decision.upper() == "NON-COMPLIANT":
                decision = "Non-Compliant"
            else:
                decision = "Unclear"
            
            return decision, confidence
            
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return "Unclear", 0.50
    
    def _fallback_prediction(self, text: str) -> Tuple[str, float]:
        """Fallback prediction when LLM is not available"""
        # Simple keyword-based fallback similar to rules-based classifier
        text_lower = text.lower()
        
        compliant_indicators = ['compliant', 'compliance', 'legal', 'approved', 'permitted']
        non_compliant_indicators = ['non-compliant', 'illegal', 'prohibited', 'violation', 'breach']
        
        compliant_score = sum(1 for word in compliant_indicators if word in text_lower)
        non_compliant_score = sum(1 for word in non_compliant_indicators if word in text_lower)
        
        if compliant_score > non_compliant_score:
            return "Compliant", 0.70
        elif non_compliant_score > compliant_score:
            return "Non-Compliant", 0.70
        else:
            return "Unclear", 0.60
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and status"""
        return {
            "model_type": "General-Purpose LLM with RAG",
            "model": self.model,
            "status": "active" if self.api_key else "fallback",
            "rag_database_size": len(self.regulatory_database),
            "strength": "Handles novel or edge-case scenarios"
        }
    
    def explain_decision(self, text: str) -> Dict[str, Any]:
        """Explain the decision-making process for transparency"""
        relevant_context = self._retrieve_relevant_context(text)
        
        return {
            "retrieved_context": relevant_context,
            "context_categories": list(self.regulatory_database.keys()),
            "reasoning": f"Retrieved {len(relevant_context)} relevant regulatory contexts"
        }
