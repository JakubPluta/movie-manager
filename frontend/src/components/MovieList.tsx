import React, { useContext, useEffect, useState } from "react";
import StateContext from "../state/StateContext";
import { MainPageFormValuesType } from "../types/form";
import MovieSection from "./MovieSection";
import { FormikProps } from "formik";
import { MovieSectionProps } from "../types/form";
import { Actions } from "../types/state";

const MovieList = ({ formik }: MovieSectionProps) => {
  const [loading, setLoading] = useState(true);
  const { state, dispatch } = useContext(StateContext);

  useEffect(() => {
    (async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URI}/movies`
      );
      const data = await response.json();
      dispatch({
        type: Actions.SetMovies,
        payload: data,
      });

      // await new Promise((resolve) => setTimeout(resolve, 300));

      setLoading(false);
    })();
  }, []);

  return (
    <MovieSection title="Movie List">
      {loading ? (
        <h2>Loading....</h2>
      ) : (
        <select
          className="h-64 w-full"
          size={10}
          {...formik.getFieldProps("movieId")}
        >
          {state?.movies.map((movie) => (
            <option key={movie.id} value={movie.id}>
              {movie.filename}
            </option>
          ))}
        </select>
      )}
    </MovieSection>
  );
};

export default MovieList;
