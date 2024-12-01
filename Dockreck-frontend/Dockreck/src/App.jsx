import { Outlet } from "react-router-dom";
import "./App.css";
import NavBar from "./components/navBar";
// import MainComp from "./components/MainComp";
// import CategoryComp from "./components/CategoryComp";
function App() {
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
