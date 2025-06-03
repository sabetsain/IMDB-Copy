import { useState } from "react";
import { register } from "../api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await register(username, password);
      if (res.success) {
        setSuccess("Registration successful! You can now login.");
        setError("");
        setUsername("");
        setPassword("");
      } else {
        setError(res.error);
        setSuccess("");
      }
    } catch (error) {
      setError("Registration failed");
      setSuccess("");
    }
  };

  return (
    <div className="page-container">
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <h2 className="form-title">Register</h2>
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}
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
          <button type="submit" className="form-submit">Register</button>
        </form>
      </div>
    </div>
  );
}