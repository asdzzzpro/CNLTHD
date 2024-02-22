import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

const HOST = 'http://127.0.0.1:8000/';

export const endpoints = {
    'login': '/o/token/',
    'current-user': '/users/current-user',
}

export const authAPI = (accessToken) => axios.create({
    baseURL: HOST,
    headers: {
        "Authorization": `Bearer ${accessToken?accessToken:AsyncStorage.getItem('access-token')}`
    },
});

export default axios.create({
    baseURL: HOST,
})