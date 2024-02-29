import { useEffect, useState } from "react";
import { View, Text, ScrollView, ActivityIndicator, TouchableOpacity } from "react-native";
import MyStyle from "../../styles/MyStyle";
import Style from "./Style";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { authAPI, endpoints } from "../../configs/API";


const Committees = ({ navigation }) => {

    const [committees, setCommittees] = useState(null);

    useEffect(() => {
        const loadCommittees = async () => {
            try {
                let accessToken = await AsyncStorage.getItem('access-token')
                let res = await authAPI(accessToken).get(endpoints['committees'])
                setCommittees(res.data)
            }
            catch (error) {
                console.error(error)
            }
        }
        console.info(committees)
        loadCommittees();
    }, [navigation]);

    const detail = (committee) => {
        navigation.navigate('CommitteesDetail', {'committee':committee})
    }

    const addCommittees = () => {
        navigation.navigate('AddCommittees')
    }
    

    return (
        <ScrollView contentContainerStyle={{ alignItems: 'flex-start'}}>
            {committees === null ? <ActivityIndicator /> : <>
                {committees.map(committee => (
                    <TouchableOpacity onPress={() => detail(committee)} style={[Style.card, MyStyle.mb_20]}>
                        <Text style={[Style.text]}>{committee.name}</Text>
                        <Text style={[Style.item]}>Thành viên:</Text>
                        {committee.members && committee.members.map((member, memberIndex) => (
                            <View key={memberIndex}>
                                <Text>{member.lecturer.fullname}</Text>
                            </View>
                        ))}
                    </TouchableOpacity>
                ))}
            </>}
            
            <TouchableOpacity onPress={() => addCommittees()}>
                <Text style={[Style.button]}>Thêm Hội Đồng Mới</Text>
            </TouchableOpacity>

        </ScrollView>
    )
}

export default Committees;