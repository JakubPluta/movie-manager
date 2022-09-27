import React from "react";
import StateContext from "../state/StateContext";
import MovieSection from "./MovieSection";
import { useContext } from "react";
import { MovieSectionProps } from "../types/form";
import { Field } from "formik";
import { useEffect, useState } from "react";
import { Actions } from "../types/state";
import Loading from "./Loading";
import { MovieInfoResponseType } from "../types/api";



const CategorySelector = ({ formik }: MovieSectionProps) => {
  const [loading, setLoading] = useState(true);
  const { state, dispatch } = useContext(StateContext);

  const onUpdateCategory = async (id: string, selected: boolean) => {
    if (formik.values.movieId) {
      const qs = new URLSearchParams({
        movie_id: formik.values.movieId,
        category_id: id,
      });

      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URI}/movies/movie_category/?${qs}`,
        {
          method: selected ? "POST" : "DELETE",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );
      const data: MovieInfoResponseType = await response.json();

      const categoryName = state?.categories.filter(
        (category) => category.id === +id
      )[0].name;

     switch (response.status) {
        case 200:
          formik.setStatus(
            `Successfully ${
              selected ? "added" : "removed"
            } category ${categoryName} ${selected ? "to" : "from"} ${data.name}`
          );
          break;

        case 404:
          formik.setStatus("Server could not find category");
          break;

        case 409:
          formik.setStatus(`Category ${categoryName} is already selected`);
          break;

        default:
          formik.setStatus("Unknown server error");
          break;
      }
    }
  };

  useEffect(() => {
    (async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URI}/categories`,
        {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        }
      );
      const data = await response.json();

      dispatch({
        type: Actions.SetCategories,
        payload: data,
      });

      // data.length > 0 && setFieldValue("movieId", data[0].id);


      setLoading(false);
    })();
  }, [dispatch]);

  return (
    <MovieSection title="Categories">
      <div className="h-72">
        {loading ? (
          <Loading />
        ) : (
          <div className="gap-1 grid grid-cols-3 overflow-y-auto">
            {state?.categories.map((category) => (
              <div key={category.id}>
                <label>
                  <Field
                    type="checkbox"
                    name="movieCategories"
                    value={category.id.toString()}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      formik.handleChange(e);
                      onUpdateCategory(e.target.value, e.target.checked);
                    }}
                  />{" "}
                  {category.name}
                </label>
              </div>
            ))}
          </div>
        )}
      </div>
    </MovieSection>
  );
};

export default CategorySelector;
