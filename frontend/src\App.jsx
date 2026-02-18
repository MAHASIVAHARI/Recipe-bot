import { useState } from "react";
import "./App.css";

function App() {
  const [ingredients, setIngredients] = useState("");
  const [diet, setDiet] = useState("general");
  const [recipe, setRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!ingredients) {
      setError("Please enter ingredients");
      return;
    }

    setIsLoading(true);
    setError(null);
    setRecipe(null);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/generate-recipe`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ingredients,
            diet,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();
      setRecipe(data);
    } catch (err) {
      setError("Failed to generate recipe. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🍳 AI Recipe Generator</h1>

      <textarea
        placeholder="Enter ingredients (e.g., tomato, onion, rice)"
        value={ingredients}
        onChange={(e) => setIngredients(e.target.value)}
      />

      <select value={diet} onChange={(e) => setDiet(e.target.value)}>
        <option value="general">General</option>
        <option value="weight-loss">Weight Loss</option>
        <option value="high-protein">High Protein</option>
        <option value="vegetarian">Vegetarian</option>
      </select>

      <button onClick={handleGenerate} disabled={isLoading}>
        {isLoading ? "Generating..." : "Generate Recipe"}
      </button>

      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {recipe && (
        <div className="recipe-card">
          <h2>{recipe.name}</h2>

          {recipe.calories && (
            <p>
              <strong>Calories:</strong> {recipe.calories}
            </p>
          )}

          {recipe.protein && (
            <p>
              <strong>Protein:</strong> {recipe.protein}
            </p>
          )}

          <ul>
            {recipe.steps &&
              recipe.steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
