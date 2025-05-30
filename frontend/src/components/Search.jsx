import { React, useState } from 'react'
// import data from "./ListData.json"

export default function SearchMovies(input, movies) {
    if (!movies || !Array.isArray(movies)) {
        console.log("Movies is not an array:", movies);
        return [];
    }
    
    if (!input || input.trim() === '') {
        console.log("No input, returning all movies");
        return movies;
    }

    try {
        const filteredData = movies.filter((movie) => {
            if (!movie || !movie.title) {
                return false;
            }
            return movie.title.toLowerCase().includes(input.toLowerCase());
        });
        
        console.log("Filtered results:", filteredData.length);
        return filteredData;
    } catch (error) {
        console.error("Error in SearchMovies:", error);
        return movies; 
    }
}

export function SearchActors(input, actors) {
    if (!actors || !Array.isArray(actors)) {
        console.log("Actors is not an array:", actors);
        return [];
    }
    
    if (!input || input.trim() === '') {
        console.log("No input, returning all actors");
        return actors;
    }

    try {
        const filteredData = actors.filter((actor) => {
            if (!actor || !actor.actor_name) {
                return false;
            }
            return actor.actor_name.toLowerCase().includes(input.toLowerCase());
        });
        
        console.log("Filtered results:", filteredData.length);
        return filteredData;
    } catch (error) {
        console.error("Error in SearchActors:", error);
        return actors; 
    }
}
