import React, { useContext, useState } from "react";
import MovieList from "../components/MovieList";
import MovieData from "../components/MovieData";
import ActorSelector from "../components/ActorSelector";
import CategorySelector from "../components/CategorySelector";
import StateContext from "../state/StateContext";

const MainPage = () => {
  const { state } = useContext(StateContext);
  console.log(state);
  return (
    <>
      <div className="lg:flex">
        <div className="m-2 lg:w-3/5">
          <MovieList />
        </div>
        <div className="m-2 lg:w-2/5">
          <MovieData />
        </div>
      </div>
      <div className="lg:flex">
        <div className="m-2 lg:w-1/2">
          <ActorSelector />
        </div>
        <div className="m-2 lg:w-1/2">
          <CategorySelector />
        </div>
      </div>
    </>
  );
};

export default MainPage;
