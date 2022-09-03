import React from "react";
import MovieSection from "./MovieSection";
import ActorSelectorList from "./ActorSelectorList";
import StateContext from "../state/StateContext";
import { useContext } from "react";
import { MovieSectionProps } from "../types/form";

const ActorSelector = ({formik}: MovieSectionProps) => {

  const {state} = useContext(StateContext)
  return (
    <MovieSection title="Actors">
      <div className="flex h-72">
        <ActorSelectorList title="Available">
           <select
            className="border border-green-500 w-full"
            size={10}
            {...formik.getFieldProps("movieActorAvailableId")}
          >
            {state?.actors.map((actor, index) => (<option key={index}>{ actor}</option>))}
          </select>
        </ActorSelectorList>

        <ActorSelectorList title="Selected">
                   <select
            className="border border-green-500 w-full"
            size={10}
            {...formik.getFieldProps("movieActorSelectedId")}
          >
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