import pybreaker
import requests
from requests.exceptions import RequestException
from popbl_chassis.discovery.consulprovider import ConsulProvider


class CircuitBreaker:

    consul_provider: ConsulProvider = None
    logger = None
    circuit_breaker: pybreaker.CircuitBreaker = None

    @classmethod
    async def create(cls, logger, consul_provider: ConsulProvider):
        self = CircuitBreaker()
        self.logger = logger
        self.consul_provider = consul_provider
        self.circuit_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)
        return self

    def breaker_call(self, service_name):
        try:
            return self.circuit_breaker.call(self.check_healthcheck, service_name)
        except pybreaker.CircuitBreakerError as cbe:
            self.logger.error(f"Circuit Breaker is open for {service_name}: {cbe}")
            raise
        except Exception as e:
            self.logger.error(f"Error during healthcheck for {service_name}: {e}")
            raise

    def check_healthcheck(self, service_name):
        # Get service address and port from Consul
        ret = self.consul_provider.get_consul_service(f"_{service_name}._tcp")
        if not ret["Address"] or not ret["Port"]:
            self.logger.error(f"Service {service_name} not found in Consul")
            raise ValueError(f"Service {service_name} not found in Consul")

        # Make the request to the /health endpoint
        try:
            response = requests.get(f"http://{ret['Address']}:{ret['Port']}/health", timeout=5)

            # Raise an error if the status code is not 200
            if response.status_code != 200:
                self.logger.warning(f"Healthcheck for {service_name} returned {response.status_code}")
                raise ValueError(f"Healthcheck for {service_name} returned {response.status_code}")

            return True

        except RequestException as re:
            self.logger.error(f"Connection error with {service_name}: {re}")
            raise ValueError(f"Connection error with {service_name}: {re}")
