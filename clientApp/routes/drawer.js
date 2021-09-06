import { createDrawerNavigator } from 'react-navigation-drawer';
import React from 'react';
import { AntDesign, MaterialCommunityIcons, Entypo } from '@expo/vector-icons'; 
import { createAppContainer} from 'react-navigation'
import HomeStack from './homeStack';
import NoticiasStack from './noticiasStack';
import ReportesSStack from './reportesSStack';
import LoginStack from './loginStack';
import PedidosStack from './pedidosStack';
import { HeaderTitle } from 'react-navigation-stack';


const RootDrawerNavigator = createDrawerNavigator({
    Login: {
        screen: LoginStack,
        navigationOptions: {
            headerLeft: null,
            drawerLabel: () => null,
            title: null,
            drawerLockMode: 'locked-closed',
        }, 
        
    },
    Inicio: {
        screen: HomeStack,
        navigationOptions: {
            drawerLockMode: 'unlocked',
            drawerIcon: () => (
                <AntDesign name="home" size={24} color='rgb(244, 148, 28)' />
            ),
          },
    },
    Reportes: {
        screen: ReportesSStack,
        navigationOptions: {
            drawerIcon: () => (
                <Entypo name="documents" size={24} color='rgb(244, 148, 28)' />
            ),
          },
    },
    Pedidos: {
        screen: PedidosStack,
        navigationOptions: {
            drawerIcon: () => (
                <Entypo name="calendar" size={24} color='rgb(244, 148, 28)' />
            ),
          },
    },
    Noticias: {
        screen: NoticiasStack,
        navigationOptions: {
            drawerIcon: () => (
                <MaterialCommunityIcons name="newspaper" size={24} color='rgb(244, 148, 28)' />
            ),
            title: 'Noticias',
            
          },
    }}, { 
        contentOptions: {
            labelStyle: {
              fontSize: 15,
              marginLeft: 10,
              color: 'rgb(22, 103, 171)'
            },
          },
        drawerWidth: 220,
});

export default createAppContainer(RootDrawerNavigator);