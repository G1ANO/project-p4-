import { useState, useEffect } from "react";
import axios from "axios";

export default function Plans() {
  const [plans, setPlans] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [message, setMessage] = useState("");

  
  useEffect(() => {
    axios.get("https://project-p4-20zj.onrender.com/plans")
      .then((res) => setPlans(res.data))
      .catch((err) => console.error("Error fetching plans:", err));

    axios.get("https://project-p4-20zj.onrender.com/users")
      .then((res) => {
        setUsers(res.data);
        if (res.data.length > 0) {
          setSelectedUser(res.data[0]); 
        }
      })
      .catch((err) => console.error("Error fetching users:", err));
  }, []);

  const handleSubscribe = async (planId) => {
    if (!selectedUser) {
      setMessage("No user selected!");
      return;
    }

    try {
      const res = await axios.post("https://project-p4-20zj.onrender.com/subscriptions", {
        user_id: selectedUser.id,
        plan_id: planId,
      });
      setMessage(
        `✅ ${selectedUser.username} subscribed to plan ID ${planId} successfully!`
      );
    } catch (err) {
      setMessage(err.response?.data?.error || "❌ Subscription failed");
    }
  };

  return (
    <div className="plans-container">
      <h1>Available Plans</h1>

      
      {users.length > 0 && (
        <div className="user-select">
          <label>Select User: </label>
          <select
            value={selectedUser?.id || ""}
            onChange={(e) =>
              setSelectedUser(users.find((u) => u.id === parseInt(e.target.value)))
            }
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>
      )}

      {message && <p className="message">{message}</p>}

      <div className="plans-grid">
        {plans.map((plan) => (
          <div key={plan.id} className="plan-card">
            <h2>{plan.name}</h2>
            <p>Duration: {plan.duration_minutes} minutes</p>
            <p>Price: ksh{plan.price}</p>
            <button onClick={() => handleSubscribe(plan.id)}>
              Subscribe
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
