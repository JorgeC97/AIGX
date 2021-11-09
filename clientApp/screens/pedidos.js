import React, { useState, useEffect } from 'react';
import { Feather } from '@expo/vector-icons'; 
import { Image, Text, StyleSheet, View, Dimensions, Animated, ScrollView, FlatList, TouchableOpacity, Alert} from "react-native";

export default function Pedidos() {

  /*const [pedido, setPedido] = useState([
    { name: '12 Abr 2020', id: '1' },
    { name: '25 Abr 2020', id: '2' },
    { name: '14 Abr 2020', id: '3' },
    { name: '13 Abr 2020', id: '4' },
    { name: '25 Ene 2020', id: '5' },
    { name: '30 Feb 2020', id: '6' },
    { name: '06 Mar 2020', id: '7' },
    { name: '09 Abr 2020', id: '8' },
    { name: '13 Jul 2020', id: '9' },
    { name: '24 Ago 2020', id: '10' },
    { name: '21 Sep 2020', id: '11' },
  ]);*/

  const [pedido, setPedido] = useState([])

  useEffect(() => {
    fetch('http://192.168.0.2:80/api/news/', {
      method:"GET"
    })

    .then(resp => resp.json())
    .then(pedido => {
      setPedido(pedido)
    })
    .catch(error => Alert.alert("error", error))

  }, [])


  return (
    <View style={styles.container}>
      <FlatList 
        keyExtractor={item => `${item.id}`} 
        data={pedido} 
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
      justifyContent: 'center',
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