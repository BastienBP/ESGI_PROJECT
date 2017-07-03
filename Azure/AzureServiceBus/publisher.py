from azure.servicebus import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read("azureServiceBus.cfg")
azureNamespace = cfg.get("ConfigServiceBus","namespace")
azureAccountName = cfg.get("ConfigServiceBus","shared_access_key_name")
azureAccountKey = cfg.get("ConfigServiceBus","shared_access_key")

bus_service = ServiceBusService(
    service_namespace=azureNamespace,
    shared_access_key_name=azureAccountName,
    shared_access_key_value=azureAccountKey)

#creating the topic
bus_service.create_topic('pythontopic')

#creating the subscription
bus_service.create_subscription('pythontopic', 'messages')

#sending message:
msg = Message('My message'.encode('utf-8'))
bus_service.send_topic_message('pythontopic', msg)
