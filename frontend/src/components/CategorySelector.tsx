import React from "react";
import StateContext from "../state/StateContext";
import MovieSection from "./MovieSection";
import { useContext } from "react";
import { MovieSectionProps } from "../types/form";
import { Field } from "formik";

const CategorySelector = ({ formik }: MovieSectionProps) => {
  const { state } = useContext(StateContext);
  return (
    <MovieSection title="Categories">
      <div className="gap-1 grid grid-cols-3 overflow-y-auto">
        {state?.categories.map((category, index) => (
          <div key={category.id}>
            {" "}
            <label>
              <Field
                type="checkbox"
                name="movieCategories"
                value={index.toString()}
              />{" "}
              {category.name}
            </label>{" "}
          </div>
        ))}
      </div>
    </MovieSection>
  );
};

export default CategorySelector;
