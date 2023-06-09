import axios from "axios";
import jwt_decode from "jwt-decode";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import {
  _clearLocal,
  _getAccessToken,
  _getRefreshToken,
} from "../../services/localStorageServcies";
import Image from "next/image";
import axiosInstance from "../../services/axiosauth";

const Sidebar = () => {
  const router = useRouter();
  const [LoggedIn, setLoggedIn] = useState<Boolean>(false);
  const [isOpen, setIsOpen] = useState<Boolean>(false);

  const collapseSidebar = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    console.log(_getRefreshToken());
    axiosInstance
      .post(`${process.env.NEXT_PUBLIC_API_HOST}/core/user/logout/`, {
        refresh: _getRefreshToken(),
      })
      .then((res) => {
        _clearLocal();
        setLoggedIn(false);
        router.push("/");
      })
      .catch((err) => {
        console.log(err.response);
        // if (err.response.status === 401) {
        //   _clearLocal();
        //   router.push("/login");
        // }
      });
  };

  useEffect(() => {
    const hadleSidebarSize = () => {
      if (window.innerWidth >= 768) {
        setIsOpen(true);
      } else {
        setIsOpen(false);
      }
    };
    window.addEventListener("resize", hadleSidebarSize);

    const accesToken = _getAccessToken();

    try {
      const decoded: any = jwt_decode(accesToken);
      if (decoded.exp * 1000 < Date.now()) {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
      }
    } catch (error) {
      setLoggedIn(false);
    }
  }, []);

  const navToHome = () => {
    router.push("/");
    collapseSidebar();
  };

  return (
    <>
      {!isOpen ? (
        <div
          className="z-50 float-right mt-5 mr-4 cursor-pointer rounded-md bg-white p-2 dark:bg-slate-700 md:hidden"
          onClick={collapseSidebar}
        >
          <svg
            className="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h8m-8 6h16"
            />
          </svg>
        </div>
      ) : (
        <div className="z-50 float-right mt-5 mr-4 cursor-pointer rounded-md bg-white p-2 dark:bg-slate-700 md:hidden">
          <svg
            className="h-6 w-6"
            onClick={collapseSidebar}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            ></path>
          </svg>
        </div>
      )}
      <>
        <div
          className={`sidebar fixed top-0
                    z-30
                    h-screen w-1/4 overflow-y-hidden
                    bg-transparent
                    duration-300
                    ease-in-out dark:border-none ${
                      isOpen ? "translate-x-0" : "-translate-x-full"
                    }
                    md:hidden`}
          onClick={collapseSidebar}
        />
        <div
          className={`sidebar font-Poppins fixed right-0 top-0 bottom-0 z-30  h-screen w-3/4  
                       overflow-y-hidden border-2
                      border-gray-200 px-2 
                      py-2 duration-300 ease-in-out
                      dark:border-none
                      md:flex md:h-20 md:w-screen md:items-center md:overflow-y-hidden
                      md:rounded-b-lg md:border-0 ${
                        isOpen
                          ? "translate-x-0"
                          : "translate-x-full md:translate-x-0"
                      }
                      bg-white dark:bg-gray-800 md:bg-gray-200`}
        >
          <div className="mt-4 flex justify-between text-xl text-gray-900 dark:text-white md:mt-1 md:items-center md:justify-between md:py-2 md:pr-2">
            <div className="mx-4 -mt-2 flex justify-start px-4 py-2">
              <Image
                src="/shelterkart_final_logo.svg"
                alt="Shelterkart"
                objectFit="cover"
                width={200}
                height={50}
              />
            </div>
          </div>

          <div className="md:fixed md:right-20 md:flex md:items-center">
            <div className=" sidebar-menu" onClick={navToHome}>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-7 w-7"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                />
              </svg>
              <span className="ml-4 text-lg ">Home</span>
            </div>

            {!LoggedIn ? (
              <div className="md:flex">
                <div
                  className="sidebar-menu"
                  onClick={() => router.push("/login")}
                >
                  <svg
                    className="h-7 w-7"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1}
                      d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                    />
                  </svg>
                  <span className="ml-4 text-lg">Login</span>
                </div>
                <div
                  className="sidebar-menu"
                  onClick={() => router.push("/signup")}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-7 w-7"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                    />
                  </svg>
                  <span className="ml-4 text-lg">Signup</span>
                </div>
              </div>
            ) : (
              <div className="md:flex">
                <div
                  className="sidebar-menu"
                  onClick={() => router.push("/coupon")}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-7 w-7"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                    />
                  </svg>
                  <span className="ml-4 text-lg">My Coupons</span>
                </div>

                <div className="sidebar-menu" onClick={handleLogout}>
                  <svg
                    className="h-7 w-7"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1}
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                  </svg>
                  <span className="ml-4 text-lg">Logout</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </>
    </>
  );
};

export default Sidebar;
