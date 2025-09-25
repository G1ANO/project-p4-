import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const [user, setUser] = useState(null);
  const [subscriptions, setSubscriptions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (!savedUser) {
      navigate("/login", { replace: true });
      return;
    }

    const userObj = JSON.parse(savedUser);
    setUser(userObj);

    // Fetch subscriptions for this user
    axios
      .get(`http://localhost:5000/subscriptions/${userObj.id}`)
      .then((res) => setSubscriptions(res.data))
      .catch((err) => console.error(err));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/login", { replace: true });
  };

  return (
    <div className="app-container">
      {user ? (
        <>
          <h2>Welcome, {user.username || user.name}</h2>
          <p>Email: {user.email}</p>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>

          <h3>Your Subscriptions:</h3>
          {subscriptions.length > 0 ? (
            <ul>
              {subscriptions.map((sub) => (
                <li key={sub.id}>
                  {sub.plan.name} - Status: {sub.status} - Ends:{" "}
                  {new Date(sub.ends_at).toLocaleString()}
                </li>
              ))}
            </ul>
          ) : (
            <p>No subscriptions yet.</p>
          )}
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Dashboard;
