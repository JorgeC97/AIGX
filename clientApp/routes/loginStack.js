import { createStackNavigator } from 'react-navigation-stack';
import { createAppContainer } from 'react-navigation';
import React from 'react';
import Header from '../shared/header';
import Login from '../screens/login';
import Home from '../screens/home';

const screens = {
    Login: {screen: Login, 
        navigationOptions: {
        headerShown: false,
        }
    },
};

const LoginStack = createStackNavigator(screens);

export default createAppContainer(LoginStack);
