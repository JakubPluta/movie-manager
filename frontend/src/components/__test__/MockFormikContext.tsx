import { Formik } from "formik";
import { mainPageFormInitialValues } from "../../state/formik";


interface Props {
    children: React.ReactElement
}

const MockFormikContext: React.FC<Props> = ({ children }) => (
  <Formik initialValues={mainPageFormInitialValues} onSubmit={jest.fn()}>
    {children}
  </Formik>
);

export default MockFormikContext;
