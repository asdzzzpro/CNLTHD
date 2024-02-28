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
import Profile from './components/User/Profile';
import Thesis from './components/Thesis/Thesis';
import Logout from './components/User/Logout';

const Drawer = createDrawerNavigator();
const Stack = createStackNavigator()

const HomeStack = () => {
  <Stack.Navigator initialRouteName='Home'>
    
  </Stack.Navigator>
}

const App = () => {

  const [user, dispatch] = useReducer(UserReducer, null);

  return (
    <MyContext.Provider value={[user, dispatch]}>
      <NavigationContainer >
        <Drawer.Navigator initialRouteName='Login' screenOptions={{headerRight: Logout}}>
          {user===null?<>
            <Drawer.Screen name='Login' component={Login}
            options=
            {
              {
                title: 'Đăng nhập',
                headerStyle: {
                  backgroundColor: '#afeeee',
                },
              }
            } />
          </>:<>
            <Drawer.Screen name={user?.fullname} component={Thesis}/>
            <Drawer.Screen name='Home' component={Home} options={{ title: 'Trang chủ' }} />
            <Drawer.Screen name='Profile' component={Profile} options={{ title: 'Profile' }} />
          </>}
        </Drawer.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  );
}

export default App;