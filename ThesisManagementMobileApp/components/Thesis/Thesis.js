import { Text, TextInput, TouchableOpacity, View } from "react-native";
import MyStyle from "../../styles/MyStyle";
import Style from "./Style";

const Thesis = () => {
    return (
        <View style={[MyStyle.container, {alignItems: 'flex-start', width: '90%'}]}>
            <Text style={[Style.title]}>Quản lý nhà sách</Text>
            <Text style={[Style.item]}>Điểm:</Text>
            <Text style={[Style.item]}>Sinh viên thực hiện:</Text>
            <Text style={[Style.item]}>Giảng viên hướng dẫn:</Text>
            <Text style={[Style.item]}>Hội đồng bảo vệ:</Text>
            <View style={{alignItems: 'center', width: '100%', marginVertical: 10}}>
                <TouchableOpacity style={Style.button}>
                    <Text style={Style.text}>Chấm điểm</Text>
                </TouchableOpacity>
            </View>
            <View style={[MyStyle.elevation, Style.card]}>
                <Text style={[Style.subject]}>1. Trình bày</Text>
                <TextInput style={Style.input} placeholder="Nhập điểm"/>
            </View>
            <View style={{alignItems: 'center', width: '100%', marginVertical: 10}}>
                <TouchableOpacity style={Style.button}>
                    <Text style={Style.text}>Lưu</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}

export default Thesis;