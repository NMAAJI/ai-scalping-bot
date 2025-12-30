"""
Advanced Multi-Timeframe AI Analysis
Analyzes 1m, 5m, 15m, and 1h timeframes together for better decisions
"""

import json
import logging
from typing import Dict, List, Optional
from google import genai

logger = logging.getLogger(__name__)


class AdvancedMultiTimeframeAI:
    """Multi-timeframe analysis using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """Initialize with Gemini API key"""
        self.client = genai.Client(api_key=api_key)
        self.timeframes = ['1m', '5m', '15m', '1h']
        self.model = 'gemini-2.0-flash-exp'
    
    def analyze_market_advanced(self, market_data_multi: Dict) -> Dict:
        """
        Analyze multiple timeframes at once
        
        Args:
            market_data_multi: Dictionary with timeframe data
                {
                    '1m': {price, rsi, ema_fast, ema_slow, volume_ratio, trend},
                    '5m': {...},
                    '15m': {...},
                    '1h': {...}
                }
        
        Returns:
            Decision dictionary with action, confidence, and analysis
        """
        
        try:
            # Validate input data
            for tf in self.timeframes:
                if tf not in market_data_multi:
                    logger.warning(f"Missing timeframe data: {tf}")
                    return self._default_hold()
            
            # Build detailed analysis prompt
            prompt = self._build_analysis_prompt(market_data_multi)
            
            # Get AI analysis from Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse response
            decision = self._parse_response(response.text)
            
            # Validate decision
            decision = self._validate_decision(decision, market_data_multi)
            
            return decision
            
        except Exception as e:
            logger.error(f"❌ Multi-timeframe AI error: {e}")
            return self._default_hold(error=str(e))
    
    def _build_analysis_prompt(self, market_data_multi: Dict) -> str:
        """Build comprehensive analysis prompt for Gemini"""
        
        return f"""
You are an expert multi-timeframe cryptocurrency trader analyzing BTCUSDT.

MULTI-TIMEFRAME ANALYSIS:

📊 1-MINUTE TIMEFRAME (Scalping Entry):
- Price: ${market_data_multi['1m'].get('price', 0):,.2f}
- RSI: {market_data_multi['1m'].get('rsi', 50):.1f}
- EMA(9): ${market_data_multi['1m'].get('ema_fast', 0):,.2f}
- EMA(21): ${market_data_multi['1m'].get('ema_slow', 0):,.2f}
- Volume Ratio: {market_data_multi['1m'].get('volume_ratio', 1.0):.2f}x
- Trend: {market_data_multi['1m'].get('trend', 'NEUTRAL')}
- ATR: ${market_data_multi['1m'].get('atr', 0):.2f}

📊 5-MINUTE TIMEFRAME (Short-term Context):
- Price: ${market_data_multi['5m'].get('price', 0):,.2f}
- RSI: {market_data_multi['5m'].get('rsi', 50):.1f}
- Trend: {market_data_multi['5m'].get('trend', 'NEUTRAL')}
- EMA Cross: {"Bullish" if market_data_multi['5m'].get('ema_fast', 0) > market_data_multi['5m'].get('ema_slow', 0) else "Bearish"}
- Volume: {market_data_multi['5m'].get('volume_ratio', 1.0):.2f}x

📊 15-MINUTE TIMEFRAME (Medium-term Direction):
- Price: ${market_data_multi['15m'].get('price', 0):,.2f}
- RSI: {market_data_multi['15m'].get('rsi', 50):.1f}
- Trend: {market_data_multi['15m'].get('trend', 'NEUTRAL')}
- Price Position: {"Above EMAs" if market_data_multi['15m'].get('price', 0) > market_data_multi['15m'].get('ema_slow', 0) else "Below EMAs"}

📊 1-HOUR TIMEFRAME (Overall Bias):
- Price: ${market_data_multi['1h'].get('price', 0):,.2f}
- RSI: {market_data_multi['1h'].get('rsi', 50):.1f}
- Trend: {market_data_multi['1h'].get('trend', 'NEUTRAL')}
- Major Trend: {"BULLISH" if market_data_multi['1h'].get('ema_fast', 0) > market_data_multi['1h'].get('ema_slow', 0) else "BEARISH"}

