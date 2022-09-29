import { Provider } from "react-redux";
import { render, RenderOptions } from "@testing-library/react"

import { createNewStore } from "./state/store";

interface Props {
  children: React.ReactNode;
}

const Wrapper: React.FC<Props> = ({ children }) => (
  <Provider store={createNewStore()}>{children}</Provider>
);


const customRender = (
    ui: React.ReactElement,
    options?: Omit<RenderOptions, "wrapper">
) => (render(ui, { wrapper: Wrapper, ...options }))


export * from "@testing-library/react"
export {customRender as render}
