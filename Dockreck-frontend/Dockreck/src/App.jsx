import { Outlet } from "react-router-dom";
import "./App.css";
import NavBar from "./components/navBar";
import { useNavigate, Routes,Route } from "react-router-dom";
import SignIn from "./components/Signin";
import Dashboard from "./components/dashboard";
import CategoryComp from "./components/CategoryComp";
import History from "./components/History";
import About from "./components/About";

// import MainComp from "./components/MainComp";
// import CategoryComp from "./components/CategoryComp";
function App() {
  return (
    <>
      <Routes>
        <Route path="/dashboard" element={<Dashboard></Dashboard>}></Route>
        <Route path="/" element={<SignIn></SignIn>}></Route>
        <Route path="/classification" element={<CategoryComp></CategoryComp>}></Route>
        <Route path="/history" element={<History></History>}></Route>
        <Route path="/about" element={<About></About>}></Route>
      </Routes>
      
    </>
  );
}

export default App;
