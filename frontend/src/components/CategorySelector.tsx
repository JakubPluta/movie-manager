import React from "react";
import StateContext from "../state/StateContext";
import MovieSection from "./MovieSection";
import {useContext} from "react"
const CategorySelector = () => {
  const {state} = useContext(StateContext)
  return (
    <MovieSection title="Categories">
      <div className="gap-1 grid grid-cols-3 overflow-y-auto">
        {state?.categories.map((category, index) => (<div key={index}><label><input className="mx-1" type="checkbox" />{ category }</label> </div>))}
      </div>
    </MovieSection>
  );
};

export default CategorySelector;
