import unittest
from unittest.mock import patch, Mock
from app import FlaskApp
import json

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = FlaskApp()
        self.client = self.app.app.test_client()
        
    def test_home_endpoint(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'running')
        self.assertIsInstance(data['endpoints'], list)
        
    def test_forecast_missing_lat(self):
        response = self.client.get('/forecast?lon=21')
        self.assertEqual(response.status_code, 400)
        
    def test_forecast_missing_lon(self):
        response = self.client.get('/forecast?lat=52.2')
        self.assertEqual(response.status_code, 400)
        
    @patch('weatherClass.WeatherService.get_weather')
    def test_forecast_success(self, mock_get_weather):
        expected_data = {
            "date": "2024-01-24",
            "weatherCode": 1,
            "temperature2mMax": 20,
            "temperature2mMin": 10,
            "estimatedEnergy": 5.5
        }
        mock_get_weather.return_value = expected_data
        
        response = self.client.get('/forecast?lat=52.2&lon=21')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected_data)
        mock_get_weather.assert_called_once_with('52.2', '21')
        
    def test_weekly_summary_missing_params(self):
        response = self.client.get('/weekly_summary')
        self.assertEqual(response.status_code, 400)
        
    @patch('weeklySummaryClass.WeeklySummaryService.get_weather_summary')
    def test_weekly_summary_success(self, mock_get_summary):
        expected_data = {
            "averagePressure": 1013.25,
            "averageSunshineDuration": 28800,
            "maxTemperature": 25.5,
            "minTemperature": 15.5,
            "precipitationDays": 2,
            "weatherSummary": "bez opadów",
            "windAverage": 12.3
        }
        mock_get_summary.return_value = expected_data
        
        response = self.client.get('/weekly_summary?lat=52.2&lon=21')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, expected_data)
        mock_get_summary.assert_called_once_with('52.2', '21')

    @patch('requests.get')
    def test_api_integration(self, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"daily": {"time": []}}
        mock_requests.return_value = mock_response
        
        response = self.client.get('/forecast?lat=52.2&lon=21')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()