import React, { useRef } from 'react';
import {
  View,
  Button,
  Alert,
  Text,
  StyleSheet,
} from 'react-native';
import {
  CameraView,
  useCameraPermissions,
  CameraType,
} from 'expo-camera';
import axios from 'axios';

export default function CheckinScreen() {
  // 1. Permission hook
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState(CameraType.front);    
  const cameraRef = useRef(null);

  // 2. Loading state
  if (!permission) {
    return <View />;
  }

  // 3. Not granted yet
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

  // 4. Camera + check-in logic
  const handleCheckin = async () => {
    const photo = await cameraRef.current.takePictureAsync({
      base64: true,
    });
    try {
      const res = await axios.post(
        'http://192.168.1.123:5000/checkin',
        { image: photo.base64 }
      );
      Alert.alert('Check-In Status', res.data.message);
    } catch (err) {
      console.error(err);
      Alert.alert(
        'Check-In Error',
        err.response?.data?.message || err.message
      );
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef} facing={facing}/>
      <Button
        title="Mark Attendance"
        onPress={handleCheckin}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});