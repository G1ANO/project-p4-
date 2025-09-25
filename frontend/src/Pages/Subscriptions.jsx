import { useEffect, useState } from "react";

export default function Subscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) return;

    fetch(`https://project-p4-20zj.onrender.com/subscriptions/${user.id}`)
      .then((res) => res.json())
      .then((data) => setSubscriptions(data));
  }, []);

  const cancelSubscription = async (subId) => {
    await fetch(`https://project-p4-20zj.onrender.com/subscriptions/${subId}`, {
      method: "DELETE",
    });
    setSubscriptions(subscriptions.filter((sub) => sub.id !== subId));
  };

  const getStatusClass = (status) => {
    if (status.toLowerCase() === "active") return "status-active";
    if (status.toLowerCase() === "almost over") return "status-almost";
    if (status.toLowerCase() === "cancelled") return "status-cancelled";
    return "";
  };

  const formatDate = (dateStr) => new Date(dateStr).toLocaleString();

  return (
    <div className="subscriptions-page">
      <h1>My Subscriptions</h1>
      {subscriptions.length === 0 ? (
        <p>No subscriptions found.</p>
      ) : (
        <ul className="subscriptions-list">
          {subscriptions.map((sub) => (
            <li key={sub.id} className="subscription-item">
              <span className={`status ${getStatusClass(sub.status)}`}>
                {sub.status}
              </span>
              <div className="plan-details">
                <p className="plan-name">{sub.plan?.name || "Unknown Plan"}</p>
                <p>Bought: {formatDate(sub.created_at)}</p>
                <p>Ends: {formatDate(sub.ends_at)}</p>
              </div>
              {sub.status.toLowerCase() !== "cancelled" && (
                <button
                  className="cancel-btn"
                  onClick={() => cancelSubscription(sub.id)}
                >
                  Cancel
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
