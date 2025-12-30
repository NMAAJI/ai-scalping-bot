"""
AI Analysis Module
Integrates with Google Gemini API for trading decisions
"""

import json
import logging
from typing import Dict, Optional
from google import genai
from config.settings import AI_MODEL, AI_MAX_RETRIES, AI_TIMEOUT, TRADING_CONFIG

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    """Handles AI analysis using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini analyzer
        
        Args:
            api_key: Google Gemini API key
        """
        self.client = genai.Client(api_key=api_key)
        self.model = AI_MODEL
        self.max_retries = AI_MAX_RETRIES
        self.timeout = AI_TIMEOUT
    
    def analyze_market(self, market_data: Dict) -> Dict:
        """
        Analyze market data using Gemini AI and generate trading decision
        
        Args:
            market_data: Dictionary containing market data and indicators
        
        Returns:
            Dictionary with trading action, confidence, and price levels
        """
        try:
            prompt = self._build_analysis_prompt(market_data)
            
            for attempt in range(self.max_retries):
                try:
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt
                    )
                    
                    ai_decision = self._parse_response(response.text)
                    
                    logger.info(
                        f"🤖 AI Decision: {ai_decision['action']} "
                        f"(Confidence: {ai_decision['confidence']:.2%})"
                    )
                    
                    return ai_decision
                    
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                        continue
                    raise
            
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            return self._fallback_decision()
    
    @staticmethod
    def _build_analysis_prompt(market_data: Dict) -> str:
        """Build analysis prompt for Gemini AI"""
        return f"""
You are an expert cryptocurrency scalping trader. Analyze this market data and make a trading decision.

MARKET DATA:
- Symbol: {TRADING_CONFIG['symbol']}
- Current Price: ${market_data['price']:.2f}
- RSI: {market_data['rsi']:.2f}
- Fast EMA (9): ${market_data['ema_fast']:.2f}
- Slow EMA (21): ${market_data['ema_slow']:.2f}
- ATR: ${market_data['atr']:.2f}
- Current Volume: {market_data['volume']:.0f}
- Average Volume: {market_data['avg_volume']:.0f}
- Volume Ratio: {market_data['volume_ratio']:.2f}x
- Trend: {market_data['trend']}

TRADING RULES:
1. BUY when: Fast EMA crosses above Slow EMA, RSI < {TRADING_CONFIG['rsi_overbought']}, volume > average, bullish trend
2. SELL when: Fast EMA crosses below Slow EMA, RSI > {TRADING_CONFIG['rsi_oversold']}, volume > average, bearish trend
3. HOLD when: No clear signal or mixed indicators
4. Risk-reward ratio minimum 1:2
5. Use ATR for stop loss and take profit calculation

Respond in EXACT JSON format (no markdown):
{{
    "action": "BUY" or "SELL" or "HOLD",
    "confidence": 0.0 to 1.0,
    "entry_price": {market_data['price']},
    "stop_loss": price level,
    "take_profit": price level,
    "reasoning": "brief explanation"
}}
"""
    
    @staticmethod
    def _parse_response(response_text: str) -> Dict:
        """Parse and validate AI response"""
        try:
            # Clean JSON from markdown
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            ai_decision = json.loads(response_text)
            
            # Validate response
            required_keys = ['action', 'confidence', 'entry_price', 'stop_loss', 'take_profit', 'reasoning']
            if not all(key in ai_decision for key in required_keys):
                raise ValueError("Missing required keys in AI response")
            
            return ai_decision
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            raise
    
    @staticmethod
    def _fallback_decision() -> Dict:
        """Return fallback decision when AI fails"""
        return {
            'action': 'HOLD',
            'confidence': 0.0,
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'reasoning': 'AI analysis failed, defaulting to HOLD'
        }
