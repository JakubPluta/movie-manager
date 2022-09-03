import React, { useContext } from "react";
import StateContext from "../state/StateContext";
import MovieSection from "./MovieSection";

const MovieList = () => {
  const { state } = useContext(StateContext);

  return (
    <MovieSection title="Movie List">
      <select className="h-64 w-full" size={10}>
        {state?.movies.map((movie, index) => (
          <option key={index}>{movie}</option>
        ))}
      </select>
    </MovieSection>
  );
};

export default MovieList;
