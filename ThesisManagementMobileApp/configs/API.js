import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";

const HOST = 'https://ngovanlau.pythonanywhere.com';

export const endpoints = {
    'login': '/o/token/',
    'current-user': '/users/current-user',
    'theses-need-grading': (committeeId) => `/committees/${committeeId}/theses`,
    'thesis-detail': (thesisId) => `/theses/${thesisId}`,
    'criteria': '/criteria/',
    'scoring': (thesisId) => `/theses/${thesisId}/scores/`,
    'change-password': '/users/change-password/',
    'theses': '/theses/',
    'thesis-of-student': '/students/thesis',
    'students': '/students/',
    'lecturers': '/lecturers/',
    'committees': '/committees/',
    'add-committee-to-thesis': (thesisId) => `/theses/${thesisId}/committee`
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