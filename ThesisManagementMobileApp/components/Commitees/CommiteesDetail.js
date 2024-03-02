import { useEffect, useState } from "react";
import { View, Text, Image, ScrollView } from "react-native"
import Style from "./Style";
import MyStyle from "../../styles/MyStyle";


const CommiteesDetail = ({route}) => {

    const { committee } = route.params;

    return (
        <ScrollView contentContainerStyles={[MyStyle.container]}>
            <Text style={[Style.title]}>{committee.name}</Text>
            <Text style={[Style.text]}>Thành viên:</Text>
        {committee.members && committee.members.map((member, idx) => (
                <View key={idx} style={[Style.card, MyStyle.mb_20, MyStyle.elevation]}>
                    <Image source={{ uri: member.lecturer.avatar }} style={{ width: 100, height: 100 }} />
                    <Text>Họ và tên: {member.lecturer.fullname}</Text>
                    <Text>Vai trò: {member.role}</Text>
                    <Text>Khoa: {member.lecturer.faculty.name}</Text>
                </View>
            ))}
        </ScrollView>
            
        
    )
}

export default CommiteesDetail;