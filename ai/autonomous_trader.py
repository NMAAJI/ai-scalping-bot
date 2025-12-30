"""
Autonomous AI Trading Engine
Fully automated trading with Gemini AI and backup API support
Direct AI decision-making without human intervention
"""

import json
import logging
import time
from typing import Dict, Optional, List
from datetime import datetime
from google import genai
from config.settings import (
    AI_MODEL, AI_MAX_RETRIES, AI_TIMEOUT, TRADING_CONFIG,
    GEMINI_API_KEY
)

logger = logging.getLogger(__name__)


class AutonomousAITrader:
    """
    Fully autonomous AI trading engine
    - Multi-turn conversations with AI
    - Backup API support
    - Automatic trade execution
    - No human intervention required
    """
    
    def __init__(self, primary_api_key: str, backup_api_key: Optional[str] = None):
        """
        Initialize autonomous AI trader
        
        Args:
            primary_api_key: Gemini API key (primary)
            backup_api_key: Backup API key (OpenAI, Anthropic, etc.)
        """
        self.primary_client = genai.Client(api_key=primary_api_key)
        self.backup_api_key = backup_api_key
        self.model = AI_MODEL
        self.max_retries = AI_MAX_RETRIES
        self.timeout = AI_TIMEOUT
        
        # Conversation history for multi-turn discussions
        self.conversation_history: List[Dict] = []
        
        # Decision audit trail
        self.decision_log: List[Dict] = []
        
        # Market context
        self.current_market_state = None
        self.last_decision = None
        
    def analyze_and_execute(self, market_data: Dict, execute: bool = True) -> Dict:
        """
        Full autonomous analysis and execution
        
        Args:
            market_data: Current market data
            execute: Whether to actually execute trade (default: True)
        
        Returns:
            Decision with execution status
        """
        try:
            # Step 1: Initial analysis
            logger.info("🤖 Starting autonomous AI analysis...")
            initial_analysis = self._initial_analysis(market_data)
            
            # Step 2: Multi-turn refinement
            logger.info("💭 Refining analysis through AI conversation...")
            refined_decision = self._refine_decision(initial_analysis, market_data)
            
            # Step 3: Risk validation
            logger.info("⚠️ Validating risk parameters...")
            risk_validated = self._validate_risk(refined_decision, market_data)
            
            # Step 4: Confidence verification
            logger.info("✅ Verifying confidence levels...")
            final_decision = self._verify_confidence(risk_validated)
            
            # Step 5: Log decision
            self._log_decision(final_decision, market_data)
            
            # Step 6: Execute if approved
            if execute and final_decision['action'] != 'HOLD':
                final_decision['execution'] = {
                    'status': 'READY_FOR_EXECUTION',
                    'timestamp': datetime.now().isoformat(),
                    'auto_trade': True
                }
                logger.info(f"🚀 Trade ready for execution: {final_decision['action']}")
            else:
                final_decision['execution'] = {
                    'status': 'HOLD_NO_EXECUTION',
                    'reason': 'Confidence too low or market unclear'
                }
            
            self.last_decision = final_decision
            return final_decision
            
        except Exception as e:
            logger.error(f"❌ Autonomous analysis error: {e}")
            return self._fallback_decision('ERROR', str(e))
    
    def _initial_analysis(self, market_data: Dict) -> Dict:
        """
        Phase 1: Initial AI analysis
        """
        try:
            prompt = self._build_initial_prompt(market_data)
            
            response = self.primary_client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            analysis = self._parse_response(response.text)
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': prompt,
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation_history.append({
                'role': 'ai',
                'content': response.text,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"📊 Initial analysis: {analysis['action']} ({analysis['confidence']:.2%})")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Initial analysis error: {e}")
            if self.backup_api_key:
                logger.info("🔄 Switching to backup API...")
                return self._backup_analysis(market_data)
            raise
    
    def _refine_decision(self, initial: Dict, market_data: Dict) -> Dict:
        """
        Phase 2: Multi-turn conversation to refine decision
        Ask AI follow-up questions
        """
        try:
            # Build refinement prompt
            refinement_prompt = f"""
Based on your initial analysis of {initial['action']} with {initial['confidence']:.2%} confidence:

1. What are the KEY FACTORS supporting this decision?
2. What RISKS or CONTRADICTIONS exist?
3. Should we ADJUST the confidence level?
4. Are there ALTERNATIVE signals we should consider?
5. What is the probability of this trade being PROFITABLE?

Current analysis:
- Action: {initial['action']}
- Confidence: {initial['confidence']:.2%}
- Entry: ${initial['entry_price']}
- Stop Loss: ${initial['stop_loss']}
- Take Profit: ${initial['take_profit']}

Provide a refined decision in JSON format with:
- refined_action (BUY/SELL/HOLD)
- refined_confidence (0.0-1.0)
- key_factors (array of supporting factors)
- risks (array of risk factors)
- probability_profit (0.0-1.0)
"""
            
            # Get refinement from AI
            response = self.primary_client.models.generate_content(
                model=self.model,
                contents=self.conversation_history + [{
                    'parts': [{'text': refinement_prompt}]
                }]
            )
            
            refinement = self._parse_response(response.text)
            
            # Add to conversation
            self.conversation_history.append({
                'role': 'user',
                'content': refinement_prompt,
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation_history.append({
                'role': 'ai',
                'content': response.text,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"💭 Refined decision: {refinement.get('refined_action', initial['action'])} "
                       f"({refinement.get('refined_confidence', initial['confidence']):.2%})")
            
            # Merge with initial analysis
            return {
                **initial,
                'action': refinement.get('refined_action', initial['action']),
                'confidence': refinement.get('refined_confidence', initial['confidence']),
                'key_factors': refinement.get('key_factors', []),
                'risks': refinement.get('risks', []),
                'probability_profit': refinement.get('probability_profit', 0.5)
            }
            
        except Exception as e:
            logger.warning(f"Refinement error: {e}, using initial analysis")
            return initial
    
    def _validate_risk(self, decision: Dict, market_data: Dict) -> Dict:
        """
        Phase 3: Validate risk parameters
        Ensure decision complies with risk management rules
        """
        try:
            risk_prompt = f"""
Validate this trading decision against risk management rules:

Decision: {decision['action']}
Entry: ${decision['entry_price']}
Stop Loss: ${decision['stop_loss']}
Take Profit: ${decision['take_profit']}
Confidence: {decision['confidence']:.2%}

Risk Management Rules:
- Max loss per trade: {TRADING_CONFIG['risk_per_trade']*100}% of capital
- Min reward/risk ratio: 2:1
- Max daily loss: {TRADING_CONFIG.get('daily_loss_limit', 0.05)*100}%
- Min winning probability: 55%

Is this trade COMPLIANT with all rules? 
Would you APPROVE or REJECT this trade?
What adjustments would make it better?

Respond with JSON:
{{
    "is_compliant": true/false,
    "approval": "APPROVE" or "REJECT" or "CONDITIONAL",
    "reason": "explanation",
    "suggested_adjustments": {{...}},
    "safety_score": 0.0-1.0
}}
"""
            
            response = self.primary_client.models.generate_content(
                model=self.model,
                contents=self.conversation_history + [{
                    'parts': [{'text': risk_prompt}]
                }]
            )
            
            validation = self._parse_response(response.text)
            
            logger.info(f"⚠️ Risk validation: {validation.get('approval', 'UNKNOWN')} "
                       f"(Safety: {validation.get('safety_score', 0):.2%})")
            
            return {
                **decision,
                'risk_validated': validation.get('is_compliant', False),
                'approval_status': validation.get('approval', 'REJECT'),
                'safety_score': validation.get('safety_score', 0),
                'suggested_adjustments': validation.get('suggested_adjustments', {})
            }
            
        except Exception as e:
            logger.warning(f"Risk validation error: {e}")
            return {**decision, 'risk_validated': False, 'safety_score': 0}
    
    def _verify_confidence(self, decision: Dict) -> Dict:
        """
        Phase 4: Final confidence verification
        Ensure decision meets minimum confidence thresholds
        """
        min_confidence = TRADING_CONFIG.get('min_confidence', 0.5)
        
        # Check multiple confidence factors
        is_confident = (
            decision.get('confidence', 0) >= min_confidence and
            decision.get('probability_profit', 0) >= 0.55 and
            decision.get('safety_score', 0) >= 0.6 and
            decision.get('approval_status') != 'REJECT'
        )
        
        if not is_confident:
            logger.info("⚠️ Confidence below threshold, setting to HOLD")
            decision['action'] = 'HOLD'
        
        decision['final_confidence'] = min(
            decision.get('confidence', 0.5),
            decision.get('probability_profit', 0.5),
            decision.get('safety_score', 0.5)
        )
        
        return decision
    
    def _log_decision(self, decision: Dict, market_data: Dict) -> None:
        """Log AI decision for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision': decision,
            'market_data': {
                'price': market_data.get('price'),
                'rsi': market_data.get('rsi'),
                'trend': market_data.get('trend'),
                'volume_ratio': market_data.get('volume_ratio')
            },
            'conversation_turns': len(self.conversation_history),
            'ai_reasoning': decision.get('reasoning', 'N/A')
        }
        
        self.decision_log.append(log_entry)
        
        # Save to file for auditing
        try:
            with open('logs/ai_decisions.jsonl', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            logger.info("📝 Decision logged to audit trail")
        except Exception as e:
            logger.warning(f"Could not log decision: {e}")
    
    def _build_initial_prompt(self, market_data: Dict) -> str:
        """Build comprehensive initial analysis prompt"""
        return f"""
You are an EXPERT autonomous cryptocurrency trading AI with years of professional trading experience.

CURRENT MARKET STATE:
- Symbol: {TRADING_CONFIG['symbol']}
- Price: ${market_data['price']:.2f}
- RSI(14): {market_data['rsi']:.2f}
- EMA(9): ${market_data.get('ema_fast', 0):.2f}
- EMA(21): ${market_data.get('ema_slow', 0):.2f}
- ATR: ${market_data.get('atr', 0):.2f}
- Volume: {market_data['volume']:.0f} (Ratio: {market_data.get('volume_ratio', 1):.2f}x)
- Trend: {market_data['trend']}
- Signal Strength: {market_data.get('signal_strength', 'UNKNOWN')}

YOUR TASK:
1. ANALYZE current market structure and momentum
2. IDENTIFY entry/exit points with precision
3. ASSESS market condition (trending/ranging/volatile)
4. DETERMINE trade direction with CONFIDENCE score
5. CALCULATE risk-reward ratio for optimal position sizing
6. PREPARE DETAILED REASONING for your decision

TRADING RULES (STRICT):
- BUY: Fast EMA > Slow EMA + RSI < 70 + Volume confirmation
- SELL: Fast EMA < Slow EMA + RSI > 30 + Volume confirmation
- HOLD: No clear setup or mixed signals
- Min Confidence for trade: 60%
- Min Risk/Reward: 1:2
- Max leverage: 2:1

RESPOND IN VALID JSON (no markdown, no code blocks):
{{
    "action": "BUY"|"SELL"|"HOLD",
    "confidence": 0.60,
    "entry_price": {market_data['price']},
    "stop_loss": {market_data['price'] - market_data.get('atr', 10)},
    "take_profit": {market_data['price'] + market_data.get('atr', 10) * 2},
    "reasoning": "Clear explanation of decision",
    "market_structure": "trending|ranging|volatile",
    "next_resistance": 0,
    "next_support": 0,
    "signal_strength": "weak|moderate|strong"
}}
"""
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse AI response with robust error handling"""
        try:
            # Clean markdown if present
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate critical fields
            required = ['action', 'confidence', 'entry_price', 'stop_loss', 'take_profit', 'reasoning']
            for field in required:
                if field not in result:
                    logger.error(f"Missing required field: {field}")
                    raise ValueError(f"Missing field: {field}")
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}\nText: {response_text[:500]}")
            raise
        except Exception as e:
            logger.error(f"Parse error: {e}")
            raise
    
    def _backup_analysis(self, market_data: Dict) -> Dict:
        """
        Fallback to backup API when primary fails
        Can integrate OpenAI, Anthropic, or other services
        """
        logger.warning("⚠️ Primary API failed, using backup analysis")
        
        # Implement backup API logic here
        # For now, use simple technical analysis
        
        # Simple fallback: Use technical indicators only
        price = market_data['price']
        rsi = market_data['rsi']
        ema_fast = market_data.get('ema_fast', price)
        ema_slow = market_data.get('ema_slow', price)
        atr = market_data.get('atr', price * 0.01)
        
        # Rule-based decision
        if ema_fast > ema_slow and rsi < 70:
            action = 'BUY'
            confidence = 0.65
        elif ema_fast < ema_slow and rsi > 30:
            action = 'SELL'
            confidence = 0.65
        else:
            action = 'HOLD'
            confidence = 0.4
        
        return {
            'action': action,
            'confidence': confidence,
            'entry_price': price,
            'stop_loss': price - atr if action == 'BUY' else price + atr,
            'take_profit': price + atr * 2 if action == 'BUY' else price - atr * 2,
            'reasoning': 'Backup API fallback - technical analysis only',
            'using_backup': True
        }
    
    def _fallback_decision(self, action: str = 'HOLD', reason: str = 'Error') -> Dict:
        """Return safe fallback decision"""
        return {
            'action': action,
            'confidence': 0.0,
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'reasoning': f'Fallback due to {reason}',
            'is_fallback': True,
            'execution': {
                'status': 'REJECTED',
                'reason': reason
            }
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history for audit/review"""
        return self.conversation_history
    
    def get_decision_log(self) -> List[Dict]:
        """Get all logged decisions"""
        return self.decision_log
    
    def clear_conversation(self) -> None:
        """Clear conversation history for new analysis"""
        self.conversation_history = []
        logger.info("🗑️ Conversation history cleared")


# Backward compatibility with old analyzer
class GeminiAnalyzer:
    """Compatibility wrapper for existing code"""
    
    def __init__(self, api_key: str):
        self.trader = AutonomousAITrader(api_key)
    
    def analyze_market(self, market_data: Dict) -> Dict:
        """Simple analysis without full autonomy"""
        decision = self.trader.analyze_and_execute(market_data, execute=False)
        
        # Return in old format
        return {
            'action': decision['action'],
            'confidence': decision.get('final_confidence', decision['confidence']),
            'entry_price': decision['entry_price'],
            'stop_loss': decision['stop_loss'],
            'take_profit': decision['take_profit'],
            'reasoning': decision['reasoning']
        }
