import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Nav from "./components/Nav";
import Login from "./Pages/Login";
import Dashboard from "./Pages/Dashboard";
import Plans from "./Pages/Plans";
import Subscriptions from "./Pages/Subscriptions";
import Signup from "./Pages/Signup";
import "./App.css";

function ProtectedRoute({ children }) {
  const user = localStorage.getItem("user");
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* ✅ Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/plans"
          element={
            <ProtectedRoute>
              <Plans />
            </ProtectedRoute>
          }
        />
        <Route
          path="/subscriptions"
          element={
            <ProtectedRoute>
              <Subscriptions />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
