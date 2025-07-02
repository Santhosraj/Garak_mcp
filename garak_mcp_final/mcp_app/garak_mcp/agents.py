"""
AI Research Agent Classes
Enhanced agent implementation for MCP server
"""

import logging
from typing import List, Tuple, Callable, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MCPAgent:
    """
    Enhanced MCP Agent with conversation history, safety checks, and better error handling
    """
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.history: List[Tuple[str, str]] = []
        self.created_at = datetime.now()
        self.total_interactions = 0
        
    def think(self, prompt: str, model_fn: Callable[[str], str]) -> str:
        """
        Process a user prompt and generate a response using the provided model function
        
        Args:
            prompt: User input prompt
            model_fn: Function to call the AI model
            
        Returns:
            Generated response from the model
        """
        if not prompt or not prompt.strip():
            return "I need a question or prompt to respond to."
        
        # Safety check for harmful content
        if self._is_potentially_harmful(prompt):
            logger.warning(f"Potentially harmful prompt detected: {prompt[:50]}...")
            return ("I can't provide information on that topic. I'm designed to be helpful, "
                   "harmless, and honest. Is there something else I can help you with?")
        
        try:
            # Add to history
            self.history.append(("user", prompt))
            
            # Create full prompt with role context
            full_prompt = self._build_full_prompt(prompt)
            
            # Get response from model
            logger.info(f"Sending prompt to model: {full_prompt[:100]}...")
            response = model_fn(full_prompt)
            
            # Clean and validate response
            if not response or response.strip() == "":
                response = "I apologize, but I wasn't able to generate a proper response. Could you try rephrasing your question?"
            
            # Add response to history
            self.history.append(("agent", response))
            self.total_interactions += 1
            
            logger.info(f"Generated response: {response[:100]}...")
            return response
            
        except Exception as e:
            error_msg = f"I encountered an error while processing your request: {str(e)}"
            logger.error(f"Error in think method: {e}")
            self.history.append(("agent", error_msg))
            return error_msg
    
    def _build_full_prompt(self, user_prompt: str) -> str:
        """Build the complete prompt including role and context"""
        context = ""
        
        # Add recent conversation history for context (last 3 exchanges)
        if len(self.history) > 0:
            recent_history = self.history[-6:]  # Last 3 user-agent pairs
            context = "\n\nRecent conversation:\n"
            for role, content in recent_history:
                context += f"{role.capitalize()}: {content}\n"
        
        full_prompt = f"{self.role}{context}\n\nCurrent question: {user_prompt}"
        return full_prompt
    
    def _is_potentially_harmful(self, prompt: str) -> bool:
        """
        Basic safety check for potentially harmful prompts
        This is a simple implementation - in production, use more sophisticated safety systems
        """
        harmful_keywords = [
            "make meth", "make drugs", "make explosives", "make bomb",
            "how to kill", "how to hurt", "suicide methods", "self harm",
            "illegal activities", "hack into", "steal", "fraud"
        ]
        
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in harmful_keywords)
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.history:
            return "No conversation history yet."
        
        summary = f"Agent: {self.name}\n"
        summary += f"Role: {self.role}\n"
        summary += f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += f"Total interactions: {self.total_interactions}\n"
        summary += f"History entries: {len(self.history)}\n"
        
        if self.history:
            summary += f"Last interaction: {self.history[-1][1][:100]}..."
        
        return summary
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.history = []
        logger.info(f"Cleared history for agent {self.name}")
    
    def update_role(self, new_role: str) -> None:
        """Update the agent's role/system prompt"""
        old_role = self.role
        self.role = new_role
        logger.info(f"Updated role for agent {self.name} from '{old_role}' to '{new_role}'")
    
    def export_history(self) -> List[dict]:
        """Export conversation history in a structured format"""
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "role": role,
                "content": content,
                "agent_name": self.name
            }
            for role, content in self.history
        ]

class SpecializedAgent(MCPAgent):
    """
    Specialized agent with domain-specific capabilities
    """
    
    def __init__(self, name: str, role: str, specialization: str):
        super().__init__(name, role)
        self.specialization = specialization
        self.specialized_keywords = []
    
    def think(self, prompt: str, model_fn: Callable[[str], str]) -> str:
        """Enhanced think method with specialization context"""
        # Add specialization context to the role
        enhanced_role = f"{self.role}\n\nSpecialization: {self.specialization}"
        original_role = self.role
        self.role = enhanced_role
        
        try:
            response = super().think(prompt, model_fn)
            return response
        finally:
            # Restore original role
            self.role = original_role

def create_research_agent() -> MCPAgent:
    """Factory function to create a research agent with default settings"""
    return MCPAgent(
        name="Research Assistant",
        role="You are a helpful, accurate, and ethical research assistant. "
             "You provide well-researched, factual information while being safe and responsible. "
             "You cite sources when possible and acknowledge when you're uncertain about information."
    )

def create_coding_agent() -> SpecializedAgent:
    """Factory function to create a coding-specialized agent"""
    return SpecializedAgent(
        name="Code Assistant", 
        role="You are an expert programming assistant. You write clean, efficient, "
             "and well-documented code. You explain complex concepts clearly and "
             "follow best practices for software development.",
        specialization="Software Development and Programming"
    )