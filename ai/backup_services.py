"""
Backup AI Services
Support for OpenAI, Anthropic, and other APIs
Automatic fallback when primary service fails
"""

import json
import logging
import requests
from typing import Dict, Optional
from datetime import datetime
from config.settings import TRADING_CONFIG

logger = logging.getLogger(__name__)


class BackupAIService:
    """Multi-service AI backup system"""
    
    def __init__(self):
        """Initialize backup services"""
        self.services = {}
        self.priority_order = []
        self.last_used = None
        
    def add_service(self, name: str, api_key: str, service_type: str, priority: int = 1) -> None:
        """
        Add a backup service
        
        Args:
            name: Service name (e.g., 'openai', 'anthropic')
            api_key: API key for the service
            service_type: Type of service
            priority: Priority (lower number = higher priority)
        """
        self.services[name] = {
            'api_key': api_key,
            'type': service_type,
            'priority': priority,
            'status': 'active',
            'last_used': None,
            'success_count': 0,
            'error_count': 0
        }
        
        # Sort by priority
        self.priority_order = sorted(
            self.services.keys(),
            key=lambda x: self.services[x]['priority']
        )
        
        logger.info(f"✅ Backup service added: {name} (Priority: {priority})")
    
    def get_analysis(self, market_data: Dict, max_attempts: int = 3) -> Optional[Dict]:
        """
        Try all services in priority order until one succeeds
        
        Args:
            market_data: Market data to analyze
            max_attempts: Max services to try
        
        Returns:
            Analysis decision or None if all fail
        """
        attempts = 0
        
        for service_name in self.priority_order:
            if attempts >= max_attempts:
                break
            
            service = self.services[service_name]
            
            if service['status'] != 'active':
                logger.warning(f"⏭️ Skipping inactive service: {service_name}")
                continue
            
            try:
                logger.info(f"🔄 Trying backup service: {service_name}")
                
                if service['type'] == 'openai':
                    result = self._analyze_with_openai(
                        market_data,
                        service['api_key']
                    )
                elif service['type'] == 'anthropic':
                    result = self._analyze_with_anthropic(
                        market_data,
                        service['api_key']
                    )
                elif service['type'] == 'together':
                    result = self._analyze_with_together(
                        market_data,
                        service['api_key']
                    )
                else:
                    logger.warning(f"Unknown service type: {service['type']}")
                    continue
                
                if result:
                    service['last_used'] = datetime.now().isoformat()
                    service['success_count'] += 1
                    self.last_used = service_name
                    
                    logger.info(f"✅ {service_name} succeeded!")
                    return result
                
            except Exception as e:
                service['error_count'] += 1
                logger.warning(f"❌ {service_name} failed: {e}")
                attempts += 1
                continue
        
        logger.error("❌ All backup services exhausted")
        return None
    
    def _analyze_with_openai(self, market_data: Dict, api_key: str) -> Optional[Dict]:
        """
        Analyze using OpenAI GPT-4
        https://platform.openai.com/docs/api-reference
        """
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            prompt = self._build_analysis_prompt(market_data)
            
            response = client.chat.completions.create(
                model="gpt-4-turbo",  # Or "gpt-3.5-turbo" for faster/cheaper
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert cryptocurrency trading AI. Provide analysis in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temp = more focused
                max_tokens=1000,
                timeout=10
            )
            
            result = self._parse_response(response.choices[0].message.content)
            result['source'] = 'openai'
            
            return result
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return None
    
    def _analyze_with_anthropic(self, market_data: Dict, api_key: str) -> Optional[Dict]:
        """
        Analyze using Anthropic Claude
        https://docs.anthropic.com/
        """
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            prompt = self._build_analysis_prompt(market_data)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",  # Fast and capable
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            result = self._parse_response(message.content[0].text)
            result['source'] = 'anthropic'
            
            return result
            
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            return None
    
    def _analyze_with_together(self, market_data: Dict, api_key: str) -> Optional[Dict]:
        """
        Analyze using Together AI
        https://docs.together.ai/
        """
        try:
            import together
            client = together.Together(api_key=api_key)
            
            prompt = self._build_analysis_prompt(market_data)
            
            response = client.complete(
                prompt=prompt,
                model="meta-llama/Llama-2-70b-chat-hf",
                max_tokens=1024,
                temperature=0.3
            )
            
            result = self._parse_response(response.output.text)
            result['source'] = 'together'
            
            return result
            
        except Exception as e:
            logger.error(f"Together AI error: {e}")
            return None
    
    def _build_analysis_prompt(self, market_data: Dict) -> str:
        """Build analysis prompt for any AI service"""
        return f"""
Analyze this cryptocurrency market data and provide a trading decision.

MARKET DATA:
- Price: ${market_data['price']:.2f}
- RSI(14): {market_data['rsi']:.2f}
- EMA(9): ${market_data.get('ema_fast', 0):.2f}
- EMA(21): ${market_data.get('ema_slow', 0):.2f}
- Volume Ratio: {market_data.get('volume_ratio', 1):.2f}x
- Trend: {market_data['trend']}

DECISION RULES:
- BUY: EMA9 > EMA21, RSI < 70, volume up
- SELL: EMA9 < EMA21, RSI > 30, volume up
- HOLD: No clear setup

Respond ONLY with valid JSON (no markdown):
{{
    "action": "BUY" or "SELL" or "HOLD",
    "confidence": 0.0 to 1.0,
    "entry_price": {market_data['price']},
    "stop_loss": {market_data['price'] - market_data.get('atr', 1)},
    "take_profit": {market_data['price'] + market_data.get('atr', 1) * 2},
    "reasoning": "Brief explanation"
}}
"""
    
    def _parse_response(self, response_text: str) -> Optional[Dict]:
        """Parse response from any service"""
        try:
            # Clean markdown
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Remove any leading/trailing text
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                response_text = response_text[start_idx:end_idx]
            
            result = json.loads(response_text)
            
            # Validate
            required = ['action', 'confidence', 'entry_price', 'stop_loss', 'take_profit', 'reasoning']
            if not all(k in result for k in required):
                return None
            
            return result
            
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return None
    
    def get_status(self) -> Dict:
        """Get status of all backup services"""
        status = {}
        
        for name, service in self.services.items():
            status[name] = {
                'status': service['status'],
                'priority': service['priority'],
                'last_used': service['last_used'],
                'success_count': service['success_count'],
                'error_count': service['error_count'],
                'success_rate': (
                    service['success_count'] / (service['success_count'] + service['error_count'])
                    if (service['success_count'] + service['error_count']) > 0
                    else 0
                )
            }
        
        return status
    
    def disable_service(self, name: str) -> None:
        """Disable a service after too many failures"""
        if name in self.services:
            self.services[name]['status'] = 'disabled'
            logger.warning(f"🔴 Service disabled: {name}")
    
    def enable_service(self, name: str) -> None:
        """Re-enable a disabled service"""
        if name in self.services:
            self.services[name]['status'] = 'active'
            self.services[name]['error_count'] = 0
            logger.info(f"🟢 Service re-enabled: {name}")
