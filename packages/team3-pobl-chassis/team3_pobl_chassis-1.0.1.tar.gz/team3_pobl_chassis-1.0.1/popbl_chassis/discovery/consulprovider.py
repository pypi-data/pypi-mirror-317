import logging

import consul
import dns.resolver
import ifaddr


class ConsulProvider:
    
    consul_port: int= 8500
    consul_dns_port: int= 8600
    consul_host: str= None
    consul_instance: consul = None
    consul_resolver: dns.resolver = None
    ip: str= None
    logger: logging.Logger = None
    
    @classmethod
    async def create(cls, consul_host, logger):
        self = ConsulProvider()
        self.consul_host = consul_host
        self.logger = logger
        self.create_instance()
        self.create_resolver()
        self.set_ip()        
        return self
    
    def set_ip(self):
        ip = self.get_adapter_ip("eth0")  
        self.logger.info(f"service ip is {ip}")
        if ip is None:
            ip = "127.0.0.1"
        self.ip = ip
    
    def create_instance(self):
        self.consul_instance = consul.Consul(
            host=self.consul_host,
            port=self.consul_port
        )
        self.consul_instance.kv.put("aas_example_variable", "aas_example_value")
        
    def create_resolver(self):
        self.consul_resolver = dns.resolver.Resolver(configure=False)
        self.consul_resolver.port = self.consul_dns_port
        self.consul_resolver.nameservers = [str(self.consul_host)]

    @staticmethod
    def get_adapter_ip(nice_name):
        adapters = ifaddr.get_adapters()

        for adapter in adapters:
            if adapter.nice_name == nice_name and len(adapter.ips) > 0:
                return adapter.ips[0].ip

        return None

    def register_consul_service(self, service_name, service_port, service_id):
        self.logger.debug(f"Registering {service_name} service ({service_id})")
        self.consul_instance.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=self.ip,
            port=service_port,
            tags=["python", "microservice", "aas"],
            check={
                "http": 'http://{host}:{port}/health'.format(
                    host=self.ip,
                    port=service_port,
                    service_name=service_name
                ),
                "interval": '10s'
            }
        )
        self.logger.info(f"Registered {service_name} service ({service_id})")
        
        
    def get_consul_service(self, service_name):
        ret = {
            "Address": None,
            "Port": None
        }
        try:
            #  srv_results = consul_dns_resolver.query("{}.service.consul".format(service_name), "srv")
    
            srv_results = self.consul_resolver.resolve(
                "{}.service.consul".format(service_name),
                "srv"
            )  # SRV DNS query
            srv_list = srv_results.response.answer  # PORT - target_name relation
            a_list = srv_results.response.additional  # IP - target_name relation
    
            # DNS returns a list of replicas, supposedly sorted using Round Robin. We always get the 1st element: [0]
            srv_replica = srv_list[0][0]
            port = srv_replica.port
            target_name = srv_replica.target
    
            # From all the IPs, get the one with the chosen target_name
            for a in a_list:
                if a.name == target_name:
                    ret['Address'] = a[0]
                    ret['Port'] = port
                    break
    
        except dns.exception.DNSException as e:
            self.logger.error("Could not get service url: {}".format(e))
        return ret

    def get_consul_key_value_item(self,key):
        """Get consul item value for the given key. It only works for string items!"""
        index, data = self.consul_instance.kv.get(key)
        value = None
        if data and data['Value']:
            value = data['Value'].decode('utf-8')
        return key, value


    def get_consul_service_catalog(self):
        """List al consul services"""
        return self.consul_instance.catalog.services()
    
    
    def get_consul_service_replicas(self):
        """Get all services including replicas"""
        return self.consul_instance.agent.services()
    
    
    def unregister_service_from_consul(self, service_id):
        self.logger.debug(f"Unregistering service ({service_id})")
        self.consul_instance.agent.service.deregister(service_id)
        self.logger.info(f"Unregistered service ({service_id})")