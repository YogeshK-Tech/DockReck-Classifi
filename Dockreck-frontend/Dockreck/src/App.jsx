import { Outlet } from "react-router-dom";
import "./App.css";
import NavBar from '../src/components/NavBar';
// import MainComp from "./components/MainComp";
// import CategoryComp from "./components/CategoryComp";
function App() {
  return (
    <>
      <NavBar/>
      <Outlet />
      {/* <MainComp></MainComp>
      <CategoryComp></CategoryComp> */}
    </>
  );
}

export default App;
