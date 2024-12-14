import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { useAuth } from "@clerk/clerk-react";
import { useCallback } from "react";
import { RiLinkedinLine, RiTwitterLine, RiFacebookFill } from "@remixicon/react";


export default function SignIn() {
    console.log("rerender")
    const navigate = useNavigate()
    const CheckAuth = useCallback(function () {
        const { isSignedIn } = useAuth()
        if (isSignedIn) {
            navigate("/dashboard")
        }
    })
    CheckAuth()
    function handleSignIn() {
        navigate("/dashboard")
    }

    return (
        <main className="relative w-screen h-screen bg-black">

            <header className="text-white flex flex-col justify-center items-center">
                
                    <div className="flex w-[90vw] md:w-[70vw] lg:w-[70vw] p-3 justify-between items-center  relative z-10 ">
                        <h1 className="md:text-[2rem] lg:text-[2rem] text-[1rem ] font-bold text-gray-400">Dockreck</h1>
                            <SignedOut>
                                <SignInButton afterSignIn={handleSignIn} >
                                    <button  className=" p-1 border border-slate-700 pl-4 pr-4 rounded-lg bg-slate-950">Get Started</button>
                                </SignInButton>
                            </SignedOut>    
                    </div>

                
                <div className="flex p-3   relative z-10 w-[90vw] md:w-[50vw] lg:w-[50vw] mt-10 justify-center items-center text-center text-[1rem] md:text-[3.5rem] lg:text-[3.5rem] text-white">
                        Effortless Document Management 
                </div>
                <div className="flex p-3 w-[90vw] md:w-[50vw] lg:w-[50vw] relative z-10 mt-5 justify-center items-center text-center text-[1.5rem] text-gray-400">
                Upload, Preview, and Organize Your Documents in Seconds. Experience smarter categorization and seamless integration with Google Drive.
                </div>
                <div className="flex gap-5 mt-10 p-5 bg-transparent backdrop-blur-sm border border-slate-950 rounded-full relative z-10">
                    <RiLinkedinLine color="white" size={36}></RiLinkedinLine>
                    <RiTwitterLine color="white" size={36}></RiTwitterLine>
                    <RiFacebookFill color="white" size={36}></RiFacebookFill>
                </div>
                <div className="top-0 z-0 absolute bg-gradient-to-b from-slate-950 to-black w-full flex justify-center items-center h-[80vh]">
                </div>
            </header>

            <svg aria-hidden="true" className="pointer-events-none h-full w-full fill-neutral-400/80 absolute inset-0 z-0 [mask-image:radial-gradient(50vw_circle_at_center,white,transparent)]"><defs><pattern id=":r2:" width="16" height="16" patternUnits="userSpaceOnUse" patternContentUnits="userSpaceOnUse" x="0" y="0"><circle id="pattern-circle" cx="1" cy="1" r="1"></circle></pattern></defs><rect width="100%" height="100%" stroke-width="0" fill="url(#:r2:)"></rect></svg>
    </main>
    );
}