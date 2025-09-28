import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Subscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (!savedUser) {
      navigate("/login");
      return;
    }

    const userObj = JSON.parse(savedUser);
    setUser(userObj);

    fetch(`http://localhost:5000/subscriptions/${userObj.id}`)
      .then((res) => res.json())
      .then((data) => setSubscriptions(data))
      .catch((err) => console.error("Error fetching subscriptions:", err));
  }, [navigate]);

  const cancelSubscription = async (subId) => {
    try {
      await fetch(`http://localhost:5000/subscriptions/${subId}`, {
        method: "DELETE",
      });
      setSubscriptions(subscriptions.filter((sub) => sub.id !== subId));
    } catch (err) {
      console.error("Error cancelling subscription:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    
    window.dispatchEvent(new Event('userLogout'));
    navigate("/login");
  };

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  return (
    <div className="subscriptions-page">
      <div className="subscriptions-header">
        <h1>Active Subscriptions</h1>
        <p>Manage your WiFi access subscriptions</p>
      </div>

      {subscriptions.length === 0 ? (
        <div className="no-subscriptions">
          <p>No active subscriptions found.</p>
          <p>Visit the Plans page to subscribe to a WiFi plan.</p>
        </div>
      ) : (
        <div className="subscriptions-grid">
          {subscriptions.map((sub) => (
            <div key={sub.id} className="subscription-card">
              <div className="subscription-header">
                <h3>{sub.plan?.name || "Unknown Plan"}</h3>
                <span className={`status ${sub.status === 'active' ? 'status-active' : 'status-inactive'}`}>
                  {sub.status}
                </span>
              </div>

              <div className="subscription-details">
                <div className="detail-row">
                  <span className="label">Purchased:</span>
                  <span className="value">{formatDateTime(sub.timestamp)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Expires:</span>
                  <span className="value">{formatDateTime(sub.ends_at)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Duration:</span>
                  <span className="value">
                    {sub.plan?.duration_minutes < 60 ?
                      `${sub.plan?.duration_minutes} minutes` :
                      `${Math.floor(sub.plan?.duration_minutes / 60)} hour${Math.floor(sub.plan?.duration_minutes / 60) > 1 ? 's' : ''}`
                    }
                  </span>
                </div>
                <div className="detail-row">
                  <span className="label">Price:</span>
                  <span className="value">KSh {sub.plan?.price}</span>
                </div>
              </div>

              {sub.status.toLowerCase() === "active" && (
                <button
                  className="cancel-btn"
                  onClick={() => cancelSubscription(sub.id)}
                >
                  Cancel Subscription
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="logout-section">
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}
