import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Plans() {
  const [plans, setPlans] = useState([]);
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Get current user from localStorage
    const savedUser = localStorage.getItem("user");
    if (!savedUser) {
      navigate("/login");
      return;
    }
    setUser(JSON.parse(savedUser));

    // Fetch plans
    axios.get("http://localhost:5000/plans")
      .then((res) => setPlans(res.data))
      .catch((err) => console.error("Error fetching plans:", err));
  }, [navigate]);

  const handleSubscribe = async (planId) => {
    if (!user) {
      setMessage("Please log in to subscribe!");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/subscriptions", {
        user_id: user.id,
        plan_id: planId,
      });
      setMessage("✅ Subscription successful! Check your subscriptions page.");

      // Clear message after 3 seconds
      setTimeout(() => setMessage(""), 3000);
    } catch (err) {
      setMessage(err.response?.data?.error || "❌ Subscription failed");
      setTimeout(() => setMessage(""), 3000);
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
