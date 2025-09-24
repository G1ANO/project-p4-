import { Link } from "react-router-dom";

export default function Nav() {
  return (
    <nav className="nav">
      <Link to="/">Login</Link>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/plans">Plans</Link>
      <Link to="/subscriptions">Subscriptions</Link>
    </nav>
  );
}
