import { useState } from "react";

function App() {

  const [message, setMessage] = useState("");

  async function callApi() {
    const res = await fetch("http://localhost:5001/api");
    const data = await res.json();
    setMessage(data.Hello);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Frontend connecté à FastAPI 🚀</h1>

      <button onClick={callApi}>Appeler /api</button>

      {message && <p>Réponse backend : {message}</p>}
    </div>
  );
}

export default App;
