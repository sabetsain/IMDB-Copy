import { React, useState } from 'react'
// import data from "./ListData.json"

export default function SearchMovies(input, movies) {
    if (!movies || !Array.isArray(movies)) return [];
    if (!input || input.trim() === '') return movies;

    const lowerInput = input.toLowerCase();

    return movies.filter(movie =>
        movie?.title?.toLowerCase().includes(lowerInput)
    );
}

export function SearchActors(input, actors) {
    if (!actors || !Array.isArray(actors)) return [];
    if (!input || input.trim() === '') return actors;

    const lowerInput = input.toLowerCase();

    return actors.filter(actor =>
        actor?.actor_name?.toLowerCase().includes(lowerInput)
    );
}
