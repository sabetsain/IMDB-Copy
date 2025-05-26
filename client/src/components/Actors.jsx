import { useEffect, useState } from "react";
import { getActors } from "../api";

export default function Actors({ token }) {
  const [actors, setActors] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      setError("Please login to view actors.");
      return;
    }
    getActors(token).then(res => {
      if (res.success === false) setError(res.error);
      else if (res.actors && res.columns) {
        const mapped = res.actors.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setActors(mapped);
      } else {
        setActors([]);
      }
    });
  }, [token]);

  if (!token) return (
    <div className="page-container">
      <div className="error-message">{error}</div>
    </div>
  );

  return (
    <div className="page-container">
      <h2 className="page-title">Actors</h2>
      {error && <div className="error-message">{error}</div>}
      <div className="actor-list">
        {actors.map(a => (
          <div key={a.actor_id} className="actor-card">
            <div className="actor-name">{a.actor_name}</div>
          </div>
        ))}
      </div>
    </div>
  );
}