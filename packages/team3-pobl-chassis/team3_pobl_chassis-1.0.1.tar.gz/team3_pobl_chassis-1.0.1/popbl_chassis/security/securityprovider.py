import json
import os
from datetime import datetime, timedelta

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from popbl_chassis.discovery.consulprovider import ConsulProvider


class SecurityProvider:
    public_key=None
    private_key=None
    private_pem=None
    public_pem=None
    client_microservice_ip=None
    client_microservice_port=None
    consul_provider: ConsulProvider = None

    @classmethod
    async def create(cls, generate_keys: bool, ask_for_keys: bool, consul_service: ConsulProvider):
        self = SecurityProvider()
        if generate_keys:
            self.generate_keys()
            self.load_public_key()
            self.load_private_key()
            
        if ask_for_keys: 
            self.consul_provider = consul_service
            
        return self
    
    def is_public_key_loaded(self):
        return self.public_key is not None

    def get_public_key(self):
        service= self.consul_provider.get_consul_service("client")
        print(f"service_response:{service}")
        if service["Address"] is None or service["Port"] is None:
            raise ValueError("Client service not found.")
        response= requests.get(f"http://{service["Address"]}:{service["Port"]}/client/get/key")
        data = json.loads(response.text.strip('"').replace("\n", "\n"))
        self.public_key = data['public_key']
        return self.public_key

    @staticmethod
    def load_private_key():
        try:
            with open("private_key.pem", "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Private key file not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the private key: {e}")

    @staticmethod
    def load_public_key():
        try:
            with open("public_key.pem", "rb") as key_file:
                return key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Public key file not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the public key: {e}")


    def generate_keys(self):
        if os.path.exists("private_key.pem") and os.path.exists("public_key.pem"):
            print("Keys already exist. Skipping key generation.")
            return

        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open("private_key.pem", "wb") as f:
            f.write(self.private_pem)

        self.public_key = self.private_key.public_key()
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("public_key.pem", "wb") as f:
            f.write(self.public_pem)

        print("Keys generated successfully.")


    def create_token(self,data: dict, expires_delta: timedelta = timedelta(hours=3)):
        """Creates a JWT token with the given data and expiration."""
        private_key = self.load_private_key()
        data.update({"exp": datetime.utcnow() + expires_delta})
        headers = {
            "alg": "RS256",
            "typ": "JWT"
        }

        return jwt.encode(data, private_key, algorithm="RS256", headers=headers)


    def decode_token(self,token: str):
        """Decodes a JWT token and returns its payload."""
        
        if self.public_key is None:
            self.public_key = self.load_public_key()
            
        try:
            payload = jwt.decode(token, self.public_key, algorithms=["RS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

    @staticmethod
    def validate_role(payload: dict, role: str) -> bool:
        """Checks if the user has admin privileges."""
        return payload.get("role") == role or payload.get("role") == "admin"

    @staticmethod
    def validar_fecha_expiracion(payload: dict) -> bool:
        # Obtiene la fecha de expiración del token
        exp_timestamp_str = payload.get("fecha_expiracion")
        if not exp_timestamp_str:
            return False

        exp_timestamp_datetime = datetime.fromisoformat(exp_timestamp_str)
        exp_timestamp = exp_timestamp_datetime.timestamp()
        exp_datetime = datetime.utcfromtimestamp(exp_timestamp)

        # Comprueba si el token ha expirado
        return exp_datetime <= datetime.utcnow()