import { useContext, useEffect, useState } from "react";

import Loading from "./Loading";
import MovieSection from "./MovieSection";

import StateContext from "../state/StateContext";

import { MovieInfoResponseType } from "../types/api";
import { MovieSectionProps } from "../types/form";
import { Actions } from "../types/state";

const MovieList = ({ formik }: MovieSectionProps) => {
  const [loading, setLoading] = useState(true);
  const { state, dispatch } = useContext(StateContext);

  useEffect(() => {
    (async () => {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URI}/movies`);
      const data = await response.json();

      dispatch({
        type: Actions.SetMovies,
        payload: data,
      });

      setLoading(false);
    })();
  }, [dispatch]);

  useEffect(() => {
    (async () => {
      if (formik.values.movieId) {
        const id = +formik.values.movieId;

        const response = await fetch(
          `${process.env.REACT_APP_BACKEND_URI}/movies/${id}`
        );
        const data: MovieInfoResponseType = await response.json();
        console.log(data)
        if (response.ok) {

          formik.setValues({
            ...formik.values,
            movieName: data.name ?? "",
            movieSeriesId: data.series ? data.series.id.toString() : "",
            movieSeriesNumber: data.series_number
              ? data.series_number.toString()
              : "",
            movieStudioId: data.studio ? data.studio.id.toString() : "",
            movieCategories: data.categories.map((category) =>
              category.id.toString()
            ),
          });

          dispatch({
            type: Actions.SetActorsSelected,
            payload: data.actors,
          });
        }
      }
    })();
  }, [dispatch, formik.values.movieId]);

  return (
    <MovieSection title="Movie List">
      {loading ? (
        <div className="h-64">
          <Loading />
        </div>
      ) : (
        <select
          className="h-64 w-full"
          size={10}
          name="movieId"
          onChange={formik.handleChange}
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