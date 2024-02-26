import { Text, View } from "react-native"
import MyStyle from "../../styles/MyStyle";
import { useEffect, useState } from "react";
import Style from "./Style";
import { ScrollView } from "react-native";

const Home = () => {

    const [theses, setTheses] = useState();

    useEffect(() => {

    }, [])

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