
import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')

st.set_page_config(page_title='Cloudy', page_icon='🌤️')
st.title('Cloudy 🌤️')
st.write('Enter the city name and click the button to fetch the weather data')

city = st.text_input('Enter the name of the city:')

if st.button('Fetch Weather Data'):
    if not city.strip():
        st.warning('Please enter a city name.')
    else:
        try:
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {
                'q': city.strip(),
                'appid': API_KEY,
                'units': 'metric'
            }

            response = requests.get(
                url, params=params, timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                if not isinstance(data, dict) or 'main' not in data:
                    st.error('Invalid weather data received.')
                else:
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    weather_condition = data['weather'][0]['description']
                    name = data['name']
                    country = data['sys']['country']

                    st.success('Weather data fetched successfully!')
                    st.subheader(f'{name}, {country}')

                    col1, col2 = st.columns(2)
                    col3, col4 = st.columns(2)

                    col1.metric('Temperature', f'{temperature} °C')
                    col2.metric('Humidity', f'💧 {humidity}%')
                    col3.metric('Wind Speed', f'{wind_speed} m/s')
                    col4.metric('Weather Condition', weather_condition)

            else:
                st.error(
                    f'API Error {response.status_code}: '
                    f'{response.text}'
                )

        except requests.RequestException as e:
            st.error(f'Network error: {e}')
        except (KeyError, IndexError, TypeError, ValueError) as e:
            st.error(f'Unable to process weather data: {e}')
