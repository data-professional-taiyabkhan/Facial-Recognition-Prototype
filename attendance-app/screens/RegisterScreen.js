import React, { useState, useRef } from 'react';
import {
  View,
  Button,
  Alert,
  Text,
  TextInput,
  StyleSheet,
} from 'react-native';
import {
  CameraView,
  useCameraPermissions,
  cameraType as CameraType,
} from 'expo-camera';
import axios from 'axios';

export default function RegisterScreen() {
  // 1. Hook to check/request camera permission
  const [permission, requestPermission] = useCameraPermissions();
  const [name, setName] = useState('');
  const cameraRef = useRef(null);

  // 2. If permissions are still loading...
  if (!permission) {
    return <View />;
  }

  // 3. If not granted, show a button to ask
  if (!permission.granted) {
    return (
      <View style={styles.center}>
        <Text style={{ marginBottom: 10 }}>
          We need your permission to show the camera
        </Text>
        <Button
          title="Grant Camera Permission"
          onPress={requestPermission}
        />
      </View>
    );
  }

  // 4. Once granted, render the camera & controls
  const handleRegister = async () => {
    const photo = await cameraRef.current.takePictureAsync({
      base64: true,
    });
    try {
      const res = await axios.post(
        'http://192.168.1.123:5000/register',
        {
          name: name.trim() || 'Unknown',
          image: photo.base64,
        }
      );
      Alert.alert('Success', res.data.message);
    } catch (err) {
      console.error(err);
      Alert.alert(
        'Registration Error',
        err.response?.data?.message || err.message
      );
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef} />
      <TextInput
        placeholder="Enter your name"
        value={name}
        onChangeText={setName}
        style={styles.input}
      />
      <Button
        title="Register Face"
        onPress={handleRegister}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  input: {
    padding: 8,
    margin: 12,
    borderWidth: 1,
    borderRadius: 4,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});