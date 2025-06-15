import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Point these at your screen files
import RegisterScreen from './screens/RegisterScreen';
import CheckinScreen from './screens/CheckinScreen';

export type RootStackParamList = {
  Register: undefined;
  Checkin: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Register">
        <Stack.Screen 
          name="Register" 
          component={RegisterScreen} 
          options={{ title: 'Register Face' }}
        />
        <Stack.Screen 
          name="Checkin" 
          component={CheckinScreen} 
          options={{ title: 'Mark Attendance' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}