ADVANCED DECISION RULES:

✅ STRONG BUY CONDITIONS:
1. 1m: Fast EMA > Slow EMA (immediate bullish)
2. 5m: Trend = BULLISH (confirming)
3. 15m: Trend = BULLISH (supporting)
4. 1h: Trend = BULLISH (major trend aligned)
5. 1m RSI: 30-65 (not overbought)
6. Volume: >1.2x average
7. All timeframes aligned = HIGH CONFIDENCE (85-95%)

⚠️ MODERATE BUY CONDITIONS:
1. 1m + 5m bullish (but 15m/1h mixed)
2. Confidence = MEDIUM (60-75%)
3. Smaller position size recommended

❌ STRONG SELL CONDITIONS:
1. 1m: Fast EMA < Slow EMA (immediate bearish)
2. 5m: Trend = BEARISH (confirming)
3. 15m: Trend = BEARISH (supporting)
4. 1h: Trend = BEARISH (major trend aligned)
5. 1m RSI: 35-70 (not oversold)
6. Volume: >1.2x average

🛑 HOLD CONDITIONS:
1. Conflicting signals across timeframes
2. Low volume (<1.0x average)
3. Choppy/ranging market
4. RSI in extreme zones (>70 or <30) without confirmation

TIMEFRAME WEIGHT SYSTEM:
- 1m: 40% weight (entry timing)
- 5m: 25% weight (short-term confirmation)
- 15m: 20% weight (trend filter)
- 1h: 15% weight (bias filter)

RISK MANAGEMENT:
- LOW RISK: 3-4 timeframes aligned, RSI in middle zones
- MEDIUM RISK: 2 timeframes aligned, moderate RSI
- HIGH RISK: 1 timeframe only, extreme RSI or low volume

STOP LOSS & TAKE PROFIT:
- Stop Loss: Set at recent swing low + 1 ATR buffer
- Take Profit: Set at 2:1 or 3:1 risk-reward ratio

