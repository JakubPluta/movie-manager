import { useState } from "react";

const AdminImportMovies = () => {
  const [importStatus, setImportStatus] = useState("");

  const onImportMovies = async () => {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URI}/movies`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }
    );
    const data = await response.json();

    if (response.ok) {
      const count = data.length;

      if (count === 0) {
        setImportStatus("No movies were available for import");
      } else {
        setImportStatus(`Imported ${count} movie files`);
      }
    } else {
      setImportStatus(data.detail.message);
    }
  };

  return (
    <div className="border border-black p-4 text-center mx-auto w-max">
      <div>
        <button
          className="bg-blue-700 hover:bg-blue-600 font-semibold px-8 py-2 text-center text-lg text-white"
          type="button"
          onClick={onImportMovies}
        >
          Import Movies
        </button>
      </div>
      {importStatus && <div>{importStatus}</div>}
    </div>
  );
};

export default AdminImportMovies;
