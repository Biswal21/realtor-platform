import axios from "axios";
import React, { useState, useEffect } from "react";
import { _setToken } from "../services/localStorageServcies";
import { AuthFieldError, toVerifyTime } from "../types/interfaces";
import Sidebar from "./Layout/Sidebar";
import Verify from "./Verify";
import { useRouter } from "next/router";
import Back from "./Layout/Back";
import Logo from "./Layout/Logo";
import Footer from "./Layout/Footer";

const Login: React.FC = () => {
  const [toVerify, setToVerify] = useState<Boolean>(false);
  const [ttlOtp, setTtlOtp] = useState<string>("");
  const [otpSize, setOtpSize] = React.useState<number>(0);
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [error, setError] = useState<AuthFieldError>({
    phoneNumber: "",
    userDoesntExists: "",
  });
  const [moreHeight, setHeight] = useState<Boolean>(false);
  const router = useRouter();

  useEffect(() => {
    const checkHeight = () => {
      if (window.innerWidth > 768 && window.innerWidth < 1024) {
        if (window.innerHeight > 1000) setHeight(true);
        else setHeight(false);
      }
    };

    window.addEventListener("resize", checkHeight);
  }, []);
  const isSignUp: Boolean = false;

  const validateLoginForm = () => {
    let formIsvalid = true;
    const phoneRegex = new RegExp("^\\+?\\d{9,15}$");
    let phoneNumberError: string = "";
    console.log(error);

    if (!phoneNumber) {
      console.log("No phone no ", phoneNumber);
      formIsvalid = false;
      phoneNumberError = "Enter a valid phone number";
    }
    // console.log(phoneRegex.test(phoneNumber), "27");
    if (phoneNumber && !phoneRegex.test(phoneNumber)) {
      console.log("phone no regex", phoneNumber);
      formIsvalid = false;
      phoneNumberError = "Please enter a valid phone number";
    }
    setError({ ...error, phoneNumber: phoneNumberError });
    return formIsvalid;
  };

  const handleLoginClick = () => {
    if (validateLoginForm()) {
      axios
        .post(`${process.env.NEXT_PUBLIC_API_HOST}/core/user/login/`, {
          phone_number: phoneNumber,
        })
        .then((res) => {
          // console.log(res.data);
          setTtlOtp(res.data.ttl_otp);
          setOtpSize(res.data.otp_size);
          setToVerify(true);
        })
        .catch((err) => {
          console.log(err.response);
          if (err.response.status === 404) {
            setError({
              ...error,
              userDoesntExists:
                "Phone number is not registered. Kindly Sign up.",
            });
          }
        });
    }
  };
  // TODO: Add a button to resend the OTP do after throttling
  // TODO: remove inline styles
  return (
    <>
      <div className="flex min-h-screen flex-col bg-gray-200 dark:bg-slate-900">
        <div className="flex-r sticky top-0 z-10 flex justify-between  bg-gray-200 pt-2 dark:bg-slate-900">
          <Back router={router} />
          <Logo />
          <Sidebar />
        </div>
        <div className="flex">
          {!toVerify ? (
            <div className="card mx-4 mt-16 h-fit w-full py-4 px-4">
              <div className="flex justify-center">
                <h1 className="mb-2 block text-2xl font-light text-gray-900 dark:text-gray-300">
                  Login
                </h1>
              </div>

              <div className="mb-4 h-1">
                <p
                  className={` text-sm font-medium text-red-600 dark:text-red-500`}
                >
                  {error.userDoesntExists}
                </p>
              </div>
              <div>
                <label
                  htmlFor="phone number"
                  className="mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                >
                  <div className="flex items-center">
                    <svg
                      className="mb-1 h-5 w-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                      />
                    </svg>
                    <span className="text-md pl-1 font-light">
                      {" "}
                      Phone Number
                    </span>
                    <span className="pl-1 text-red-600 dark:text-red-500">
                      *
                    </span>
                  </div>
                </label>
                <input
                  className={`input-field ${
                    error.phoneNumber
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="tel"
                  name="phone_number"
                  value={phoneNumber}
                  placeholder="Enter your phone number"
                  required={true}
                  onChange={(e) => {
                    !toVerify && setPhoneNumber(e.target.value);
                    setError({
                      ...error,
                      phoneNumber: "",
                      userDoesntExists: "",
                    });
                  }}
                />
              </div>
              <div className="h-6 ">
                <p className="form-alert">{error.phoneNumber}</p>
              </div>
              <div className="flex justify-center">
                <button
                  className="mb-2 w-full rounded-lg bg-blue-700 px-2.5 py-2.5 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  type="submit"
                  value="submit"
                  onClick={handleLoginClick}
                >
                  Login
                </button>
              </div>
            </div>
          ) : (
            <Verify
              phoneNumber={phoneNumber}
              ttl={ttlOtp}
              isSignup={isSignUp}
              otpSize={otpSize}
            />
          )}
        </div>
        <Footer />
      </div>
    </>
  );
};

export default Login;
