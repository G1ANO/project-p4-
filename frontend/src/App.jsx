import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Nav from "./components/Nav";
import Login from "./Pages/Login";
import Dashboard from "./Pages/Dashboard";
import Plans from "./Pages/Plans";
import Subscriptions from "./Pages/Subscriptions";
import Signup from "./Pages/Signup";
import "./App.css";

function App() {
  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/plans" element={<Plans />} />
        <Route path="/subscriptions" element={<Subscriptions />} />
      </Routes>
    </Router>
  );
}

export default App;
