import { useState } from "react";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import Login from "./components/Login";
import Movies from "./components/Movies";
import Actors from "./components/Actors";
import Watchlist from "./components/Watchlist";
import Register from "./components/Register";
import "./styles.css";

function Navigation({ token, userId, handleLogout }) {
  const location = useLocation();
  
  return (
    <nav className="nav">
      <div className="nav-container">
        {/* Name */}
        <Link to="/movies" className="nav-brand">
          IMDB Clone
        </Link>
        
        {/* Navigation Links */}
        <div className="nav-links">
          <Link 
            to="/movies" 
            className={location.pathname === '/movies' ? 'active' : ''}
          >
            Movies
          </Link>
          <Link 
            to="/actors"
            className={location.pathname === '/actors' ? 'active' : ''}
          >
            Actors
          </Link>
          <Link 
            to="/watchlist"
            className={location.pathname === '/watchlist' ? 'active' : ''}
          >
            Watchlist
          </Link>
          {!token && (
            <Link 
              to="/register"
              className={location.pathname === '/register' ? 'active' : ''}
            >
              Register
            </Link>
          )}
        </div>
        
        {/* User Section */}
        <div className="nav-user">
          {token ? (
            <>
              <span className="nav-welcome">👋 {userId}</span>
              <button onClick={handleLogout} className="nav-logout-btn">
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" className="nav-login-link">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [userId, setUserId] = useState(localStorage.getItem("userId") || "");

  const handleLogin = (token, username) => {
    setToken(token);
    setUserId(username);
    localStorage.setItem("token", token);
    localStorage.setItem("userId", username);
  };

  const handleLogout = () => {
    setToken("");
    setUserId("");
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
  };

  return (
    <BrowserRouter>
      <Navigation token={token} userId={userId} handleLogout={handleLogout} />
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/movies" element={<Movies token={token} userId={userId} />} />
        <Route path="/actors" element={<Actors token={token} userId={userId} />} />
        <Route path="/watchlist" element={<Watchlist token={token} userId={userId} />} />
        <Route path="*" element={<Movies token={token} userId={userId} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;