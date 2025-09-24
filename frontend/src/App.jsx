// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Nav from "./components/Nav";
 import Login from "./Pages/Login";
import Dashboard from "./Pages/Dashboard";
import Plans from "./Pages/Plans";
import Subscriptions from "./Pages/Subscriptions";
import "./App.css";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-800">
        <Nav />
        <div className="p-6">
          <Routes>
            <Route path="/" element={<Login />} /> {/* ✅ Login as default */}
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/plans" element={<Plans />} />
            <Route path="/subscriptions" element={<Subscriptions />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
