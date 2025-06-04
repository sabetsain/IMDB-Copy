import { useEffect, useState, useMemo } from "react";
import { getActors, getFavouriteActors, addFavouriteActor, removeFavouriteActor } from "../api";
import { SearchActors } from "../helperFun";

export default function Actors({ token, userId, input }) {
  const [actors, setActors] = useState([]);
  const [favActorIds, setFavActorIds] = useState(new Set());
  const [error, setError] = useState("");

  const filteredActors = useMemo(() => {
    return SearchActors(input, actors);
  }, [input, actors]);

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
      }
    });

    getFavouriteActors(token, userId).then(res => {
      if (res.success === false) setError(res.error);
      else if (res.actors && res.columns) {
        const favIds = new Set(res.actors.map(row => row[0])); // actor_id assumed at index 0
        setFavActorIds(favIds);
      }
    });
  }, [token, userId]);

  const handleAddFavorite = async (actor_id) => {
    await addFavouriteActor(token, userId, actor_id);
    setFavActorIds(prev => new Set(prev).add(actor_id));
  };

  const handleRemoveFavorite = async (actor_id) => {
    await removeFavouriteActor(token, userId, actor_id);
    setFavActorIds(prev => {
      const copy = new Set(prev);
      copy.delete(actor_id);
      return copy;
    });
  };

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
        {filteredActors.map(a => (
          <div key={a.actor_id} className="actor-card">
            <div className="actor-name">{a.actor_name}</div>
            {favActorIds.has(a.actor_id) ? (
              <button className="btn btn-danger" onClick={() => handleRemoveFavorite(a.actor_id)}>
                Remove from Favorites
              </button>
            ) : (
              <button className="btn btn-primary" onClick={() => handleAddFavorite(a.actor_id)}>
                Add to Favorites
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
