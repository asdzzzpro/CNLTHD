import { Image, Text, TextInput, TouchableOpacity, View, Alert } from "react-native"
import { ScrollView } from "react-native";
import MyContext from "../../configs/MyContext";
import { useContext, useEffect, useState, useRef } from "react";
import Style from "./Style";
import MyStyle from "../../styles/MyStyle";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authAPI, endpoints } from "../../configs/API";

const Profile = ({ navigation }) => {
    const [pass, setPass] = useState({
        "password": "",
        "confirm_password": ""
    })

    const [user,] = useContext(MyContext)
    const [theses, setTheses] = useState([]);
    const [isHidden, setIsHidden] = useState(true);

    useEffect(() => {

        const loadUser = async () => {
            let accessToken = await AsyncStorage.getItem("access-token")
            let res = await authAPI(accessToken).get(endpoints['/users/current-user'])

            if (res.data.length !== 0) {
                setTheses(res.data)
            }
        }

        loadUser();
    }, [])

    const toggleVisibility = () => {
        setIsHidden(!isHidden);
    };



    const changePassword = async () => {
        if (pass.password === pass.confirm_password) {
            let form = new FormData();

            for (let key in pass) {
                form.append(key, pass[key])
            }

            try {
                let accessToken = await AsyncStorage.getItem("access-token")
                let res = await authAPI(accessToken).patch(endpoints['change-password'], form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                Alert.alert(
                    'Hoàn tất',
                    'Thay đổi thành công!',
                    [
                        { text: 'OK', onPress: () => console.log('OK') }
                    ],
                    { cancelable: true }
                )
                navigation.navigate("Home");

            } catch (ex) {
                console.error(ex);
            }
        } else {
            Alert.alert(
                'Mật khẩu không khớp!',
                'Vui lòng nhập và xác nhận mật khẩu giống nhau.',
                [
                    { text: 'OK', onPress: () => console.log('Mật khẩu không khớp') }
                ],
            )
        }


    }

    const change = (field, value) => {
        setPass(current => {
            return { ...current, [field]: value };
        });
    };


    return (
        <ScrollView contentContainerStyle={{ alignItems: 'center', justifyContent: 'center'}}>
            <View>
                <View style={[Style.container, { alignItems: 'flex-start', width: '90%' }]}>

                    <Text style={[Style.small_title]}>Thông Tin Tài Khoản:</Text>
                    <Image
                        source={{ uri: user.avatar }}
                        style={{ width: 150, height: 150 }}
                    />

                    <Text style={[Style.item, MyStyle.mb_20]}>Tên: {user.fullname}</Text>
                    <Text style={[Style.item, MyStyle.mb_20]}>Email: {user.email}</Text>
                    <TouchableOpacity onPress={toggleVisibility} style={[Style.button, MyStyle.mb_20]}>
                        <Text style={Style.text}>Đổi mật khẩu</Text>
                    </TouchableOpacity>


                </View>
                <View style={{ display: isHidden ? 'none' : 'flex' }}>
                    <TextInput value={pass.password} onChangeText={t => change("password", t)} secureTextEntry={true} placeholder="Mật khẩu..." style={[Style.input, MyStyle.mb_20]} />
                    <TextInput value={pass.confirm_password} onChangeText={t => change("confirm_password", t)} secureTextEntry={true} style={[Style.input, MyStyle.mb_20]} placeholder="Xác nhận mật khẩu" />
                    <TouchableOpacity onPress={() => changePassword(navigation)} style={[Style.button, MyStyle.mb_20, {backgroundColor:"orange"}]}>
                        <Text style={Style.text}>Xác nhận</Text>
                    </TouchableOpacity>
                </View>

            </View>
        </ScrollView>



    )
}

export default Profile;