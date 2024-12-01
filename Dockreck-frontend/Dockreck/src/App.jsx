import { useEffect } from "react";
import { Outlet } from "react-router-dom";
import "./App.css";
import NavBar from "./components/navBar";
// import MainComp from "./components/MainComp";
// import CategoryComp from "./components/CategoryComp";
function App() {
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/initial_run", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Backend Response:", data);
        } else {
          const error = await response.json();
          console.error("Error:", error);
        }
      } catch (error) {
        console.error("Fetch Error:", error);
      }
    };

    fetchData();
  }, []); // Runs only once when the component mounts
  return (
    <>
      <NavBar></NavBar>
      <Outlet />
      {/* <MainComp></MainComp>
      <CategoryComp></CategoryComp> */}
    </>
  );
}

export default App;
