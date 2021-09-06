import { createStackNavigator } from 'react-navigation-stack';
import React from 'react';
import Header from '../shared/header';
import ReportesS from '../screens/reportesS';

const screens = {
    Reportes: { screen: ReportesS,
        navigationOptions: ({ navigation }) => {
            return {
                headerTitle: () => <Header title='Reportes' navigation={navigation} />
            }
        },
        
    },
};

const ReportesSStack = createStackNavigator(screens);

export default ReportesSStack;