import { Actions, ActionType, StateType } from "../types/state";

export default (state: StateType, action: ActionType) => {
  switch (action.type) {
    case Actions.AddActor: return {
      ...state,
      actors: [...state.actors, action.payload]
    }

        case Actions.AddCategory: return {
      ...state,
      categories: [...state.categories, action.payload]
    }

            case Actions.AddSeries: return {
      ...state,
      movieSeries: [...state.movieSeries, action.payload]
    }
                case Actions.AddStudio: return {
      ...state,
      movieStudios: [...state.movieStudios, action.payload]
    }


    default:
      return state;
  }
};