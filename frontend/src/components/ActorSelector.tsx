import React from "react";
import MovieSection from "./MovieSection";
import ActorSelectorList from "./ActorSelectorList";

const ActorSelector = () => {
  return (
    <MovieSection title="Actors">
      <div className="flex h-96">
        <ActorSelectorList title="Available">
          <select className="border border-green-500 w-full" size={13}>
            <option>Actor 1</option>
            <option>Actor 2</option>
            <option>Actor 3</option>
            <option>Actor 4</option>
            <option>Actor 5</option>
          </select>
        </ActorSelectorList>

        <ActorSelectorList title="Selected">
          <select className="border border-green-500 w-full" size={13}>
            <option>Selected 1</option>
            <option>Selected 12</option>
            <option>Selected 2</option>
            <option>Selected 3</option>
            <option>Selected 4</option>
            <option>Selected 5</option>
          </select>
        </ActorSelectorList>
      </div>
    </MovieSection>
  );
};

export default ActorSelector;
