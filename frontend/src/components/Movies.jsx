import { round} from "mathjs";
import { useEffect, useState, useCallback, useMemo } from "react";
import { getMovies, getWatchlist, addToWatchlist, 
        removeFromWatchlist, addRating, changeRating, 
        deleteRating, getUserRating} from "../api";
import { formatVotes, SearchMovies } from "../helperFun";

export default function Movies({ token, userId, input}) {
  const [allMovies, setAllMovies] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const MOVIES_PER_PAGE = 20; 

  const filteredMovies = useMemo(() => {
    return SearchMovies(input, allMovies);
  }, [input, allMovies]);

  const paginatedMovies = useMemo(() => {
    const endIndex = currentPage * MOVIES_PER_PAGE;
    return filteredMovies.slice(0, endIndex);
  }, [filteredMovies, currentPage]);
  // Fetch all movies once
  useEffect(() => {
    if (!token) {
      setError("Please login or register to view movies.");
      return;
    }
    
    setLoading(true);
    getMovies(token).then(result => {
      if (result.success === false) setError(result.error);
      else if (result.movies && result.columns) {
        const mapped = result.movies.map(row =>
          Object.fromEntries(result.columns.map((col, i) => [col, row[i]]))
        ).sort((a, b) => a.movie_id - b.movie_id);
        setAllMovies(mapped);
        
        // Load first batch
        setHasMore(mapped.length > MOVIES_PER_PAGE);
        
        fetchUserRatings();
      } else {
        setAllMovies([]);
      }
      setLoading(false);
    });
  }, [token]);

  // Fetch watchlist
  useEffect(() => {
    if (!token || !userId) return;
    getWatchlist(token, userId).then(result => {
      if (result.success === false) setWatchlist([]);
      else setWatchlist(result.movies ? result.movies.map(m => m[0]) : []);
    });
  }, [token, userId]);
  useEffect(() => {
    setCurrentPage(1);
    setHasMore(filteredMovies.length > MOVIES_PER_PAGE);
  }, [input, filteredMovies.length]);

  // Load more movies when scrolling
  const loadMoreMovies = useCallback(() => {
    if (loading || !hasMore) return;

    const nextPage = currentPage + 1;
    const endIndex = nextPage * MOVIES_PER_PAGE;

    setCurrentPage(nextPage);
    setHasMore(endIndex < filteredMovies.length);
  }, [currentPage, filteredMovies.length, loading, hasMore]);

  // Infinite scroll detection
  useEffect(() => {
    const handleScroll = () => {
      if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight) {
        return;
      }
      loadMoreMovies();
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loadMoreMovies]);

  const fetchUserRatings = async () => {
    try {
      const result = await getUserRating(token, userId);
      const ratings = {};
      if (result.ratings) {
        result.ratings.forEach(([movie_id, rating]) => {
          ratings[movie_id] = rating / 2;
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
    } catch (error) {
      console.error("Failed to remove rating:", error);
    }
  };

  const handleAdd = async (movie_id) => {
    await addToWatchlist(token, userId, movie_id);
    setWatchlist(prev => [...prev, movie_id]);
  };

  const handleRemove = async (movie_id) => {
    await removeFromWatchlist(token, userId, movie_id);
    setWatchlist(prev => prev.filter(id => id !== movie_id));
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
      <h2 className="page-title">Movies</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="movies-stats">
        {/* Showing {filteredMovies.length} of {allMovies.length} movies */}
        Showing { paginatedMovies.length} of {filteredMovies.length} movies
      </div>

      {filteredMovies.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-title">No movies found</div>
          <div className="empty-state-message">Try a different search keyword.</div>
        </div>
      ) : (
        <div className="content-list">
        {/* {filteredMovies.map(m => ( */}
        {paginatedMovies.map(m => (
          <div key={m.movie_id} className="movie-card">
            <img 
              src={m.poster_url} 
              alt={m.title} 
              className="movie-poster"
              loading="lazy" // Lazy load images
            />
            <div className="movie-info">
              <div className="movie-title">{m.title} ({m.year})</div>
              <div className="movie-detail"><strong>Director:</strong> {m.director}</div>
              <div className="movie-detail"><strong>Genre:</strong> {m.genre}</div>
              <div className="movie-detail"><strong>Runtime:</strong> {m.run_time} min</div>
              <div className="movie-detail"><strong>IMDB:</strong> {round((m.imdb_rating/ 2),1)} ({formatVotes(m.num_votes)} votes)</div>
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

      {/* Loading indicator */}
      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading movies...</p>
        </div>
      )}

      {/* Load more button (fallback for infinite scroll) */}
      {!loading && hasMore && filteredMovies.length >= 20 && (
        <div className="load-more-container">
          <button onClick={loadMoreMovies} className="btn btn-primary load-more-btn">
            Load More Movies
          </button>
        </div>
      )}

      {/* End of list indicator */}
      {!hasMore && paginatedMovies.length > 0 && (
        <div className="end-of-list">
          <p>You've seen all movies!</p>
        </div>
      )}
    </div>
  );
}