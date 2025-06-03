import { round } from "mathjs";

export function formatVotes(num) {
  if (num >= 1000000) { // Format numbers in millions
    return round((num / 1000000),1) + "M"; 
  }
  
  if (num >= 1000) { // Format numbers in thousands
    if (num >= 10000) {
      return Math.floor(num / 1000) + "K";
    } else {
      return round((num / 1000),1) + "K";
    }
  }
  
  return num.toString();
}

// function to search movies by title
export function SearchMovies(input, movies) { 
    if (!movies || !Array.isArray(movies)) return []; // Check if movies is an array
    if (!input || input.trim() === '') return movies; // If input is empty, return all movies

    const lowerInput = input.toLowerCase();

    // Filter movies based on title
    return movies.filter(movie =>
        movie?.title?.toLowerCase().includes(lowerInput)
    );
}

// function to search actors by name
export function SearchActors(input, actors) {
    if (!actors || !Array.isArray(actors)) return [];
    if (!input || input.trim() === '') return actors;

    const lowerInput = input.toLowerCase();
    
    // Filter actors based on actor_name
    return actors.filter(actor =>
        actor?.actor_name?.toLowerCase().includes(lowerInput)
    );
}