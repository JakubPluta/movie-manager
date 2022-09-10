import React from "react";
import MovieSection from "./MovieSection";
import ActorSelectorList from "./ActorSelectorList";
import StateContext from "../state/StateContext";
import { useContext, useEffect, useState } from "react";
import { MovieSectionProps } from "../types/form";
import { Actions } from "../types/state";
import Loading from "./Loading";
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
        type: Actions.SetActorsAvailable,
        payload: data,
      });
      setLoading(false);
    })();
  }, [dispatch]);

  const onUpdateActor = async (id: string, selected: boolean) => {
    if (formik.values.movieId) {
      const qs = new URLSearchParams({
        movie_id: formik.values.movieId,
        actor_id: id,
      });
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URI}/movie_actor?${qs}`,
        {
          method: selected ? "POST" : "DELETE",
        }
      );
      const data = await response.json();

      if (response.ok) {
        dispatch({
          type: Actions.SetActorsSelected,
          payload: data.actors,
        });
      }
    }
  };

  return (
    <MovieSection title="Actors">
      <div className="flex h-72">
        {loading ? (
          <Loading />
        ) : (
          <ActorSelectorList title="Available">
            <select
              className="border border-green-500 w-full"
              size={10}
              name="movieActorAvailableId"
              onChange={formik.handleChange}
              onDoubleClick={() =>
                formik.values.movieActorAvailableId &&
                onUpdateActor(formik.values.movieActorAvailableId, true)
              }
              onKeyPress={(e) => {
                e.key === "Enter" &&
                  formik.values.movieActorAvailableId &&
                  onUpdateActor(formik.values.movieActorAvailableId, true);
              }}
            >
              {state?.actorsAvailable.map((actor) => (
                <option key={actor.id} value={actor.id}>
                  {actor.name}
                </option>
              ))}
            </select>
          </ActorSelectorList>
        )}


        <ActorSelectorList title="Selected">
          {state!.actorsSelected.length > 0 ? (
            <select
              className="border border-green-500 w-full"
              size={10}
              name="movieActorSelectedId"
              onChange={formik.handleChange}
              onDoubleClick={() =>
                formik.values.movieActorSelectedId &&
                onUpdateActor(formik.values.movieActorSelectedId, false)
              }
              onKeyPress={(e) => {
                e.key === "Enter" &&
                  formik.values.movieActorSelectedId &&
                  onUpdateActor(formik.values.movieActorSelectedId, false);
              }}
            >
              {state?.actorsSelected.map((actor) => (
                <option key={actor.id} value={actor.id}>
                  {actor.name}
                </option>
              ))}
            </select>
          ) : (
            <div className="border border-green-500">
              <h3 className="font-bold text-center text-lg">None</h3>
            </div>
          )}
        </ActorSelectorList>
      </div>
    </MovieSection>
  );
};

export default ActorSelector;
