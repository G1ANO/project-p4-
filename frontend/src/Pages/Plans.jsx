import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { API_ENDPOINTS } from "../config";

export default function Plans() {
  const [plans, setPlans] = useState([]);
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    
    const savedUser = localStorage.getItem("user");
    if (!savedUser) {
      navigate("/login");
      return;
    }
    setUser(JSON.parse(savedUser));

    
    axios.get(API_ENDPOINTS.PLANS)
      .then((res) => setPlans(res.data))
      .catch((err) => console.error("Error fetching plans:", err));
  }, [navigate]);

  const handleSubscribe = async (planId) => {
    if (!user) {
      setMessage("Please log in to subscribe!");
      return;
    }

    try {
      const res = await axios.post(API_ENDPOINTS.SUBSCRIPTIONS, {
        user_id: user.id,
        plan_id: planId,
      });
      setMessage("✅ Subscription successful! Check your subscriptions page.");


      setTimeout(() => setMessage(""), 5000);
    } catch (err) {
      // Handle overlap error specifically
      if (err.response?.status === 409) {
        const errorData = err.response.data;
        setMessage(`❌ ${errorData.message || errorData.error}`);
      } else {
        setMessage(err.response?.data?.error || "❌ Subscription failed");
      }
      setTimeout(() => setMessage(""), 8000); // Longer timeout for overlap messages
    }
  };

  return (
    <div className="plans-container">
      <div className="plans-header">
        <h1>WiFi Plans</h1>
        <p>Choose your internet access plan</p>
      </div>

      {message && <div className="message">{message}</div>}

      <div className="plans-grid">
        {plans.map((plan) => (
          <div key={plan.id} className="plan-card">
            <div className="plan-header">
              <h2>{plan.name}</h2>
              <div className="plan-price">KSh {plan.price}</div>
            </div>
            <div className="plan-details">
              <div className="plan-duration">
                Duration: {plan.duration_minutes < 60 ?
                  `${plan.duration_minutes} minutes` :
                  `${Math.floor(plan.duration_minutes / 60)} hour${Math.floor(plan.duration_minutes / 60) > 1 ? 's' : ''}`
                }
              </div>
            </div>
            <button
              className="subscribe-btn"
              onClick={() => handleSubscribe(plan.id)}
            >
              Subscribe Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
