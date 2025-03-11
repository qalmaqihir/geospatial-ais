# from flask import Blueprint, jsonify, request, session, make_response
# from services.llmService import generate_llm_response
# import logging
# import uuid

# logger = logging.getLogger(__name__)

# chat_bp = Blueprint('chat', __name__)

# @chat_bp.route('/chat', methods=['POST'])
# def handle_chat():
#     # Session validation
#     if 'session_id' not in session:
#         logger.warning("Unauthorized chat attempt")
#         return jsonify({'error': 'Invalid session'}), 401

#     # Request validation
#     data = request.get_json()
#     if not data or 'message' not in data:
#         logger.warning("Invalid request format")
#         return jsonify({'error': 'Message is required'}), 400

#     try:
#         logger.info(f"Chat request - Session: {session['session_id']}, Model: {data.get('model')}")
        
#         # Extract parameters with defaults
#         model = data.get('model', 'gpt-4')  # Default to GPT-4
#         print(f"Model Selected: {model}\n")
#         coordinates = data.get('coordinates', {})
#         message = data['message']

#         # Generate LLM response
#         response = generate_llm_response(
#             message=message,
#             model=model,
#             coordinates=coordinates
#         )
        
#         # Handle tool responses
#         if 'error' in response:
#             logger.error(f"LLM Error: {response['error']}")
#             return jsonify(response), 500
            
#         return jsonify(response)

#     except Exception as e:
#         logger.error(f"Chat processing failed: {str(e)}", exc_info=True)
#         return jsonify({'error': 'Internal server error'}), 500

# @chat_bp.route('/session', methods=['POST'])
# def create_session():
#     try:
#         # Generate new session ID
#         session_id = str(uuid.uuid4())
#         session['session_id'] = session_id
#         session['initialized'] = True
        
#         response = jsonify({
#             'message': 'Session initialized',
#             'session_id': session_id
#         })
        
#         # Set secure cookie
#         response.set_cookie(
#             'session_id',
#             session_id,
#             httponly=True,
#             secure=True,  # Requires HTTPS in production
#             samesite='Lax',
#             max_age=3600  # 1 hour expiration
#         )
        
#         logger.info(f"New session created: {session_id}")
#         return response

#     except Exception as e:
#         logger.error(f"Session creation failed: {str(e)}")
#         return jsonify({'error': 'Session initialization failed'}), 500



from flask import Blueprint, jsonify, request, session, make_response
from services.llmService import generate_llm_response
import logging
import uuid
import os

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def handle_chat():
    # Session validation
    if 'initialized' not in session:
        logger.warning("Unauthorized chat attempt")
        return jsonify({'error': 'Invalid session'}), 401

    # Request validation
    data = request.get_json()
    if not data or 'message' not in data:
        logger.warning("Invalid request format")
        return jsonify({'error': 'Message is required'}), 400

    try:
        logger.info(f"Chat request - Session: {session['session_id']}, Model: {data.get('model')}")
        
        # Extract parameters with defaults
        model = data.get('model', 'gpt-4')  # Default to GPT-4
        # print(f"Model Selected: {model}\n")  # Commented out for production
        coordinates = data.get('coordinates', {})
        message = data['message']

        # Generate LLM response
        response = generate_llm_response(
            message=message,
            model=model,
            coordinates=coordinates
        )
        
        # Handle tool responses
        if isinstance(response, dict) and 'error' in response:
            logger.error(f"LLM Error: {response['error']}")
            return jsonify(response), 500
            
        return jsonify(response)

    except Exception as e:
        logger.error(f"Chat processing failed: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/session', methods=['POST'])
def create_session():
    try:
        # Generate new session ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session['initialized'] = True
        
        response = jsonify({
            'message': 'Session initialized',
            'session_id': session_id
        })
        
        # Set secure cookie
        response.set_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=os.getenv('FLASK_ENV') == 'production',  # Secure only in production
            samesite='Lax',
            max_age=3600  # 1 hour expiration
        )
        
        logger.info(f"New session created: {session_id}")
        return response

    except Exception as e:
        logger.error(f"Session creation failed: {str(e)}")
        return jsonify({'error': 'Session initialization failed'}), 500