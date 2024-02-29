import { createDrawerNavigator } from '@react-navigation/drawer';
import React, { useReducer } from 'react';
import UserReducer from './reducers/UserReducer';
import MyContext from "./configs/MyContext";
import { NavigationContainer } from '@react-navigation/native';
import Login from './components/User/Login';
import Home from './components/Home/Home';
import Thesis from './components/Thesis/Thesis';
import Profile from './components/User/Profile'
import { createStackNavigator } from '@react-navigation/stack';
import Logout from './components/User/Logout';
import AddThesis from './components/Thesis/AddThesis';

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
        <Drawer.Navigator initialRouteName='Login' screenOptions={({route}) => ({
          headerRight: () => {
            if (route.name === 'Login') {
              return null
            }
            return <Logout/>
          }
        })}>
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
            <Drawer.Screen name={user?.fullname} component={Profile}/>
            <Drawer.Screen name='Home' component={Home} options={{ title: 'Trang chủ' }} />
            <Drawer.Screen name="Thesis" component={Thesis} options={{ title: "Chi tiết khóa luận", drawerItemStyle: {display: "none"}}} />
            <Drawer.Screen name='Profile' component={Profile} options={{ title: 'Thông tin cá nhân', drawerItemStyle: {display: "none"}}} />
            {user.role === 'academic_manager'?<>
            <Drawer.Screen name='AddThesis' component={AddThesis} options={{ title: 'Thêm khóa luận', drawerItemStyle: {display: "none"}}} />
            </>:<></>}
          </>}
        </Drawer.Navigator>
      </NavigationContainer>
    </MyContext.Provider>
  );
}

export default App;