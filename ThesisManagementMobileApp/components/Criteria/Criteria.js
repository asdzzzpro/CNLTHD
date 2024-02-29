import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { ActivityIndicator, ScrollView, Text, TextInput, TouchableOpacity, View } from "react-native";
import { authAPI, endpoints } from "../../configs/API";
import MyStyle from "../../styles/MyStyle";
import Style from "./Style";

const Criteria = () => {
    const [criteria, setCriteria] = useState(null)
    const [isHidden, setIsHidden] = useState(false);
    const [name, setName] = useState('');

    useEffect(() => {
        const loadCriteria = async () => {
            try {
                let accessToken = await AsyncStorage.getItem('access-token')
                //sửa lại token
                let res = await authAPI(accessToken).get(endpoints['criteria'])
                console.info(res.data)
                setCriteria(res.data)
            } catch (ex) {
                console.error(ex);
            }
        }

        loadCriteria()
    }, [])

    const createCriteria = async () => {
        try {
            let accessToken = await AsyncStorage.getItem('access-token');
            const data = {
                name: name,
            };

            let res = await authAPI(accessToken).post(endpoints['criteria'], data);

            console.info(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const toggleVisibility = () => {
        setIsHidden(!isHidden);
    };

    const handleCriteriaChange = (text) => {
        setName(text);
    };

    return (
        <ScrollView>
            {criteria === null ? <ActivityIndicator /> : <>
                {criteria.map(criteria => (
                    <Text style={[MyStyle.mb_20, Style.text, Style.card]}>Tiêu Chí {criteria.id}: {criteria.name}</Text>
                ))}
            </>}

            <TouchableOpacity onPress={toggleVisibility} style={[Style.button, MyStyle.mb_20, { width: "50%", display: isHidden ? 'flex' : 'none' }]}>
                <Text>Thêm Tiêu Chí Mới</Text>
            </TouchableOpacity>
            <View style={{ display: isHidden ? 'none' : 'flex', width: '100%' }}>
                <Text style={Style.text}>Nhập tên tiêu chí:</Text>
                <TextInput style={[Style.input]} onChangeText={t => handleCriteriaChange(t)} />
                <View style={[MyStyle.mb_20, { flexDirection: 'row', justifyContent: 'space-between' }]}>
                    <TouchableOpacity onPress={createCriteria} style={[Style.button, MyStyle.mb_20, { width: "50%", backgroundColor: "#FF4D4D" }]}>
                        <Text>Lưu</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={[Style.button, MyStyle.mb_20, { width: '45%', backgroundColor: 'orange' }]} onPress={toggleVisibility}>
                        <Text>Hủy</Text>
                    </TouchableOpacity>
                </View>

            </View>


        </ScrollView>
    )
}

export default Criteria;