import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.platine import Platine

class TestBouton(unittest.TestCase):
    @patch('model.platine.Button')
    @patch('model.platine.MotionSensor')
    def setUp(self, mock_motion, mock_button):
        self.mock_button_class = mock_button
        self.mock_button_instance = MagicMock()
        mock_button.return_value = self.mock_button_instance
        
        mock_motion.return_value = MagicMock()
        
        self.platine = Platine()

    def test_bouton_initialisation(self):
        self.mock_button_class.assert_any_call(16, bounce_time=0.5)
        self.assertIsNotNone(self.platine.button_capte.when_pressed)

    @patch('model.platine.Button')
    @patch('model.platine.MotionSensor')
    def test_bouton_start_toggle(self, mock_motion, mock_button):
        mock_button_instance = MagicMock()
        mock_button.side_effect = [MagicMock(), mock_button_instance, MagicMock()]
        mock_motion.return_value = MagicMock()
        
        platine = Platine()
        
        self.assertFalse(platine.program_active)
        
        platine._handle_start_press()
        self.assertTrue(platine.program_active)
        
        platine._handle_start_press()
        self.assertFalse(platine.program_active)


if __name__ == '__main__':
    unittest.main()
