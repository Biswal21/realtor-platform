import axios from "axios";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import { AuthFieldError, UserData } from "../types/interfaces";
import Sidebar from "./Layout/Sidebar";
import Verify from "./Verify";
import Back from "./Layout/Back";
import Logo from "./Layout/Logo";
import Footer from "./Layout/Footer";

const Signup: React.FC = () => {
  const router = useRouter();

  const [user, setUser] = useState<UserData>({
    name: "",
    alt_name: "",
    email: "",
    alt_email: "",
    phone_number: "",
    alt_phone_number: "",
  });

  const [error, setError] = useState<AuthFieldError>({
    name: "",
    email: "",
    altEmail: "",
    phoneNumber: "",
    altPhoneNumber: "",
  });

  const [ttlOtp, setTtlOtp] = useState<string>("");
  const [otpSize, setOtpSize] = React.useState<number>(0);
  const [toVerify, settoVerify] = useState<Boolean>(false);

  const isSignUp: Boolean = true;

  const [moreHeight, setHeight] = useState<Boolean>(false);
  // const [closeAlert, setCloseAlert] = useState<Boolean>(false);

  useEffect(() => {
    const checkHeight = () => {
      if (window.innerWidth > 768 && window.innerWidth < 1024) {
        if (window.innerHeight > 1000) setHeight(true);
        else setHeight(false);
      }
    };

    window.addEventListener("resize", checkHeight);
  }, []);

  const validateForm = () => {
    let formIsvalid = true;
    const emailRegex = new RegExp(
      "([!#-'*+/-9=?A-Z^-~-]+(.[!#-'*+/-9=?A-Z^-~-]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([!#-'*+/-9=?A-Z^-~-]+(.[!#-'*+/-9=?A-Z^-~-]+)*|[[\t -Z^-~]*])"
    );
    const phoneRegex = new RegExp("^\\+?\\d{9,15}$");
    let error: AuthFieldError = {
      name: "",
      email: "",
      altEmail: "",
      phoneNumber: "",
      altPhoneNumber: "",
      userExists: "",
    };

    if (!user.name) {
      formIsvalid = false;
      error.name = "Please enter your name";
    }
    if (!user.email) {
      formIsvalid = false;

      error.email = "Please enter your email id";
    }
    if (user.email && !emailRegex.test(user.email)) {
      formIsvalid = false;

      error.email = "Enter a valid email id";
    }
    if (user.alt_email && !emailRegex.test(user.alt_email)) {
      formIsvalid = false;
      error.altEmail = "Enter a valid alternate email id";
    }
    if (!user.phone_number) {
      formIsvalid = false;

      error.phoneNumber = "Please enter your phone number";
    }
    if (user.phone_number && !phoneRegex.test(user.phone_number)) {
      formIsvalid = false;

      error.phoneNumber = "Please enter a valid phone number";
    }
    if (user.alt_phone_number && !phoneRegex.test(user.alt_phone_number)) {
      formIsvalid = false;

      error.altPhoneNumber = "Please enter a valid alternate phone number";
    }
    setError(error);
    return formIsvalid;
  };

  const handleSignUpSubmit = () => {
    if (validateForm()) {
      axios
        .post(`${process.env.NEXT_PUBLIC_API_HOST}/core/user/signup/`, user)
        .then((res) => {
          setTtlOtp(res.data.ttl_otp);
          setOtpSize(res.data.otp_size);
          settoVerify(true);
        })
        .catch((err) => {
          if (err.response.status === 409) {
            setError({ ...error, userExists: "User already exists" });
          }
        });
    }
  };

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
            <div className={`card mx-4 mt-16 h-fit w-full py-4 px-4`}>
              <div className="flex justify-center">
                <h1 className="mb-2 block text-2xl font-light text-gray-900 dark:text-gray-300">
                  Create Account
                </h1>
              </div>
              <div className="mb-4 h-1">
                <p className="form-alert">{error.userExists}</p>
              </div>

              <div>
                <label htmlFor="name" className="flex items-center">
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
                      d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span className="text-md pl-1 font-medium">Name</span>
                  <span className="pl-1 text-red-600 dark:text-red-500">*</span>
                </label>

                <input
                  className={`input-field ${
                    error.name
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="text"
                  placeholder="Enter your Name"
                  name="name"
                  value={user.name}
                  onChange={(e) => {
                    setUser({ ...user, name: e.target.value });
                    setError({ ...error, name: "", userExists: "" });
                  }}
                />
              </div>
              <div className="h-6">
                <p className="form-alert">{error.name}</p>
              </div>

              <div>
                <label htmlFor="email" className="flex items-center">
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
                      d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                    />
                  </svg>
                  <span className="text-md pl-1 font-medium">Email</span>
                  <span className="pl-1 text-red-600 dark:text-red-500">*</span>
                </label>
                <input
                  className={`input-field ${
                    error.email
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="email"
                  placeholder="Enter your email"
                  name="email"
                  value={user.email}
                  onChange={(e) => {
                    setUser({ ...user, email: e.target.value });
                    setError({ ...error, email: "", userExists: "" });
                  }}
                />
              </div>
              <div className="h-6 ">
                <p className="form-alert">{error.email}</p>
              </div>

              <div>
                <label htmlFor="alternate_email" className="flex items-center">
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
                      d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                    />
                  </svg>
                  <span className="text-md pl-1 font-medium">
                    Alternate Email
                  </span>
                </label>
                <input
                  className={`input-field ${
                    error.altEmail
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="email"
                  placeholder="Enter your alternate email"
                  name="alternate_email"
                  value={user.alt_email}
                  onChange={(e) => {
                    setUser({ ...user, alt_email: e.target.value });
                    setError({ ...error, altEmail: "", userExists: "" });
                  }}
                />
              </div>
              <div className="h-6">
                <p className="form-alert">{error.altEmail}</p>
              </div>

              <div>
                <label htmlFor="phone_number" className="flex items-center">
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
                  <span className="text-md pl-1 font-medium">Phone Number</span>
                  <span className="pl-1 text-red-600 dark:text-red-500">*</span>
                </label>
                <input
                  className={`input-field ${
                    error.phoneNumber
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="tel"
                  placeholder="Enter your phone number"
                  name="phone_number"
                  value={user.phone_number}
                  onChange={(e) => {
                    setUser({ ...user, phone_number: e.target.value });
                    setError({ ...error, phoneNumber: "", userExists: "" });
                  }}
                />
              </div>
              <div className="h-6">
                <p className="form-alert">{error.phoneNumber}</p>
              </div>

              <div>
                <label
                  htmlFor="alternate_phone_number"
                  className="flex items-center"
                >
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
                  <span className="text-md pl-1 font-medium">
                    Alternate Phone Number
                  </span>
                </label>
                <input
                  className={`input-field ${
                    error.altPhoneNumber
                      ? "border-red-600 dark:border-red-600"
                      : "border-gray-300"
                  } mt-4`}
                  type="tel"
                  placeholder="Enter your alternate phone number"
                  name="alt_phone_number"
                  value={user.alt_phone_number}
                  onChange={(e) => {
                    setUser({ ...user, alt_phone_number: e.target.value });
                    setError({ ...error, altPhoneNumber: "", userExists: "" });
                  }}
                />
              </div>
              <div className="h-6">
                <p className="form-alert">{error.altPhoneNumber}</p>
              </div>

              <div className="flex justify-center">
                <button
                  className="mb-2 w-full rounded-lg bg-blue-700 px-2.5 py-2.5 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  type="submit"
                  value="Submit"
                  onClick={handleSignUpSubmit}
                >
                  Register
                </button>
              </div>
            </div>
          ) : (
            <div className="relative flex flex-col items-center justify-center">
              <Verify
                phoneNumber={user.phone_number}
                ttl={ttlOtp}
                isSignup={isSignUp}
                otpSize={otpSize}
              />
            </div>
          )}
        </div>
        <Footer />
      </div>
    </>
  );
};

export default Signup;
