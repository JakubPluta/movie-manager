import React, { useReducer } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Container from "./components/Container";
import AdminPage from "./pages/AdminPage";
import MainPage from "./pages/MainPage";
import { initialState } from "./state/initialState";
import reducer from "./state/reducer";
import StateContext from "./state/StateContext";
import NavBar from "./components/NavBar";

function App() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <BrowserRouter>
    <StateContext.Provider value={{ state, dispatch }}>
        <Container>
          <NavBar />
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/admin" element={<AdminPage />} />
            </Routes>
      </Container>
      </StateContext.Provider>
      </BrowserRouter>
  );
}

export default App;
