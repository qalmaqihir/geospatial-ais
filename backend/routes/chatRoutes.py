from flask import Blueprint, jsonify, request, session, make_response
from services.llmService import generate_llm_response
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    session_id = request.cookies.get('session_id') or request.get_json().get('session')
    if not session_id or 'initialized' not in session:
        logger.warning("Invalid or expired session")
        return jsonify({'error': 'Invalid or expired session'}), 401

    data = request.get_json()
    if not data or 'message' not in data:
        logger.warning("Missing message in request")
        return jsonify({'error': 'Missing message in request'}), 400

    try:
        logger.debug(f"Processing chat request: {data}")
        response = generate_llm_response(data['message'], data.get('model', 'gpt-3'), data.get('coordinates'))
        return jsonify(response)
    except Exception as e:
        logger.error(f"Chat processing failed: {str(e)}")
        return jsonify({'error': f'Chat processing failed: {str(e)}'}), 500

@chat_bp.route('/session', methods=['POST'])
def create_session():
    session['initialized'] = True
    response = make_response(jsonify({'message': 'Session initialized'}))
    response.set_cookie('session_id', session.sid, httponly=True, samesite='Lax')
    logger.debug("Session created")
    return response


# from flask import Blueprint, jsonify, request, session, make_response
# from services.llmService import generate_llm_response
# import logging

# logger = logging.getLogger(__name__)

# chat_bp = Blueprint('chat', __name__)

# @chat_bp.route('/chat', methods=['POST'])
# def chat():
#     session_id = request.cookies.get('session_id') or request.get_json().get('session')
#     if not session_id or 'initialized' not in session:
#         logger.warning("Invalid or expired session")
#         return jsonify({'error': 'Invalid or expired session'}), 401

#     data = request.get_json()
#     if not data or 'message' not in data:
#         logger.warning("Missing message in request")
#         return jsonify({'error': 'Missing message in request'}), 400

#     try:
#         logger.debug(f"Processing chat request: {data}")
#         coordinates = data.get('coordinates', {})
#         response = generate_llm_response(data['message'], data.get('model', 'gpt-4'), coordinates)
#         return jsonify(response)
#     except Exception as e:
#         logger.error(f"Chat processing failed: {str(e)}")
#         return jsonify({'error': f'Chat processing failed: {str(e)}'}), 500

# @chat_bp.route('/session', methods=['POST'])
# def create_session():
#     session['initialized'] = True
#     response = make_response(jsonify({'message': 'Session initialized'}))
#     response.set_cookie('session_id', session.sid, httponly=True, samesite='Lax')
#     logger.debug("Session created")
#     return response