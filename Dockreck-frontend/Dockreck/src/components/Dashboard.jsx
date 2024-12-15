import "../App.css";
import NavBar from "./navBar";
import MainComp from "./MainComp";
import CategoryComp from "./CategoryComp";
import { useAuth } from "@clerk/clerk-react";
import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate()
    const [view, setview] = useState("blank")
    const { isSignedIn } = useAuth()
    const CheckAuth = useCallback(function () {
        if (!isSignedIn) {
            navigate("/")
            return null
        }else{
            if(view == "blank")
                setview("dashboard")
        }
    })
    CheckAuth()
    return(
        <>
            {
                view == "dashboard" && 
                <div className="relative">
                    <NavBar></NavBar>
                    <MainComp></MainComp>
                </div>
            }
            
        </>
    )
}

export default Dashboard;