"""
Generator module for PathPilot RAG System.
Handles LLM generation with OpenAI.
"""
import logging
import time
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from config import config
from utils.json_parser import try_parse_json

logger = logging.getLogger(__name__)


class Generator:
    """Manages LLM generation with OpenAI."""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.GENERATION_MODEL
        self.max_retries = 3
        self.retry_delay = 1.5
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 1500, 
        temperature: float = 0.2,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Generate text from OpenAI with retry logic.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            response_format: Optional response format (e.g., {"type": "json_object"})
            
        Returns:
            Generated text
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                params = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
                
                if response_format:
                    params["response_format"] = response_format
                
                response = self.client.chat.completions.create(**params)
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.warning(f"Generation attempt {attempt}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay ** attempt)
                else:
                    raise
    
    def generate_json(
        self, 
        prompt: str, 
        max_tokens: int = 1500, 
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens
            temperature: Sampling temperature
            
        Returns:
            Parsed JSON object
        """
        # Try with JSON mode first
        try:
            response_text = self.generate(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
            
            parsed = try_parse_json(response_text)
            if parsed:
                return parsed
        except Exception as e:
            logger.warning(f"JSON mode generation failed: {e}")
        
        # Fallback: try without JSON mode
        try:
            response_text = self.generate(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            parsed = try_parse_json(response_text)
            if parsed:
                return parsed
            else:
                raise ValueError("Failed to parse JSON from response")
        except Exception as e:
            logger.error(f"JSON generation failed completely: {e}")
            raise
    
    def generate_career_recommendation(self, profile: str, context: str) -> Dict[str, Any]:
        """
        Generate career recommendations.
        
        Args:
            profile: User profile text
            context: Retrieved career context
            
        Returns:
            Structured career recommendations
        """
        from utils.prompt_templates import CAREER_RECOMMENDATION_PROMPT
        
        prompt = CAREER_RECOMMENDATION_PROMPT.format(
            profile=profile,
            retrieved_context=context
        )
        
        return self.generate_json(prompt, max_tokens=2000, temperature=0.2)
    
    def generate_career_roadmap(
        self, 
        role: str, 
        current_skills: str, 
        experience_level: str,
        context: str
    ) -> Dict[str, Any]:
        """
        Generate personalized career roadmap.
        
        Args:
            role: Target role
            current_skills: User's current skills
            experience_level: Beginner/Intermediate/Advanced
            context: Retrieved context
            
        Returns:
            Structured roadmap
        """
        from utils.prompt_templates import CAREER_ROADMAP_PROMPT
        
        prompt = CAREER_ROADMAP_PROMPT.format(
            role=role,
            current_skills=current_skills,
            experience_level=experience_level,
            retrieved_context=context
        )
        
        return self.generate_json(prompt, max_tokens=2000, temperature=0.2)
    
    def generate_startup_guidance(self, project_details: str, context: str) -> Dict[str, Any]:
        """
        Generate startup guidance.
        
        Args:
            project_details: Project information
            context: Retrieved startup context
            
        Returns:
            Structured startup guidance
        """
        from utils.prompt_templates import STARTUP_GUIDANCE_PROMPT
        
        prompt = STARTUP_GUIDANCE_PROMPT.format(
            project_details=project_details,
            retrieved_context=context
        )
        
        return self.generate_json(prompt, max_tokens=2000, temperature=0.3)
    
    def generate_financial_analysis(self, query: str, context: str) -> Dict[str, Any]:
        """
        Generate financial analysis.
        
        Args:
            query: User query
            context: Retrieved financial context
            
        Returns:
            Structured financial analysis
        """
        from utils.prompt_templates import FINANCIAL_ANALYSIS_PROMPT
        
        prompt = FINANCIAL_ANALYSIS_PROMPT.format(
            query=query,
            retrieved_context=context
        )
        
        return self.generate_json(prompt, max_tokens=1500, temperature=0.2)
    
    def generate_evaluation(
        self, 
        query: str, 
        context: str, 
        response: str
    ) -> Dict[str, Any]:
        """
        Evaluate a RAG response.
        
        Args:
            query: Original query
            context: Retrieved context
            response: Generated response
            
        Returns:
            Evaluation scores and feedback
        """
        from utils.prompt_templates import EVALUATION_PROMPT
        
        prompt = EVALUATION_PROMPT.format(
            query=query,
            retrieved_context=context,
            response=response
        )
        
        return self.generate_json(prompt, max_tokens=800, temperature=0.1)
