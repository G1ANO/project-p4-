import { Link } from "react-router-dom";

export default function Nav() {
  return (
    <nav className="nav">
      <h1 className="nav-logo"></h1>
      <div className="nav-links">
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/plans">Plans</Link>
        <Link to="/subscriptions">Subscriptions</Link>
      </div>
    </nav>
  );
}
