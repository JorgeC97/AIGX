import React from 'react';
import { createStackNavigator } from 'react-navigation-stack';
import Header from '../shared/header';
import Home from '../screens/home';

const screens = {
    Inicio: { screen: Home,
        navigationOptions: ({ navigation }) => {
            return {
                headerTitle: () => <Header title='Inicio' navigation={navigation} />
            }
        },
    },
};

const HomeStack = createStackNavigator(screens, {
    /*defaultNavigationOptions: {
      headerTintColor: '#444',
      headerStyle: { backgroundColor: 'rgb( 4, 52, 92)', height: 93 },
    }*/
  });

/*const HomeStack = createStackNavigator(screens);*/

export default HomeStack;