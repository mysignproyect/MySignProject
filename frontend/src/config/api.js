const API_BASE_URL = import.meta.env.PROD
  ? "https://mysignproject.onrender.com/api"
  : "http://localhost:8000";

export default API_BASE_URL;
