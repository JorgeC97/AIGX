import React from 'react';
import { Image, StyleSheet, View, Dimensions, Animated, ScrollView } from "react-native";

export default function Noticias() {
    return (
        <View style={styles.container}>
        <Image style={styles.image} source={require('../assets/comingsoon.png')}/>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#fff",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: 'column'
    },
    mainContainer: {
      backgroundColor: "#fff",
    },
    image: {
      flex: 1,
      width: 300,
      resizeMode: 'contain', },
  });