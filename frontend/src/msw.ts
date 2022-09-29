import { rest } from "msw";
import { setupServer } from "msw/node";

// creates full URL to endpoint with base URL defined in REACT_APP_BACKEND
const backend = (path: string) =>
  new URL(path, process.env.REACT_APP_BACKEND_URI).toString();

// mock server endpoints
const endpoints = [
  rest.get(backend("/actors"), (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.json([
        {
          id: 1,
          name: "Angelina Jolie",
          },
                {
          id: 2,
          name: "Christian Bale",
        },
        {
          id: 3,
          name: "Arnold Schwarzenegger",
        },
      ])
    );
  }),
  rest.get(backend("/categories"), (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.json([
        {
          id: 1,
          name: "action",
        },
        {
          id: 2,
          name: "comedy",
        },
        {
          id: 3,
          name: "fantasy",
          },
                {
          id: 4,
          name: "sf",
        },
      ])
    );
  }),
  rest.get(backend("/movies"), (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.json([
        {
          id: 1,
          filename: "Diuna.mp4",
        },
        {
          id: 2,
          filename: "Forest Gump.mp4",
        },
        {
          id: 3,
          filename: "7even.mp4",
        },
      ])
    );
  }),
  rest.get(backend("/series"), (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.json([
        {
          id: 1,
          name: "Lord of the Rings",
        },
        {
          id: 2,
          name: "Batman",
        },
      ])
    );
  }),
  rest.get(backend("/studios"), (req, res, ctx) => {
    return res(
      ctx.delay(150),
      ctx.json([
        {
          id: 1,
          name: "Universal Pictures",
        },
        {
          id: 2,
          name: "BBC Films",
        },
        {
          id: 3,
          name: "Fox Movies",
        },
      ])
    );
  }),
];

// create the msw mock server endpoints
export const server = setupServer(...endpoints);
