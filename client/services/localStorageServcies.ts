import { TokenData } from "../types/interfaces";

export const _setToken = (tokenObj: TokenData) => {
  localStorage.setItem("access_token", tokenObj.access);
  localStorage.setItem("refresh_token", tokenObj.refresh);
};

export const _setPhoneNumber = (phoneNumber: string) => {
  localStorage.setItem("phone_number", phoneNumber);
};

export const _getPhoneNumber = () => {
  localStorage.getItem("phone_number");
};

export const _getAccessToken = () => {
  if (process.browser && localStorage.access_token)
    return localStorage.access_token;
  return "";
};

export const _getRefreshToken = () => {
  if (process.browser && localStorage.refresh_token)
    return localStorage.refresh_token;
  return "";
};

export const _setAccessToken = (access: string) => {
  localStorage.setItem("access_token", access);
};

export const _removeAccessToken = () => {
  localStorage.removeItem("access_token");
};

export const _clearLocal = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("phone_number");
};
