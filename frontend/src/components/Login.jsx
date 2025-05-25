import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(username, password);
      if (res.success) {
        onLogin(res.token, username);
        navigate("/movies");
      } else {
        setError(res.error);
      }
    } catch (error) {
      setError("Login failed");
    }
  };

  return (
    <div className="page-container">
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <h2 className="form-title">Login</h2>
          {error && <div className="error-message">{error}</div>}
          <div className="form-group">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="form-input"
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="form-input"
            />
          </div>
          <button type="submit" className="form-submit">Login</button>
        </form>
      </div>
    </div>
  );
}