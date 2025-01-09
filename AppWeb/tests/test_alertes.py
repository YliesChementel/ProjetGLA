import pytest
from unittest import mock
import smtplib
from app.alertes import *
from app.models import Alerte  
from flask import Flask
from unittest.mock import patch

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


def test_send_email_failure():
    """Test de l'échec de l'envoi d'email"""
    with patch('app.alertes.smtplib.SMTP') as mock_smtp:
        mock_server = mock_smtp.return_value
        mock_server.sendmail.side_effect = Exception("Erreur SMTP")
        with pytest.raises(smtplib.SMTPException):
            send_email("Test Subject", "Test Body", "test@example.com")

def test_send_email_alert_invalid_alert_type(app):
    with app.app_context():
        alerte = mock.Mock(spec=Alerte)
        alerte.crypto.name = "Bitcoin"
        alerte.user.email = "testuser@example.com"

        alert_type = "invalid_alert_type"
        current_value = 10000

        # Mock la fonction send_email
        with mock.patch('app.alertes.send_email') as mock_send_email, \
             mock.patch('builtins.print') as mock_print:  # Mock print pour capture les message d'avertissement
            send_email_alert(alerte, current_value, alert_type)

            # Veérifier que le send_email à été appelé
            expected_subject = f"Alerte pour Bitcoin - {alert_type}"
            expected_body = f"Alerte pour Bitcoin - Valeur: {current_value} (type inconnu)"
            mock_send_email.assert_called_once_with(expected_subject, expected_body, "testuser@example.com")

            # vérifier que l'avertissement est appelé
            mock_print.assert_called_once_with(f"Warning: alert_type '{alert_type}' non reconnu, envoi d'un message générique.")

