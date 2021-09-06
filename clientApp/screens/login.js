import React, { useState } from "react";
import { Image, StyleSheet, View, Dimensions, Animated, ScrollView } from "react-native";
import { Input, Header, Button, Icon } from "../components";

const { height } = Dimensions.get("screen");

export default function Login({navigation}) {

  const [alignment, setAlignment] = useState(new Animated.Value(0));
  const [name, setName] = useState('usuario')

  const toDocumentsPage = () => {
    Animated.timing(alignment, {
      toValue: 1,
      duration: 500,
      useNativeDriver: false,
    }).start();
  };

  const backToMainComponent = () => {
    Animated.timing(alignment, {
      toValue: 0,
      duration: 500,
      useNativeDriver: false,
    }).start();
  };

  const heightIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [height, 0],
  });

  const opacityIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [1, 0],
  });

  const documentPageOpacityIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 1],
  });

  const documentPageHeightIntropolate = alignment.interpolate({
    inputRange: [0, 1],
    outputRange: [0, height],
  });

  const mainContainerStyle = {
    height: heightIntropolate,
    opacity: opacityIntropolate,
  };

  const documentContainerStyle = {
    height: documentPageHeightIntropolate,
    opacity: documentPageOpacityIntropolate,
  };

  return (
    
    <View style={styles.container}>
    <ScrollView>
      <Animated.View style={[styles.mainContainer, mainContainerStyle]}>
        <View style={{ size: "10" }}>
          <Image style={{ width: 150, height: 150}} source={require('../assets/logoaigx.png')}/>
        </View>
        <View style={{ width: "100%" }}>
          <Header title="Bienvenido" subTitle="Introduzca los Siguientes Datos" />
        </View>
        <View>
          <Input onChangeText={(val) => setName(val)} icon="md-person" placeholder="Usuario" />
          <Input icon="md-mail" placeholder="Correo Electronico" />
          <Input icon="ios-lock" placeholder="Contraseña" />
        </View>
        <Button onPress={() => toDocumentsPage()} title="Iniciar Sesión" />
      </Animated.View>
      </ScrollView>
      <ScrollView>
      <Animated.View style={[styles.mainContainer, documentContainerStyle]}>
        <Icon
          name="chevron-left"
          onPress={() => backToMainComponent()}
          size={30}
        />
        <View style={{ width: "100%" }}>
          <Header
            title="Hola"
            subTitle={name}
          />
        </View>
        <View>

        </View>
        <Button title="Elegir contrato" onPress={() => navigation.navigate('Inicio')} />
      </Animated.View>
      </ScrollView>
    </View>
  );
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