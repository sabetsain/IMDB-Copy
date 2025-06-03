import { useEffect, useState, useMemo } from "react";
import { getFavouriteActors, removeFavouriteActor } from "../api";
import { SearchActors } from "../helperFun";

export default function FavoriteActors({ token, userId, input }) {
  const [favActors, setFavActors] = useState([]);
  const [error, setError] = useState("");
  const filteredActors = useMemo(() => {
    return SearchActors(input, favActors);
  }, [input, favActors]);

  useEffect(() => {
    if (!token) {
      setError("Please login to view favorite actors.");
      return;
    }

    getFavouriteActors(token, userId).then(res => {
      if (res.success === false) setError(res.error);
      else if (res.actors && res.columns) {
        const mapped = res.actors.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setFavActors(mapped);
      } else {
        setFavActors([]);
      }
    });
  }, [token, userId]);

  const handleRemove = async (actor_id) => {
    await removeFavouriteActor(token, userId, actor_id);
    setFavActors(prev => prev.filter(a => a.actor_id !== actor_id));
  };

  if (!token) return (
    <div className="page-container">
      <div className="error-message">{error}</div>
    </div>
  );

  return (
    <div className="page-container">
      <h2 className="page-title">Favorite Actors</h2>
      {error && <div className="error-message">{error}</div>}

      {filteredActors.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-title">Your Favorite actor list is empty</div>
          <div className="empty-state-message">Start adding actors to build your list!</div>
        </div>
      ) : (
        <div className="actor-list">
          {filteredActors.map(a => (
            <div key={a.actor_id} className="actor-card">
              <div className="actor-name">{a.actor_name}</div>
              <button className="btn btn-danger" onClick={() => handleRemove(a.actor_id)}>
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
