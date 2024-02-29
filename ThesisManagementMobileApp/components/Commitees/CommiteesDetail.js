import { useEffect, useState } from "react";
import { View, Text, Image } from "react-native"


const CommiteesDetail = ({route}) => {

    const { committee } = route.params;

    return (
        <View>
            <Text>{committee.name}</Text>
            <Text>Thành viên:</Text>
            {committee.members && committee.members.map((member, idx) => (
                <View key={idx}>
                    <Image source={{ uri: member.lecturer.avatar }} style={{ width: 100, height: 100 }} />
                    <Text>Họ và tên: {member.lecturer.fullname}</Text>
                    <Text>Vai trò: {member.role}</Text>
                    <Text>Khoa: {member.lecturer.faculty.name}</Text>
                </View>
            ))}
        </View>
    )
}

export default CommiteesDetail;