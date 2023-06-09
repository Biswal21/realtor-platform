import axios from "axios";
import { useRouter } from "next/router";
import React, { useState, useEffect } from "react";
import {
  _clearLocal,
  _setPhoneNumber,
  _setToken,
} from "../services/localStorageServcies";

const Verify: React.FC<{
  phoneNumber: string;
  ttl: string;
  isSignup: Boolean;
  otpSize: number;
}> = ({ phoneNumber, ttl, isSignup, otpSize }) => {
  const router = useRouter();

  const OTPobj: { [key: string]: string } = {};

  useEffect(() => {
    for (let OTPindex: number = 0; OTPindex < otpSize; OTPindex++) {
      OTPobj["otp" + OTPindex] = "";
    }
  }, []);

  const [otpObject, setOtpObject] = useState(OTPobj);
  const [OtpValue, setOtpValue] = useState("");
  const [ttlTimer, setTtlTimer] = useState<number>(parseInt(ttl));
  const [resendTimer, setResendTimer] = useState<number>(5);

  const handleChangeValue = (
    otpIndex: string,
    e: { target: { value: string } }
  ) => {
    setOtpObject({ ...otpObject, [otpIndex]: e.target.value });
  };

  const inputFocus = (elmnt: any) => {
    if (elmnt.key === "Delete" || elmnt.key === "Backspace") {
      setOtpValue(OtpValue.slice(0, -1));

      if (
        elmnt.target.value.length === 0 &&
        elmnt.target.previousSibling !== null
      ) {
        elmnt.target.previousSibling.focus();
      }
    } else {
      if (OtpValue.length < otpSize) {
        console.log("object");
        setOtpValue(OtpValue.concat(elmnt.target.value));
      }

      if (
        elmnt.target.value.length === 1 &&
        elmnt.target.nextSibling !== null
      ) {
        elmnt.target.nextSibling.focus();
      }
    }
  };

  const clockFormat = (time: number) => {
    let seconds: number | string = time % 60;
    let minutes: number | string = Math.floor(time / 60);
    minutes = minutes.toString().length === 1 ? `0${minutes}` : minutes;
    seconds = seconds.toString().length === 1 ? `0${seconds}` : seconds;
    return `${minutes}:${seconds}`;
  };

  useEffect(() => {
    let timer: any = null;
    let resendTimer: any = null;

    if (ttlTimer > 0) {
      timer = setInterval(() => {
        setTtlTimer((count) => (count > 0 ? count - 1 : 0));
      }, 1000);
    }

    resendTimer = setInterval(() => {
      setResendTimer((countValue) => (countValue > 0 ? countValue - 1 : 0));
    }, 1000);

    return () => {
      // console.log("object clear");
      clearInterval(timer);
      clearInterval(resendTimer);
    };
  }, []);

  useEffect(() => {
    if (ttlTimer === 0) {
      _clearLocal();
      router.reload();
    }
  }, [ttlTimer]);

  const handleVerifySubmit = () => {
    axios
      .post(`${process.env.NEXT_PUBLIC_API_HOST}/core/user/verify_otp/`, {
        phone_number: phoneNumber,
        otp: OtpValue,
        otp_size: otpSize,
      })
      .then((res) => {
        _clearLocal();
        _setToken(res.data);
        _setPhoneNumber(phoneNumber);

        router.back();
      })
      .catch((err) => {});
  };

  const resendOtp = () => {
    setResendTimer(5);
    axios
      .post(`${process.env.NEXT_PUBLIC_API_HOST}/core/user/resend_otp/`, {
        phone_number: phoneNumber,
        is_signup: isSignup,
      })
      .then((res) => {
        setTtlTimer(res.data.ttl_otp);
      })
      .catch((err) => {
        if (err.response.status === 500) {
        }
      });
  };

  const createInput = () => {
    let inputArray: JSX.Element[] = [];
    for (let OTPindex: number = 0; OTPindex < otpSize; OTPindex++) {
      inputArray.push(
        <input
          key={OTPindex}
          type="tel"
          autoComplete="off"
          className="mx-2 block  w-12 rounded-lg border   bg-gray-50 p-2.5 text-center text-2xl text-gray-900 focus:border-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400  dark:focus:border-blue-500   dark:focus:ring-blue-500"
          onChange={(e) => handleChangeValue("otp" + OTPindex, e)}
          maxLength={1}
          onKeyUp={(e) => inputFocus(e)}
        />
      );
    }
    return inputArray;
  };

  return (
    <div className="card mx-4 mt-16 h-fit w-full px-4 py-4">
      <h1 className="mb-2 flex justify-center text-2xl font-light text-gray-900 dark:text-gray-300">
        OTP verification
      </h1>
      <div className="flex justify-center text-sm font-light text-gray-500">
        Please enter OTP sent to your number
      </div>
      <p className="flex justify-center py-4">
        {clockFormat(Math.trunc(ttlTimer))}
      </p>
      <div className="flex justify-center">{createInput()}</div>

      <div className="my-4 flex justify-center">
        <button
          className="disabled-button mb-2 w-full rounded-lg bg-blue-700 px-2.5 py-2.5 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          type="submit"
          value="submit"
          disabled={!OtpValue || OtpValue.length < otpSize}
          onClick={handleVerifySubmit}
        >
          Submit OTP
        </button>
      </div>
      <div className="flex items-center">
        <button
          className="disabled-button mb-2 w-full rounded-lg bg-blue-700 px-2.5 py-2.5 text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          type="submit"
          onClick={resendOtp}
          disabled={resendTimer > 0}
        >
          Resend OTP in {clockFormat(Math.trunc(resendTimer))}
        </button>
      </div>
    </div>
  );
};

export default Verify;
