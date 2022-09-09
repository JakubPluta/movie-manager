export interface StateType {
  actors: ActorType[];
  categories: CategoryType[];
  series: SeriesType[];
  studios: StudioType[];
  movies: MovieFileType[];
}

export interface MovieFileType {
  id: number;
  filename: string;
}

export interface MovieDataBaseType {
  id: number;
  name: string;
}

export interface ActorType extends MovieDataBaseType {}
export interface CategoryType extends MovieDataBaseType {}
export interface SeriesType extends MovieDataBaseType {}
export interface StudioType extends MovieDataBaseType {}

export type ActionType =
  | SetAvailableActorsAction
  | SetCategoriesAction
  | SetMoviesAction
  | SetSeriesAction
  | SetStudiosAction;

export enum Actions {
  SetAvailableActors,
  SetCategories,
  SetMovies,
  SetSeries,
  SetStudios,
}

export interface SetAvailableActorsAction {
  type: Actions.SetAvailableActors;
  payload: ActorType[];
}

export interface SetCategoriesAction {
  type: Actions.SetCategories;
  payload: CategoryType[];
}
export interface SetMoviesAction {
  type: Actions.SetMovies;
  payload: MovieFileType[];
}

export interface SetSeriesAction {
  type: Actions.SetSeries;
  payload: SeriesType[];
}

export interface SetStudiosAction {
  type: Actions.SetStudios;
  payload: StudioType[];
}
