import { createStackNavigator } from 'react-navigation-stack';
import React from 'react';
import Header from '../shared/header';
import Pedidos from '../screens/pedidos';

const screens = {
    Pedidos: { screen: Pedidos,
        navigationOptions: ({ navigation }) => {
            return {
                headerTitle: () => <Header title='Pedidos' navigation={navigation} />
            }
        },
        
    },
};

const PedidosStack = createStackNavigator(screens);

export default PedidosStack;