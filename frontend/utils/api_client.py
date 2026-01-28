# frontend/utils/api_client.py
"""API client for backend communication."""

import requests
from typing import Dict, Optional, Any
from frontend.config import API_BASE_URL


class APIClient:
    """Client for communicating with the FastAPI backend."""
    
    def __init__(self):
        self.base_url = API_BASE_URL
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make an HTTP request."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, params=params)
            elif method == "POST":
                response = requests.post(url, json=data)
            elif method == "PUT":
                response = requests.put(url, json=data)
            elif method == "DELETE":
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    # User endpoints
    def create_user(self, user_data: Dict) -> Dict:
        return self._request("POST", "/users/", data=user_data)
    
    def get_user(self, user_id: str) -> Dict:
        return self._request("GET", f"/users/{user_id}")
    
    def get_user_by_email(self, email: str) -> Dict:
        return self._request("GET", f"/users/email/{email}")
    
    def update_user(self, user_id: str, user_data: Dict) -> Dict:
        return self._request("PUT", f"/users/{user_id}", data=user_data)
    
    def get_user_stats(self, user_id: str) -> Dict:
        return self._request("GET", f"/users/{user_id}/stats")
    
    # Plan endpoints
    def generate_plan(self, user_id: str, plan_type: str, preferences: str = None) -> Dict:
        data = {
            "user_id": user_id,
            "plan_type": plan_type,
            "additional_preferences": preferences
        }
        return self._request("POST", "/plans/generate", data=data)
    
    def generate_workout_plan(self, user_id: str) -> Dict:
        return self._request("POST", f"/plans/{user_id}/workout")
    
    def generate_diet_plan(self, user_id: str) -> Dict:
        return self._request("POST", f"/plans/{user_id}/diet")
    
    def get_active_plans(self, user_id: str) -> Dict:
        return self._request("GET", f"/plans/{user_id}/active")
    
    def regenerate_plan(self, user_id: str, plan_type: str) -> Dict:
        return self._request("POST", f"/plans/{user_id}/regenerate/{plan_type}")
    
    # Progress endpoints
    def log_weight(self, user_id: str, weight_kg: float, date: str = None, notes: str = None) -> Dict:
        params = {"weight_kg": weight_kg}
        if date:
            params["log_date"] = date
        if notes:
            params["notes"] = notes
        return self._request("POST", f"/progress/{user_id}/weight", params=params)
    
    def log_calories(self, user_id: str, calorie_data: Dict) -> Dict:
        return self._request("POST", f"/progress/{user_id}/calories", data=calorie_data)
    
    def log_workout(self, user_id: str, workout_data: Dict) -> Dict:
        return self._request("POST", f"/progress/{user_id}/workout", data=workout_data)
    
    def get_progress_summary(self, user_id: str, days: int = 30) -> Dict:
        return self._request("GET", f"/progress/{user_id}/summary", params={"days": days})
    
    def get_chart_data(self, user_id: str, days: int = 30) -> Dict:
        return self._request("GET", f"/progress/{user_id}/charts", params={"days": days})
    
    # RAG endpoints
    def query_rag(self, user_id: str, query: str, plan_type: str = "both") -> Dict:
        data = {
            "user_id": user_id,
            "query": query,
            "plan_type": plan_type,
            "include_progress_context": True
        }
        return self._request("POST", "/rag/query", data=data)


# Singleton instance
api_client = APIClient()