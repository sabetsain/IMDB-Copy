const API_URL = "http://127.0.0.1:5000/api";
// const API_URL = "http://127.0.0.1:5001/api";
import { round } from "mathjs";

export function formatVotes(num) {
  if (num >= 1000000) {
    return round((num / 1000000),1) + "M";
  }
  
  if (num >= 1000) {
    if (num >= 10000) {
      return Math.floor(num / 1000) + "K";
    } else {
      return round((num / 1000),1) + "K";
    }
  }
  
  return num.toString();
}
export async function login(username, password) {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.json();
}

export async function getMovies(token) {
  const res = await fetch(`${API_URL}/movies`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function getWatchlist(token, userId) {
  const res = await fetch(`${API_URL}/watchlist/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}
export async function getRatedMovies(token, userId) {
  const res = await fetch(`${API_URL}/rated_movies/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function addToWatchlist(token, userId, movie_id) {
  const res = await fetch(`${API_URL}/add_to_watchlist`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, movie_id }),
  });
  return res.json();
}

export async function removeFromWatchlist(token, userId, movie_id) {
  const res = await fetch(`${API_URL}/remove_from_watchlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ user_id: userId, movie_id }),
  });
  return res.json();
}

export async function getActors(token) {
  const res = await fetch(`${API_URL}/actors`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function register(username, password) {
  const res = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return res.json();
}

// Rating functions
export async function addRating(token, userId, movie_id, rating) {
  const res = await fetch(`${API_URL}/add_rating`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, movie_id, rating }),
  });
  return res.json();
}

export async function changeRating(token, userId, movie_id, rating) {
  const res = await fetch(`${API_URL}/change_rating`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, movie_id, rating }),
  });
  return res.json();
}

export async function deleteRating(token, userId, movie_id) {
  const res = await fetch(`${API_URL}/delete_rating`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, movie_id }),
  });
  return res.json();
}

export async function getUserRating(token, userId, movie_id = null) {
  const res = await fetch(`${API_URL}/rating/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  
  if (movie_id) {
    // Find rating for specific movie
    const rating = data.ratings?.find(r => r[0] === movie_id);
    return rating ? { rating: rating[1] } : {};
  } else {
    // Return all ratings
    return data;
  }
}
export async function getFavouriteActors(token, userId) {
  const res = await fetch(`${API_URL}/favourite_actor/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function addFavouriteActor(token, userId, actor_id) {
  const res = await fetch(`${API_URL}/add_favourite_actor`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, actor_id }),
  });
  return res.json();
}

export async function removeFavouriteActor(token, userId, actor_id) {
  const res = await fetch(`${API_URL}/remove_favourite_actor`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ user_id: userId, actor_id }),
  });
  return res.json();
}