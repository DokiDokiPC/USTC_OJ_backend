from backend.blueprints.user.user import user_bp
from backend.blueprints.token.token import token_bp
from backend.blueprints.problem.problem import problem_bp
from backend.blueprints.status.status import status_bp

blueprints = [user_bp, token_bp, problem_bp, status_bp]
