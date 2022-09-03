import React, { useContext } from "react";
import StateContext from "../state/StateContext";
import { MainPageFormValuesType } from "../types/form";
import MovieSection from "./MovieSection";
import { FormikProps } from "formik"
import { MovieSectionProps } from "../types/form";

const MovieList = ({formik} : MovieSectionProps) => {
  const { state } = useContext(StateContext);

  return (
    <MovieSection title="Movie List">
       <select
        className="h-64 w-full"
        size={10}
        {...formik.getFieldProps("movieId")}
      >
        {state?.movies.map((movie, index) => (
          <option key={index}>{movie}</option>
        ))}
      </select>
    </MovieSection>
  );
};

export default MovieList;
