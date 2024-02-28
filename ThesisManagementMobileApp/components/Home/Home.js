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

    const [theses, setTheses] = useState(null);
    const [user,] = useContext(MyContext);

    useEffect(() => {
        let lecturerTheses = [];

        const loadThesis = async (committee) => {
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

        user?.committees.forEach(committee => {
            loadThesis(committee);
        });

    }, [navigation])

    const thesisDetail = (thesisId) => {
        navigation.navigate('Thesis', { 'thesisId': thesisId })
    }

    return (
        <ScrollView contentContainerStyle={{ alignItems: 'center', justifyContent: 'center', flex: 1 }}>
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
                            <Text style={[MyStyle.f_16]}>Hội đồng: {thesis.committee.name}</Text>
                            <Text style={[MyStyle.f_16]}>Ngày tạo: {moment(thesis.created_date).fromNow()}</Text>
                        </View>
                    </TouchableOpacity>
                ))}
            </>}
        </ScrollView>
    )
}

export default Home;