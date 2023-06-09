import React, { useState, useEffect } from "react";
import Signup from "../../components/Signup";
import { useRouter } from "next/router";
import {
  _clearLocal,
  _getAccessToken,
  _getRefreshToken,
  _setToken,
} from "../../services/localStorageServcies";
import axiosInstance from "../../services/axiosauth";
import jwt_decode from "jwt-decode";

const Register = () => {
  const router = useRouter();
  const [Checked, setChecked] = useState<Boolean>(false);
  const [checkDecoded, setCheckDecoded] = useState<Boolean>(true);

  const getNewAccessToken = () => {
    // console.log(_getRefreshToken());
    axiosInstance
      .post(`${process.env.API_HOST}/core/refresh/`, {
        refresh: _getRefreshToken(),
      })
      .then((res) => {
        _clearLocal();
        _setToken(res.data);

        router.push("/city");
      })
      .catch((err) => {
        console.log(err);
        setChecked(true);
        router.push("/signup");
      });
  };

  useEffect(() => {
    if (_getAccessToken() && checkDecoded) {
      try {
        const decoded: any = jwt_decode(_getAccessToken());
        if (typeof decoded.exp !== "number") getNewAccessToken();
        if (decoded.exp * 1000 < Date.now()) getNewAccessToken();
        else router.push("/");
      } catch (error) {
        console.log(error);
        getNewAccessToken();
      }
    } else {
      setCheckDecoded(false);
      getNewAccessToken();
    }
  }, []);

  return <>{!Checked ? null : <Signup />} </>;
};

export default Register;
