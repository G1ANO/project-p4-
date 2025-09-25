import { useEffect, useState } from "react";

export default function Dashboard() {
  const [dashboard, setDashboard] = useState([]);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem("user"));
    if (!storedUser) return;
    setUser(storedUser);

    fetch(`http://localhost:5000/dashboard/${storedUser.id}`)
      .then((res) => res.json())
      .then((data) => setDashboard(data));
  }, []);

  return (
    <div className="dashboard-page">
      <h1>{user ? `${user.username}'s Dashboard` : "Dashboard"}</h1>
      {dashboard.length === 0 ? (
        <p>No subscriptions found.</p>
      ) : (
        <ul className="dashboard-list">
          {dashboard.map((item) => (
            <li key={item.id} className="dashboard-item">
              <p>Status: {item.status}</p>
              <p>Ends at: {new Date(item.ends_at).toLocaleString()}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
