import { round } from "mathjs";
import { useEffect, useState, useMemo } from "react";
import { getRatedMovies, addToWatchlist, removeFromWatchlist, addRating, changeRating, deleteRating, getUserRating, formatVotes, getWatchlist } from "../api";
import SearchMovies from "./Search";

export default function Watchlist({ token, userId, input }) {
  const [ratedMovies, setRatedMovies] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [watchlist, setWatchlist] = useState([]);
  const [error, setError] = useState("");

  const filteredMovies = useMemo(() => {
    return SearchMovies(input, ratedMovies);
  }, [input, ratedMovies]);

  useEffect(() => {
    if (!token || !userId) {
      setError("Please login to view your rated movies.");
      return;
    }

    getRatedMovies(token, userId).then(res => {
      if (res.success === false) {
        setError(res.error);
      } else if (res.movies && res.columns) {
        const mapped = res.movies.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setRatedMovies(mapped);
      } else {
        setRatedMovies([]);
      }
    });

    fetchUserRatings();
    fetchWatchlist();
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

  const fetchWatchlist = async () => {
    try {
      const res = await getWatchlist(token, userId);
      if (res.movies && res.columns) {
        const mapped = res.movies.map(row =>
          Object.fromEntries(res.columns.map((col, i) => [col, row[i]]))
        );
        setWatchlist(mapped);
      } else {
        setWatchlist([]);
      }
    } catch (error) {
      setWatchlist([]);
    }
  };

  const handleAdd = async (movie_id) => {
    await addToWatchlist(token, userId, movie_id);
    fetchWatchlist();
  };

  const handleRemove = async (movie_id) => {
    await removeFromWatchlist(token, userId, movie_id);
    fetchWatchlist();
  };

  const handleRating = async (movie_id, rating) => {
    const currentRating = userRatings[movie_id];
    try {
      if (currentRating) {
        await changeRating(token, userId, movie_id, rating * 2);
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
      setRatedMovies(prev => prev.filter(m => m.movie_id !== movie_id));
    } catch (error) {
      console.error("Failed to remove rating:", error);
    }
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
      <h2 className="page-title">Movies You've Rated</h2>
      {error && <div className="error-message">{error}</div>}
      {filteredMovies.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-title">You have not rated any movies yet.</div>
          <div className="empty-state-message">Start rating movies to see them here!</div>
        </div>
      ) : (
        <div className="content-list">
          {filteredMovies.map(m => (
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
                {watchlist.includes(m.movie_id) ? (
                  <button onClick={() => handleRemove(m.movie_id)} className="btn btn-danger">
                    Remove from Watchlist
                  </button>
                ) : (
                  <button onClick={() => handleAdd(m.movie_id)} className="btn btn-primary">
                    Add to Watchlist
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}