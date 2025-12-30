from google import genai
from google.genai import types
import json
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedMultiTimeframeAI:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the Multi-Timeframe AI Analyst.
        
        Args:
            api_key: Google GenAI API Key.
            model_name: The model version to use (default: gemini-2.0-flash-exp).
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.required_timeframes = ['1m', '5m', '15m', '1h']
        self.required_metrics = ['price', 'rsi', 'ema_fast', 'ema_slow', 'trend']

    def analyze_market_advanced(self, market_data_multi: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze multiple timeframes simultaneously to generate a trading decision.
        
        Args:
            market_data_multi: Dictionary containing data for '1m', '5m', '15m', '1h'.
                               Each timeframe dict must contain: price, rsi, ema_fast, 
                               ema_slow, volume_ratio, trend.
        
        Returns:
            Dict containing action, confidence, entry/exit targets, and reasoning.
        """
        
        # 1. Validate Input Data
        if not all(tf in market_data_multi for tf in self.required_timeframes):
            missing = [tf for tf in self.required_timeframes if tf not in market_data_multi]
            return self._generate_error_response(f"Missing timeframes: {missing}")
            
        # 1.1 Validate Inner Metrics
        for tf in self.required_timeframes:
            missing_metrics = [k for k in self.required_metrics if k not in market_data_multi[tf]]
            if missing_metrics:
                return self._generate_error_response(f"Missing metrics in {tf}: {missing_metrics}")

        # 2. Construct the Prompt
        # Note: We pass the raw values. The LLM does the logic.
        try:
            prompt = f"""
            Act as an expert algorithmic trader specializing in Multi-Timeframe Analysis (MTA).
            Analyze the following Bitcoin (BTC/USDT) market data to generate a high-probability trade setup.
            
            Do not hallucinate data. Use only the provided metrics below.

            INPUT DATA:
            
            [1-MINUTE TIMEFRAME - ENTRY TRIGGER]
            Price: ${market_data_multi['1m']['price']:,.2f}
            RSI (14): {market_data_multi['1m']['rsi']:.1f}
            EMA Fast: ${market_data_multi['1m']['ema_fast']:,.2f}
            EMA Slow: ${market_data_multi['1m']['ema_slow']:,.2f}
            Volume Ratio: {market_data_multi['1m'].get('volume_ratio', 1.0):.2f}x
            Trend Status: {market_data_multi['1m']['trend']}

            [5-MINUTE TIMEFRAME - SHORT-TERM TREND]
            RSI (14): {market_data_multi['5m']['rsi']:.1f}
            Trend Status: {market_data_multi['5m']['trend']}
            EMA Spread: {market_data_multi['5m']['ema_fast'] - market_data_multi['5m']['ema_slow']:.2f}

            [15-MINUTE TIMEFRAME - MOMENTUM]
            RSI (14): {market_data_multi['15m']['rsi']:.1f}
            Trend Status: {market_data_multi['15m']['trend']}
            Price vs EMA Slow: {"Above" if market_data_multi['15m']['price'] > market_data_multi['15m']['ema_slow'] else "Below"}

            [1-HOUR TIMEFRAME - MACRO BIAS]
            RSI (14): {market_data_multi['1h']['rsi']:.1f}
            Trend Status: {market_data_multi['1h']['trend']}
            
            STRATEGY RULES:
            1. CONFLUENCE: A trade requires alignment of at least 3 timeframes.
            2. ENTRY: 1m timeframe dictates the exact entry price.
            3. STOP LOSS: Place tight stops based on 1m/5m EMA structure.
            4. RISK: If 1h trend opposes 1m trend, reduce confidence significantly.
            
            OUTPUT REQUIREMENT:
            Return a JSON object with the specific schema requested.
            """
        except (ValueError, TypeError) as e:
            return self._generate_error_response(f"Data formatting error: {str(e)}")

        try:
            # 3. Call Gemini with JSON Mode
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,  # Low temperature for deterministic, analytical output
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "action": {"type": "STRING", "enum": ["BUY", "SELL", "HOLD"]},
                            "confidence": {"type": "NUMBER"},
                            "entry_price": {"type": "NUMBER"},
                            "stop_loss": {"type": "NUMBER"},
                            "take_profit": {"type": "NUMBER"},
                            "timeframe_alignment": {
                                "type": "OBJECT",
                                "properties": {
                                    "1m": {"type": "STRING"},
                                    "5m": {"type": "STRING"},
                                    "15m": {"type": "STRING"},
                                    "1h": {"type": "STRING"}
                                }
                            },
                            "aligned_timeframes": {"type": "INTEGER"},
                            "primary_reason": {"type": "STRING"},
                            "risk_level": {"type": "STRING", "enum": ["LOW", "MEDIUM", "HIGH"]}
                        },
                        "required": ["action", "confidence", "aligned_timeframes", "primary_reason"]
                    }
                )
            )
            
            # 4. Parse Response
            # With JSON mode, response.text is guaranteed to be JSON (or empty on error)
            decision = json.loads(response.text)
            
            # 5. Logic Validation
            if decision['confidence'] > 1.0:
                decision['confidence'] /= 100.0  # Handle cases where LLM outputs 95 instead of 0.95
            
            return decision

        except Exception as e:
            logger.error(f"AI Analysis Failed: {e}")
            return self._generate_error_response(str(e))

    def _generate_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Returns a safe default dictionary to prevent downstream crashes."""
        return {
            "action": "HOLD",
            "confidence": 0.0,
            "entry_price": 0.0,
            "stop_loss": 0.0,
            "take_profit": 0.0,
            "timeframe_alignment": {
                "1m": "NEUTRAL", "5m": "NEUTRAL", "15m": "NEUTRAL", "1h": "NEUTRAL"
            },
            "aligned_timeframes": 0,
            "primary_reason": f"System Error: {error_msg}",
            "risk_level": "HIGH"
        }
