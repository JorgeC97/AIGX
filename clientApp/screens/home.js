import React from 'react';
import { Image, StyleSheet, View, Dimensions, Animated, ScrollView } from "react-native";

export default function Home() {
    return (
        <View style={styles.container}>
         <Image style={{ width: 150, height: 150}} source={require('../assets/logoaigx.png')}/>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#fff",
    },
    mainContainer: {
      backgroundColor: "#fff",
      alignItems: "center",
      justifyContent: "center",
    },
  });