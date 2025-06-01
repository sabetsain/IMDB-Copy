import { round } from "mathjs";
import { useEffect, useState, useMemo } from "react";
import { getWatchlist, removeFromWatchlist, addRating, changeRating, deleteRating, getUserRating, formatVotes } from "../api";
import SearchMovies from "./Search";
import SearchMovies from "./Search";

export default function Watchlist({ token, userId, input }) {
export default function Watchlist({ token, userId, input }) {
  const [watchlist, setWatchlist] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [error, setError] = useState("");

  const filteredMovies = useMemo(() => {
    return SearchMovies(input, watchlist);
  }, [input, watchlist]);

  useEffect(() => {
    if (!token || !userId) {
      setError("Please login to view your watchlist.");
      return;
    }
    
    getWatchlist(token, userId).then(res => {
      if (res.success === false) setError(res.error);
      else if (res.movies && res.columns) {
        const mapped = res.movies.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setWatchlist(mapped);
        fetchUserRatings();
      } else {
        setWatchlist([]);
      }
    });
  }, [token, userId]);

  const fetchUserRatings = async () => {
    try {
      const res = await getUserRating(token, userId);
      const ratings = {};
      if (res.ratings) {
        res.ratings.forEach(([movie_id, rating]) => {
          ratings[movie_id] = rating;
        });
      }
      setUserRatings(ratings);
    } catch (error) {
      console.log("Failed to fetch user ratings:", error);
    }
  };

  const handleRating = async (movie_id, rating) => {
    const currentRating = userRatings[movie_id];
    try {
      if (currentRating) {
        await changeRating(token, userId, movie_id, rating);
      } else {
        await addRating(token, userId, movie_id, rating * 2);
      }
      setUserRatings(prev => ({ ...prev, [movie_id]: rating }));
    } catch (error) {
      console.error("Failed to rate movie:", error);
    }
  };

  const handleRemoveRating = async (movie_id) => {
    try {
      await deleteRating(token, userId, movie_id);
      setUserRatings(prev => {
        const newRatings = { ...prev };
        delete newRatings[movie_id];
        return newRatings;
      });
    } catch (error) {
      console.error("Failed to remove rating:", error);
    }
  };

  const handleRemove = async (movie_id) => {
    await removeFromWatchlist(token, userId, movie_id);
    getWatchlist(token, userId).then(res => {
      if (res.movies && res.columns) {
        const mapped = res.movies.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setWatchlist(mapped);
      } else {
        setWatchlist([]);
      }
    });
  };

  const StarRating = ({ movie_id, currentRating }) => {
    const [hoverRating, setHoverRating] = useState(undefined);

    return (
      <div className="star-rating">
        <span className="star-rating-label">Your Rating:</span>
        {[1, 2, 3, 4, 5].map(star => (
          <span
            key={star}
            onClick={() => handleRating(movie_id, star)}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            className={`star ${
              star <= (hoverRating || currentRating) ? 'star-filled' : 'star-empty'
            }`}
          >
            ★
          </span>
        ))}
        {currentRating && (
          <button 
            onClick={() => handleRemoveRating(movie_id)}
            className="btn btn-secondary btn-small"
          >
            Remove Rating
          </button>
        )}
      </div>
    );
  };

  if (!token) return (
    <div className="page-container">
      <div className="error-message">{error}</div>
    </div>
  );

  return (
    <div className="page-container">
      <h2 className="page-title">My Watchlist</h2>
      {error && <div className="error-message">{error}</div>}

      {filteredMovies.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-title">Your watchlist is empty</div>
          <div className="empty-state-message">Start adding movies to build your watchlist!</div>
        </div>
      ) : (
        <div className="content-list">
          {filteredMovies.map((m) => (
            <div key={m.movie_id} className="movie-card">
              <img src={m.poster_url} alt={m.title} className="movie-poster" />
              <div className="movie-info">
                <div className="movie-title">{m.title} ({m.year})</div>
                <div className="movie-detail"><strong>Director:</strong> {m.director}</div>
                <div className="movie-detail"><strong>Genre:</strong> {m.genre}</div>
                <div className="movie-detail"><strong>Runtime:</strong> {m.run_time} min</div>
                <div className="movie-detail"><strong>IMDB:</strong> {round((m.imdb_rating/2),1)} ({formatVotes(m.num_votes)} votes)</div>
                <StarRating movie_id={m.movie_id} currentRating={userRatings[m.movie_id]} />
              </div>
              <div className="movie-actions">
                <button onClick={() => handleRemove(m.movie_id)} className="btn btn-danger">
                  Remove from Watchlist
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}