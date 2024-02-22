import { createDrawerNavigator } from '@react-navigation/drawer';
import { StatusBar } from 'expo-status-bar';
import React, { useReducer } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import UserReducer from './reducers/UserReducer';
import MyContext from "./configs/MyContext";
import { NavigationContainer } from '@react-navigation/native';
import Login from './components/User/Login';
import Home from './components/Home/Home';
import { createStackNavigator } from '@react-navigation/stack';

const Drawer = createDrawerNavigator();
const Stack = createStackNavigator()

const HomeDrawer = () => {
  <Drawer.Navigator initialRouteName='Home'>
    <Drawer.Screen name='Login' component={Login} options={{ title: 'Trang chủ' }} />
    <Drawer.Screen name='Home' component={Home} options={{ title: 'Trang chủ' }} />
  </Drawer.Navigator>
}

const App = () => {

  const [user, dispatch] = useReducer(UserReducer, null);

  return (
    <MyContext.Provider value={[user, dispatch]}>
      <NavigationContainer >
        <Stack.Navigator initialRouteName='Login'>
          <Stack.Screen name='Login' component={Login}
            options=
            {
              {
                title: 'Đăng nhập',
                headerStyle: {
                  backgroundColor: '#afeeee',
                },
              }
            } />
          <Stack.Screen name='Home' component={HomeDrawer}/>
        </Stack.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  );
}

export default App;