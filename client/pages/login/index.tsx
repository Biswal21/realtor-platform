import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import Login from "../../components/Login";
import {
  _getAccessToken,
  _getRefreshToken,
  _setToken,
  _clearLocal,
} from "../../services/localStorageServcies";
import axiosInstance from "../../services/axiosauth";
import jwt_decode from "jwt-decode";

const LoginUser = () => {
  const router = useRouter();
  const [Checked, setChecked] = useState<Boolean>(false);
  const [checkDecoded, setCheckDecoded] = useState<Boolean>(true);

  const getNewAccessToken = () => {
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
        // console.log(err)
        setChecked(true);
        router.push("/login");
      });
  };

  useEffect(() => {
    if (_getAccessToken() && checkDecoded) {
      try {
        const decoded: any = jwt_decode(_getAccessToken());
        if (typeof decoded.exp !== "number") getNewAccessToken();
        if (decoded.exp * 1000 < Date.now()) getNewAccessToken();
        else router.push("/city");
      } catch (error) {
        console.log(error);
        getNewAccessToken();
      }
    } else {
      setCheckDecoded(false);
      getNewAccessToken();
    }
  }, []);

  return <div className="">{!Checked ? null : <Login />}</div>;
};

export default LoginUser;
