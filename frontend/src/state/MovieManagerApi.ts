import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

import {
  ActorType,
  CategoryType,
  MovieFileType,
  MovieType,
  SeriesType,
  StudioType,
} from "../types/api";
import { MovieActorAssociationType } from "../types/state";

const api = createApi({
  reducerPath: "movieManagerApi",
  tagTypes: ["actors", "categories", "movie", "movies", "series", "studios"],
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_BACKEND_URI,
  }),

  endpoints: (builder) => ({
    // fetch actors from backend
    actors: builder.query<ActorType[], void>({
      query: () => "/actors",
      providesTags: ["actors"],
    }),

    // fetch categories from backend
    categories: builder.query<CategoryType[], void>({
      query: () => "/categories",
      providesTags: ["categories"],
    }),

    // fetch movie info from backend
    movie: builder.query<MovieType, string>({
      query: (id) => `/movies/${id}`,
      providesTags: ["movie"],
    }),

    // add an actor to a movie
    movieActorAdd: builder.mutation<MovieType, MovieActorAssociationType>({
      query: ({ actorId, movieId }) => ({
        url: `/movies/movie_actor/?movie_id=${movieId}&actor_id=${actorId}`,
        method: "POST",
      }),
      invalidatesTags: ["movie", "movies"],
    }),

    // delete an actor from a movie
    movieActorDelete: builder.mutation<MovieType, MovieActorAssociationType>({
      query: ({ actorId, movieId }) => ({
        url: `/movies/movie_actor/?movie_id=${movieId}&actor_id=${actorId}`,
        method: "DELETE",
      }),
      invalidatesTags: ["movie", "movies"],
    }),

    // fetch movies from backend
    movies: builder.query<MovieFileType[], void>({
      query: () => "/movies",
      providesTags: ["movies"],
    }),

    // fetch series from backend
    series: builder.query<SeriesType[], void>({
      query: () => "/series",
      providesTags: ["series"],
    }),

    // fetch studios from backend
    studios: builder.query<StudioType[], void>({
      query: () => "/studios",
      providesTags: ["studios"],
    }),
  }),
});

export const {
  useActorsQuery,
  useCategoriesQuery,
  useMovieQuery,
  useMovieActorAddMutation,
  useMovieActorDeleteMutation,
  useMoviesQuery,
  useSeriesQuery,
  useStudiosQuery,
} = api;

export default api;
