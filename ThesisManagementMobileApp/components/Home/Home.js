import { Text, View } from "react-native"
import MyStyle from "../../styles/MyStyle";
import { useContext, useEffect, useState } from "react";
import Style from "./Style";
import { ScrollView } from "react-native";
import MyContext from "../../configs/MyContext";
import API, { authAPI, endpoints } from "../../configs/API";
import AsyncStorage from "@react-native-async-storage/async-storage";

const Home = () => {

    const [theses, setTheses] = useState();
    const [user, ] = useContext(MyContext);

    useEffect(() => {
        let theses = [];

        user?.committees.forEach(committee => {

            const loadThesis = async () => {
                let accessToken = await AsyncStorage.getItem("access-token")
                let res = await authAPI(accessToken).get(endpoints['theses-need-grading'](committee.id))

                if (res.data.length !== 0) {
                    console.info(res.data)
                    theses.map(res.data)
                }
            }

            loadThesis();
        });

        setTheses(theses)

    }, [])

    console.info(theses)

    return (
        <ScrollView contentContainerStyle={{alignItems: 'center', justifyContent: 'center', flex: 1}}>
            <View style={[MyStyle.elevation, Style.card, MyStyle.mb_20]}>
                <View style={[MyStyle.row, MyStyle.between]}>
                    <Text style={[Style.title]}>Quản lý khách sản</Text>
                    <Text style={[MyStyle.elevation, Style.score]}>9.0</Text>
                </View>
                <Text style={[MyStyle.f_16]}>SV:</Text>
                <Text style={[MyStyle.f_16]}>GVHD:</Text>
                <Text style={[MyStyle.f_16]}>Hội đồng:</Text>
                <Text style={[MyStyle.f_16]}>Ngày tạo:</Text>
            </View>
        </ScrollView>
    )
}

export default Home;