import React, { useState, useEffect } from 'react';
import { Feather } from '@expo/vector-icons'; 
import { Image, Text, StyleSheet, View, Dimensions, Animated, ScrollView, FlatList, TouchableOpacity, Alert} from "react-native";

export default function Reportes() {

  /*const [reporte, setReporte] = useState([
    { name: 'Semana 16    12 Abr - 18 Abr 2020', id: '1' },
    { name: 'Semana 17    19 Abr - 25 Abr 2020', id: '2' },
    { name: 'Semana 18    26 Abr - 14 Abr 2020', id: '3' },
    { name: 'Semana 19    03 Abr - 13 Abr 2020', id: '4' },
    { name: 'Semana 20    10 Dic - 25 Ene 2020', id: '5' },
    { name: 'Semana 21    17 Abr - 30 Feb 2020', id: '6' },
    { name: 'Semana 22    24 Jul - 06 Mar 2020', id: '7' },
    { name: 'Semana 23    32 Abr - 09 Abr 2020', id: '8' },
    { name: 'Semana 24    07 Jun - 13 Jul 2020', id: '9' },
    { name: 'Semana 25    15 Abr - 24 Ago 2020', id: '10' },
    { name: 'Semana 26    30 May - 21 Sep 2020', id: '11' },
  ]);*/

  const [reporte, setReporte] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://192.168.0.2:80/api/reportes/', {
      method:"GET"
    })

    .then(resp => resp.json())
    .then(reporte => {
      setReporte(reporte)
    })
    .catch(error => Alert.alert("error", error))

  }, [])

  return (
    <View style={styles.container}>
      <FlatList 
        keyExtractor={item => `${item.id}`} 
        data={reporte} 
        renderItem={({ item }) => (
          <TouchableOpacity style={{flex:1,flexDirection:"row",flexWrap: 'wrap'}}>
            <View style={{flex:1}}>
              <Text style={styles.item} > 
                {item.title} 
              </Text>
            </View>  
            <View>
                <TouchableOpacity>
              <Feather style={styles.icon} name="download" size={24} color='rgb(244, 148, 28)' />
              </TouchableOpacity> 
            </View>  
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
      backgroundColor: "#fff",
    },
    mainContainer: {
      backgroundColor: "#fff",
      alignItems: "center",
      justifyContent: "center",
    },
    item: {
      marginHorizontal: 10,
      marginTop: 10,
      padding: 20,
      backgroundColor: '#04245c',
      fontSize: 15,
      color:'rgb(244, 148, 28)',
      borderRadius: 15,
    },
    icon: {
      marginTop: 7,
      padding: 20,
      borderRadius: 15,
      alignSelf:'flex-end'
    },
  });