# frontend/api_client.py
"""API client for backend communication."""

import requests
from typing import Dict, Optional
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


class APIClient:
    """Client for communicating with the FastAPI backend."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or API_BASE_URL
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make an HTTP request."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=30)
            elif method == "PUT":
                response = requests.put(url, json=data, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to backend. Make sure the API server is running on port 8000."}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except requests.exceptions.HTTPError as e:
            try:
                return {"error": e.response.json().get("detail", str(e))}
            except:
                return {"error": str(e)}
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
    def log_weight(self, user_id: str, weight_kg: float, 
                   log_date: str = None, notes: str = None) -> Dict:
        params = {"weight_kg": weight_kg}
        if log_date:
            params["log_date"] = log_date
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
    
    # Health check
    def health_check(self) -> Dict:
        return self._request("GET", "/health")


# Create singleton instance
api_client = APIClient()