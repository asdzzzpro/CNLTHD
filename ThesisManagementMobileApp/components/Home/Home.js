import { ActivityIndicator, Text, TouchableOpacity, View } from "react-native"
import MyStyle from "../../styles/MyStyle";
import { useContext, useEffect, useState } from "react";
import Style from "./Style";
import { ScrollView } from "react-native";
import MyContext from "../../configs/MyContext";
import API, { authAPI, endpoints } from "../../configs/API";
import AsyncStorage from "@react-native-async-storage/async-storage";
import moment from "moment";

const Home = ({ navigation }) => {

    const [theses, setTheses] = useState(null)
    const [user,] = useContext(MyContext)

    useEffect(() => {
        switch (user.role) {
            case 'academic_manager':
                const loadTheses = async () => {
                    try {
                        let accessToken = await AsyncStorage.getItem('access-token')
                        let res = await authAPI(accessToken).get(endpoints['theses'])
                        setTheses(res.data)
                    } catch (ex) {
                        console.error(ex);
                    }
                }

                loadTheses()
                break
            case 'lecturer':
                let lecturerTheses = [];

                user?.committees.forEach(committee => {
                    const loadTheses = async () => {
                        try {
                            let accessToken = await AsyncStorage.getItem('access-token')
                            let res = await authAPI(accessToken).get(endpoints['theses-need-grading'](committee.id))
                            let data = res.data

                            if (data.length !== 0) {
                                lecturerTheses = lecturerTheses.concat(res.data)
                                setTheses(lecturerTheses)
                            }
                        } catch (ex) {
                            console.error
                        }
                    }

                    loadTheses();
                });
                break
            case 'student':
                const loadThesis = async () => {
                    try {
                        let accessToken = await AsyncStorage.getItem('access-token')
                        let res = await authAPI(accessToken).get(endpoints['thesis-of-student'])
                        setTheses(() => [].concat(res.data))
                    } catch (ex) {
                        console.error(ex);
                    }
                }

                loadThesis()
                break

        }
    }, [navigation])

    const thesisDetail = (thesisId) => {
        navigation.navigate('Thesis', { 'thesisId': thesisId })
    }

    const addThesis = () => {
        navigation.navigate('AddThesis')
    }

    return (
        <View>
            {user.role === 'academic_manager' ? <>
                <View style={{width: '100%', marginTop: 20, alignItems: 'center'}}>
                    <TouchableOpacity style={[Style.button, {width: '90%'}]} onPress={addThesis}>
                        <Text style={Style.text}>Thêm khóa luận</Text>
                    </TouchableOpacity>
                </View>
            </> : <></>}

            <ScrollView contentContainerStyle={{ alignItems: 'center', justifyContent: 'center', marginTop: 20 }}>
                {theses === null ? <ActivityIndicator /> : <>
                    {theses.map(thesis => (
                        <TouchableOpacity onPress={() => thesisDetail(thesis.id)}>
                            <View style={[MyStyle.elevation, Style.card, MyStyle.mb_20]} >
                                <View style={[MyStyle.row, MyStyle.between]}>
                                    <Text style={[Style.title]}>{thesis.name}</Text>
                                    <Text style={[MyStyle.elevation, Style.score]}>{thesis.average}</Text>
                                </View>
                                <Text style={[MyStyle.f_16]}>SV: {thesis.students.map(student => student.fullname)}</Text>
                                <Text style={[MyStyle.f_16]}>GVHD: {thesis.lecturers.map(lecturer => lecturer.fullname)}</Text>
                                <Text style={[MyStyle.f_16]}>Hội đồng: {thesis.committee?thesis.committee.name:'Chưa thêm hội đồng'}</Text>
                                <Text style={[MyStyle.f_16]}>Ngày tạo: {moment(thesis.created_date).fromNow()}</Text>
                            </View>
                        </TouchableOpacity>
                    ))}
                </>}
            </ScrollView>
        </View>
    )
}

export default Home;