RESPOND IN EXACT JSON FORMAT (no markdown, pure JSON):
{{
    "action": "BUY" or "SELL" or "HOLD",
    "confidence": 0.0 to 1.0,
    "entry_price": {market_data_multi['1m'].get('price', 0)},
    "stop_loss": number,
    "take_profit": number,
    "timeframe_alignment": {{
        "1m": "BULLISH/BEARISH/NEUTRAL",
        "5m": "BULLISH/BEARISH/NEUTRAL",
        "15m": "BULLISH/BEARISH/NEUTRAL",
        "1h": "BULLISH/BEARISH/NEUTRAL"
    }},
    "aligned_timeframes": number (0-4),
    "primary_reason": "brief explanation",
    "secondary_reasons": ["reason1", "reason2"],
    "risk_level": "LOW/MEDIUM/HIGH",
    "position_size_multiplier": 0.5 to 1.5,
    "rsi_status": "Overbought/Normal/Oversold",
    "volume_confirmation": true or false
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse Gemini response to JSON"""
        
        # Clean markdown formatting
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        # Parse JSON
        decision = json.loads(response_text)
        return decision
    
    def _validate_decision(self, decision: Dict, market_data: Dict) -> Dict:
        """Validate and sanitize decision"""
        
        # Ensure required fields
        required = ['action', 'confidence', 'entry_price', 'aligned_timeframes']
        for field in required:
            if field not in decision:
                logger.warning(f"Missing field in decision: {field}")
                return self._default_hold()
        
        # Validate action
        if decision['action'] not in ['BUY', 'SELL', 'HOLD']:
            decision['action'] = 'HOLD'
        
        # Validate confidence
        decision['confidence'] = max(0, min(1, decision.get('confidence', 0)))
        
        # Validate aligned timeframes
        decision['aligned_timeframes'] = int(decision.get('aligned_timeframes', 0))
        decision['aligned_timeframes'] = max(0, min(4, decision['aligned_timeframes']))
        
        # Validate risk level
        if decision.get('risk_level') not in ['LOW', 'MEDIUM', 'HIGH']:
            decision['risk_level'] = 'MEDIUM'
        
        # Set defaults if missing
        decision.setdefault('stop_loss', 0)
        decision.setdefault('take_profit', 0)
        decision.setdefault('primary_reason', 'Multi-timeframe analysis')
        decision.setdefault('position_size_multiplier', 1.0)
        
        return decision
    
    def _default_hold(self, error: str = "") -> Dict:
        """Return safe HOLD decision"""
        return {
            'action': 'HOLD',
            'confidence': 0,
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'timeframe_alignment': {
                '1m': 'NEUTRAL',
                '5m': 'NEUTRAL',
                '15m': 'NEUTRAL',
                '1h': 'NEUTRAL'
            },
            'aligned_timeframes': 0,
            'primary_reason': f'Error or insufficient data: {error}',
            'risk_level': 'HIGH',
            'volume_confirmation': False
        }
    
    def get_alignment_score(self, decision: Dict) -> float:
        """
        Calculate overall alignment score (0-1)
        
        Based on:
        - Number of aligned timeframes (0-4)
        - Confidence level (0-1)
        - Risk level
        """
        
        alignment = decision.get('aligned_timeframes', 0) / 4
        confidence = decision.get('confidence', 0)
        risk_factor = {'LOW': 1.0, 'MEDIUM': 0.8, 'HIGH': 0.5}.get(
            decision.get('risk_level', 'HIGH'), 0.5
        )
        
        return alignment * confidence * risk_factor
    
    def should_trade(self, decision: Dict, min_alignment: int = 3, min_confidence: float = 0.7) -> bool:
        """
        Determine if trade should be executed based on criteria
        
        Args:
            decision: Decision from analyze_market_advanced
            min_alignment: Minimum aligned timeframes (0-4)
            min_confidence: Minimum confidence level (0-1)
        
        Returns:
            True if trade meets criteria, False otherwise
        """
        
        if decision['action'] == 'HOLD':
            return False
        
        aligned = decision.get('aligned_timeframes', 0)
        confidence = decision.get('confidence', 0)
        
        return aligned >= min_alignment and confidence >= min_confidence


# ============= HELPER FUNCTIONS =============

def format_decision_for_display(decision: Dict) -> str:
    """Format decision for logging/display"""
    
    action = decision.get('action', 'HOLD')
    confidence = decision.get('confidence', 0) * 100
    aligned = decision.get('aligned_timeframes', 0)
    risk = decision.get('risk_level', 'UNKNOWN')
    reason = decision.get('primary_reason', 'N/A')
    
    return f"""
╔════════════════════════════════════════════════════════════╗
║         MULTI-TIMEFRAME AI ANALYSIS RESULT                ║
╚════════════════════════════════════════════════════════════╝

📊 ACTION: {action}
💯 CONFIDENCE: {confidence:.0f}%
📈 ALIGNED TIMEFRAMES: {aligned}/4
⚠️  RISK LEVEL: {risk}
💡 REASON: {reason}

Timeframe Status:
  1m:  {decision.get('timeframe_alignment', {}).get('1m', 'UNKNOWN')}
  5m:  {decision.get('timeframe_alignment', {}).get('5m', 'UNKNOWN')}
  15m: {decision.get('timeframe_alignment', {}).get('15m', 'UNKNOWN')}
  1h:  {decision.get('timeframe_alignment', {}).get('1h', 'UNKNOWN')}

Entry: ${decision.get('entry_price', 0):,.2f}
SL:    ${decision.get('stop_loss', 0):,.2f}
TP:    ${decision.get('take_profit', 0):,.2f}
Size:  {decision.get('position_size_multiplier', 1.0):.1f}x

╔════════════════════════════════════════════════════════════╝
"""

