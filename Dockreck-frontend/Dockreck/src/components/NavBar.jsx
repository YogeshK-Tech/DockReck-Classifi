import React from "react";
import { SignedIn,UserButton } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";

const NavBar = () => {
  const navigate = useNavigate()

  return (
    <div className="overflow-hidden top-0">
      <header className="w-screen h-[10vh] bg-slate-950 flex justify-evenly pl-10 pr-10 items-center border-b border-gray-600 ">
        <button className=" text-yellow-500 text-[1.5rem]" onClick={()=>{navigate("/")}}> <a href="/">Dockreck</a>
        </button>
        <div className="flex gap-6 text-white">
          <button onClick={()=>{navigate("/dashboard")}} className="p-2 pl-4 pr-4 rounded-lg hover:bg-slate-800">Home</button>
          <button onClick={()=>{navigate("/history")}} className="p-2 pl-4 pr-4 rounded-lg hover:bg-slate-800">History</button>
          <button onClick={()=>{navigate("/about")}} className="p-2 pl-4 pr-4 rounded-lg hover:bg-slate-800 ">About</button>
        </div>
        <SignedIn >
                <UserButton />
        </SignedIn> 
      </header>
    </div>
  );
};

export default NavBar;
