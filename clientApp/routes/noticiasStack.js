import { createStackNavigator } from 'react-navigation-stack';
import React from 'react';
import Header from '../shared/header';
import Noticias from '../screens/noticias';

const screens = {
    Noticias: { screen: Noticias,
        navigationOptions: ({ navigation }) => {
            return {
                headerTitle: () => <Header title='Noticias' navigation={navigation} />
            }
        },
    },
};

const NoticiasStack = createStackNavigator(screens);

export default NoticiasStack;