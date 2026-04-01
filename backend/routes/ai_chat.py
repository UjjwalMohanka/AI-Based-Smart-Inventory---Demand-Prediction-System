from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
from anthropic import Anthropic

ai_chat_bp = Blueprint('ai_chat', __name__, url_prefix='/api/chat')

# Initialize Anthropic client
def get_anthropic_client():
    """Get Anthropic client with API key from environment"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


@ai_chat_bp.route('', methods=['POST'])
@jwt_required()
def chat():
    """
    Chat with Claude AI assistant for inventory insights
    
    Request body:
        {
            "message": str,
            "context": {
                "product_id": int (optional),
                "product_name": str (optional),
                "current_stock": int (optional),
                "predictions": list (optional)
            }
        }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data:
            return jsonify({'error': 'message required'}), 400
        
        user_message = data['message']
        context = data.get('context', {})
        
        # Get Anthropic client
        client = get_anthropic_client()
        if not client:
            return jsonify({
                'error': 'AI chat is not configured. Please set ANTHROPIC_API_KEY environment variable.'
            }), 503
        
        # Build system prompt with context
        system_prompt = """You are an expert AI assistant for inventory management and demand forecasting. 

Your role is to help users:
- Understand their stock levels and alerts
- Interpret demand predictions and forecasts
- Suggest procurement strategies and reorder quantities
- Identify trends in sales and inventory data
- Provide actionable recommendations for inventory optimization

Be concise, professional, and data-driven. When making recommendations, explain your reasoning briefly.
Focus on actionable insights that help reduce stockouts and overstock situations."""

        # Add context information if provided
        if context:
            context_info = "\n\nCurrent Context:\n"
            if context.get('product_name'):
                context_info += f"- Product: {context['product_name']}\n"
            if context.get('current_stock') is not None:
                context_info += f"- Current Stock: {context['current_stock']} units\n"
            if context.get('reorder_point'):
                context_info += f"- Reorder Point: {context['reorder_point']} units\n"
            if context.get('predictions'):
                context_info += f"- Predicted Demand: {context['predictions']}\n"
            
            system_prompt += context_info
        
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        # Extract response text
        reply = response.content[0].text
        
        return jsonify({
            'reply': reply,
            'model': 'claude-sonnet-4-20250514'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'AI chat error: {str(e)}'}), 500
