import { useRouter } from 'next/router';
import { config } from 'process';
import { _getAccessToken, _getRefreshToken, _setToken, _setAccessToken, _removeAccessToken } from './localStorageServcies';
import axios from "axios";
import { count } from 'console';
import jwt_decode from "jwt-decode";
import dayjs from 'dayjs';

// const baseURL = 'http://139.59.23.157:8000';
const baseURL = process.env.NEXT_PUBLIC_API_HOST;

let refresh = _getRefreshToken()
let access = _getAccessToken()
const axiosInstance = axios.create({
    
    baseURL,
    headers: {
        Authorization: `Bearer ${ _getAccessToken() }`
    }
});

axiosInstance.interceptors.request.use(async req => {

    if (req.headers) req.headers.Authorization = `Bearer ${ _getAccessToken() }`
    

    const user: any = jwt_decode(_getAccessToken())
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1
    // console.log('is_expired', isExpired)
    if(!isExpired) return req


    const res = await axios.post(`${baseURL}/core/user/refresh/`, { refresh: _getRefreshToken() })
    const tokens = await res.data
    // console.log("36================",tokens);
    _removeAccessToken()
    _setAccessToken(tokens.access)
    if (req.headers) req.headers.Authorization = `Bearer ${ _getAccessToken() }`
    
    return req
    
})

export default axiosInstance


