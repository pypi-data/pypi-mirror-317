# Copyright 2024 Lazar Jovanovic (https://github.com/Aragonski97)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import fastavro
from confluent_kafka import Producer, Message, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField, StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from structlog import get_logger
from pydantic import BaseModel
from confluent_kafka_config.topic_context import TopicContext
from confluent_kafka_config.registry_context import RegistryContext


class ProducerContext:

    def __init__(
            self,
            name: str,
            topic: dict,
            config: dict,
    ) -> None:

        self._logger = get_logger()
        self.name = name
        self.topic: TopicContext | None = None
        self._topic_config = topic
        self._config = config
        self._producer = Producer(self._config)

    def configure(
            self,
            registry_client: SchemaRegistryClient | None = None
    ):
        self._resolve_topic(registry_client)
        """
        TODO: Check if the count of partitions matches available partitions
        """

    def _resolve_topic(
            self,
            registry_client: SchemaRegistryClient | None = None
    ):
        if registry_client:
            registry_context = RegistryContext(
                registry_client=registry_client,
                schema_name=self._topic_config["schema_name"]
            )
            self.topic = TopicContext(
                name=self._topic_config["name"],
                partitions=self._topic_config["partitions"],
                registry_context = registry_context
            )
            self._configure_serialization()
            return
        self.topic = TopicContext(
            name=self._topic_config["name"],
            partitions=self._topic_config["partitions"]
        )
        return

    def _configure_json_serialization(self) -> None:
        """
        Not yet implemented
        """
        self._logger.error("Json schema not implemented yet!")
        raise TypeError("Json schema not implemented yet!")

    def _configure_avro_serialization(self) -> None:
        self.topic.registry_context.parsed_schema = fastavro.parse_schema(self.topic.registry_context.schema_dict)
        self.topic.value_serialization_method = AvroSerializer(
            schema_registry_client=self.topic.registry_context.registry_client,
            schema_str=self.topic.registry_context.schema_latest_version.schema.schema_str,
            to_dict=lambda obj, ctx: self.topic.registry_context.registered_model.model_dump(obj, context=ctx)
        )
        self.topic.key_serialization_method = StringSerializer('utf_8')
        self._logger.info(f"Avro serialization set for {self.name}")

    def _configure_protobuf_serialization(self) -> None:
        """
        Not yet implemented
        """
        self._logger.error("Protobuf schema not implemented yet!")
        raise TypeError("Protobuf schema not implemented yet!")

    def _configure_serialization(self) -> None:
        if not self.topic.registry_context:
            return
        match self.topic.registry_context.schema_type:
            case "JSON":
                self._configure_json_serialization()
            case "AVRO":
                self._configure_avro_serialization()
            case "PROTOBUF":
                self._configure_protobuf_serialization()
            case _:
                self._logger.error(f"Schema of type {self.topic.registry_context.schema_type} not recognized")
                raise ValueError(f"Schema of type {self.topic.registry_context.schema_type} not recognized")

    def produce(
            self,
            key: str,
            value: BaseModel,
    ) -> None:

        # Manually commit the offset for this partition only
        if not self.topic:
            self._logger.warning("Subject by that name doesn't exist")
            return
        try:
            if self.topic.registry_context:
                key = self.topic.key_serialization_method(key, SerializationContext(self.topic.name, MessageField.KEY))
                value = self.topic.value_serialization_method(
                    value, SerializationContext(self.topic.name, MessageField.VALUE)
                )
            else:
                key = self.topic.key_serialization_method(key, SerializationContext(self.topic.name, MessageField.KEY))
                value = value.model_dump_json(indent=True, exclude_none=True)
            # will override internal partitioner logic
            if self.topic.partitions:
                for partition in self.topic.partitions:
                    self._producer.produce(
                        topic=self.topic.name,
                        partition=partition,
                        key=key,
                        value=value,
                        on_delivery=self.delivery_report
                    )
            else:
                self._producer.produce(
                    topic=self.topic.name,
                    key=key,
                    value=value,
                    on_delivery=self.delivery_report
                )
                return
        except Exception as err:
            self._logger.warning(err)
            raise err

    def delivery_report(self, err: KafkaError, msg: Message):
        if err is not None:
            self._logger.info("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        self._logger.info('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))



