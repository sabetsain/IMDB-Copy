import { useState } from "react";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import InputBase from '@mui/material/InputBase';
import Paper from '@mui/material/Paper';
import Login from "./components/Login";
import Movies from "./components/Movies";
import Actors from "./components/Actors";
import Watchlist from "./components/Watchlist";
import Register from "./components/Register";
import Rated from "./components/Rated";
import FavoriteActors from "./components/Favorite_Actors";
import "./styles.css";


function Navigation({ token, userId, handleLogout }) {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="nav">
      <div className="nav-container">
        {/* Name */}
        <Link to="/movies" className="nav-brand">
          IMDB Clone
        </Link>
        
        {/* Navigation Links */}
        <div className="nav-links">
          {/* <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400 }}
          >
              <InputBase
                id="outlined-basic"
                sx={{ ml: 1, flex: 1 }}
                placeholder="Search..."
                inputProps={{ 'aria-label': 'search' }}
                onChange={inputHandler}
              />
          </Paper> */}
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
        <div className="nav-user" style={{ position: "relative" }}>
          {token ? (
            <>
              <button
                className="nav-user-button"
                onClick={() => setMenuOpen((open) => !open)}
                aria-haspopup="true"
                aria-expanded={menuOpen}
              >
                👋 {userId} ▼
              </button>
              {menuOpen && (
                <div
                  className="nav-user-menu"
                  style={{
                    position: "absolute",
                    left: 0,
                    top: "100%",
                    marginTop: "5px",
                    minWidth: "160px",
                  }}
                >
                  <Link
                    to="/favourite_actor"
                    className="nav-user-menu-item"
                    onClick={() => setMenuOpen(false)}
                  >
                    Favourite Actors
                  </Link>
                  <Link
                    to="/watchlist"
                    className="nav-user-menu-item"
                    onClick={() => setMenuOpen(false)}
                  >
                    Watchlist
                  </Link>
                  <Link
                    to="/rated_movies"
                    className="nav-user-menu-item"
                    onClick={() => setMenuOpen(false)}
                  >
                    Rated Movies
                  </Link>
                </div>
              )}
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
  const [inputText, setInputText] = useState("");

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

  let inputHandler = (e) => {
    //convert input text to lower case
    var lowerCase = e.target.value.toLowerCase();
    setInputText(lowerCase);
  };

  return (
    <BrowserRouter>
      <Navigation token={token} userId={userId} handleLogout={handleLogout} />
      <div style={{ display: "flex", justifyContent: "center", margin: "20px 0" }}>
        <Paper
          component="form"
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400 }}
        >
          <InputBase
            id="outlined-basic"
            sx={{ ml: 1, flex: 1 }}
            placeholder="Search..."
            inputProps={{ 'aria-label': 'search' }}
            onChange={inputHandler}
          />
        </Paper>
      </div>
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/movies" element={<Movies token={token} userId={userId} input={inputText} />} />
        <Route path="/actors" element={<Actors token={token} userId={userId} input={inputText} />} />
        <Route path="/watchlist" element={<Watchlist token={token} userId={userId} input={inputText} />} />
        <Route path="/rated_movies" element={<Rated token={token} userId={userId} input={inputText} />} />
        <Route path="/favourite_actor" element={<FavoriteActors token={token} userId={userId} input={inputText} />} />
        <Route path="*" element={<Movies token={token} userId={userId} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;