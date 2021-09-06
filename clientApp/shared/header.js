import React from 'react';
import { StyleSheet, Text, View, Image} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

export default function Header({ title, navigation }) {

  const openMenu = () => {
    navigation.openDrawer();
  }

  return (
    <View style={styles.header} >
      <MaterialIcons name='menu' color='rgb(244, 148, 28)' size={28} onPress={openMenu} style={styles.icon} />
      <View style={styles.headerTitle}>
      <Image source={require('../assets/logoaigx.png')} style={styles.headerImage} />
        <Text color='rgb(244, 148, 28)'  style={styles.headerText}>{title}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
    header: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'center',
    },
    headerText: {
      fontWeight: 'bold',
      fontSize: 20,
      color: 'rgb(244, 148, 28)',
      letterSpacing: 1,
    },
    icon: {
      position: 'absolute',
      left: 0,
    },
    headerTitle: {
      flexDirection: 'row'
    },
    headerImage: {
      width: 26,
      height: 26,
      marginHorizontal: 10
    },
  });