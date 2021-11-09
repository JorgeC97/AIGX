import React, { useState } from "react";
import { Image, StyleSheet, View, Dimensions, Animated, ScrollView, Alert } from "react-native";
import { Input, Header, Button, Icon,  } from "../components";
import AsyncStorage from '@react-native-async-storage/async-storage';
import {Picker} from '@react-native-picker/picker';

const { height } = Dimensions.get("screen");

export default function Login({navigation}) {

  const [alignment, setAlignment] = useState(new Animated.Value(0));
  const [name, setName] = useState('usuario')
  const [username, setUsername] = useState('username')
  const [password, setPassword] = useState('password')

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

  const get_set_cookies = async function(value) {
    
    await AsyncStorage.setItem('cookie', value)
    console.log(value)
}

  const login = () => {
    let formdata = new FormData();
    formdata.append('username',username)
    formdata.append('password',password)

    fetch('http://192.168.0.2:80/api/login', {
      method: 'POST',
      credentials: 'same-origin',
      body: formdata})
      .then((resp)=>{
        return resp.json()
      })
      .then((data)=>{ 
        if (data.name !== "Wrong Username or Password"){
          console.log("Logged in!!");
          setName(data.name)
          get_set_cookies(data.session)
          getContratos()
          toDocumentsPage()
        } else {
          // Alert.alert("error", text)
          alert(data.name)
        }
        console.log(data)
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const [contratos, setContratos] = useState([])

  const [contrato, setContrato] = useState()

  const handleValueChange=(itemValue, itemIndex) =>setContrato(itemValue)

  const getContratos = async () => {
    const cookie = await AsyncStorage.getItem('cookie') 
    fetch('http://192.168.0.2:80/api/proyectos?sid='+cookie, {
      method:"GET"
    })

    .then(resp => resp.json())
    .then(datos => {
      let arrayContratos = []
      if(typeof(datos) != 'array'){
        arrayContratos.push(datos)
      } else {
        arrayContratos = datos
      }
      setContratos(arrayContratos)
      console.log(arrayContratos)
    })
    .then(()=> {
      toDocumentsPage()
    })
    .catch((error) => {
      console.error(error);
    });

  }


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
          {/* <Input onChangeText={(val) => setName(val)} icon="md-person" placeholder="Usuarioss" /> */}
          <Input icon="md-mail" placeholder="Correo Electronico" value={username} onChangeText={setUsername} />
          <Input icon="ios-lock" placeholder="Contraseña" value={password} onChangeText={setPassword} />
        </View>
        <Button onPress={() => login()} title="Iniciar Sesión" />
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
          <ul>
          {contratos.map((item) => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
        {/* <Picker
          selectedValue={contrato}
          style={{ height: 50, width: 150 }}
          onValueChange={handleValueChange}
        >
          {
            contratos.map(contrato=> <Picker.Item key={contrato.id} label={contrato.name} value={contrato.id}/>)
          }
        </Picker> */}
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