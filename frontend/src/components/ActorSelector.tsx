import React from "react";
import MovieSection from "./MovieSection";
import ActorSelectorList from "./ActorSelectorList";
import StateContext from "../state/StateContext";
import { useContext, useEffect, useState } from "react";
import { MovieSectionProps } from "../types/form";
import { Actions } from "../types/state";
const ActorSelector = ({ formik }: MovieSectionProps) => {
  const { state, dispatch } = useContext(StateContext);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URI}/actors`
      );
      const data = await response.json();

      dispatch({
        type: Actions.SetAvailableActors,
        payload: data,
      });
      setLoading(false);
    })();
  }, [dispatch]);

  return (
    <MovieSection title="Actors">
      <div className="flex h-72">
        <ActorSelectorList title="Available">
          <select
            className="border border-green-500 w-full"
            size={10}
            {...formik.getFieldProps("movieActorAvailableId")}
          >
            {state?.actors.map((actor) => (
              <option key={actor.id} value={actor.id}>
                {actor.name}
              </option>
            ))}
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
