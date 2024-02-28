import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

const HOST = 'https://ngovanlau.pythonanywhere.com';

export const endpoints = {
    'login': '/o/token/',
    'current-user': '/users/current-user',
    'theses-need-grading': (committee_id) => `/committees/${committee_id}/theses`,
    'change-password': '/users/change-password/'
}

export const authAPI = (accessToken) => axios.create({
    baseURL: HOST,
    headers: {
        "Authorization": `Bearer ${accessToken}`
    },
});

export default axios.create({
    baseURL: HOST,
})