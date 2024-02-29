import { ActivityIndicator, ScrollView, Text, TextInput, TouchableOpacity, View } from "react-native";
import MyStyle from "../../styles/MyStyle";
import Style from "./Style";
import { useContext, useEffect, useState } from "react";
import MyContext from "../../configs/MyContext";
import { authAPI, endpoints } from "../../configs/API";
import AsyncStorage from "@react-native-async-storage/async-storage";

const Thesis = ({ route }) => {

    const [thesis, setThesis] = useState(null)
    const [criteria, setCriteria] = useState(null)
    const [user,] = useContext(MyContext)
    const { thesisId } = route.params;
    const [isShow, setIsShow] = useState(true)
    const [scores, setScores] = useState(null)

    useEffect(() => {
        const loadThesis = async () => {
            try {
                let accessToken = await AsyncStorage.getItem('access-token')
                let res = await authAPI(accessToken).get(endpoints['thesis-detail'](thesisId));
                setThesis(res.data)
            } catch (ex) {
                console.error(ex);
            }
        }
        loadThesis();

        if (user.role === 'lecturer') {
            const loadCriteria = async () => {
                try {
                    let accessToken = await AsyncStorage.getItem('access-token')
                    let res = await authAPI(accessToken).get(endpoints['criteria'])
                    setCriteria(res.data)
                } catch (ex) {
                    console.error(ex)
                }
            }
            loadCriteria();
        }
    }, [thesisId])

    const show = () => {
        setIsShow(!isShow)
    }

    const createForm = (id, value) => {
        setScores(current => {
            return {
                ...current, [id - 1]: {
                    'criteria_id': id,
                    'score': value
                }
            }
        })
    }

    const scoring = () => {
        let index = 0
        criteria.forEach(async criteria => {
            try {
                let accessToken = await AsyncStorage.getItem('access-token')
                let res = await authAPI(accessToken).post(endpoints['scoring'](thesisId), scores[index++]);

                setThesis(res.data)
            } catch (ex) {
                console.error(ex);
            }
        });
    }

    return (
            <ScrollView contentContainerStyle={{paddingHorizontal: 16}}>
            {thesis === null ? <ActivityIndicator /> : <>
                <Text style={[Style.title]}>{thesis.name}</Text>
                <Text style={[Style.item]}>Điểm: {thesis.average}</Text>
                <Text style={[Style.item]}>Sinh viên thực hiện: {thesis.students.map(student => student.fullname)}</Text>
                <Text style={[Style.item]}>Giảng viên hướng dẫn: {thesis.lecturers.map(lecturer => lecturer.fullname)}</Text>
                <Text style={[Style.item]}>Hội đồng bảo vệ: {thesis.committee?thesis.committee.name:'Chưa thêm hội đồng'}</Text>
                <Text style={[Style.item]}>Ngành: {thesis.students[0].major.name}</Text>
                <Text style={[Style.item]}>Khoa: {thesis.students[0].faculty.name}</Text>

                {user.role === 'lecturer' ? <>
                    <View style={{ alignItems: 'center', width: '100%', marginVertical: 10, display: isShow?'flex':'none'}}>
                        <TouchableOpacity style={[Style.button]} onPress={() => { show(); }}>
                            <Text style={Style.text}>Chấm điểm</Text>
                        </TouchableOpacity>
                    </View>
                    <View style={[MyStyle.container, { width: '100%', display: isShow ? 'none' : 'flex' }]}>
                        <Text style={Style.title}>Các tiêu chí chấm điểm</Text>
                        {criteria === null ? <ActivityIndicator /> : <>
                            {criteria.map(criteria => (
                                <View style={[MyStyle.elevation, MyStyle.mb_20, Style.card, {width: '100%'}]}>
                                    <Text style={[Style.subject]}>{criteria.name}</Text>
                                    <TextInput style={[Style.input]} onChangeText={t => createForm(criteria.id, parseFloat(t))} placeholder="Nhập điểm" />
                                </View>
                            ))}
                        </>}
                        <View style={[MyStyle.row, { alignItems: 'center', justifyContent: 'space-between', width: '100%', marginVertical: 10 }]}>
                            <TouchableOpacity style={[Style.button, {width: '45%'}]} onPress={scoring}>
                                <Text style={Style.text}>Lưu</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={[Style.button, {width: '45%', backgroundColor: 'orange'}]} onPress={() => { show(); }}>
                                <Text style={Style.text}>Hủy</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </> : <></>}
            </>}
        </ScrollView>
    )
}


export default Thesis;