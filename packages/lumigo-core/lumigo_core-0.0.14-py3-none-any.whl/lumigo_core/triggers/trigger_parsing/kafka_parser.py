from typing import Any, Dict, List, Optional

from lumigo_core.logger import get_logger
from lumigo_core.lumigo_utils import ascii_to_string, is_number_list
from lumigo_core.triggers.trigger_parsing.event_trigger_base import (
    EventTriggerParser,
    ExtraKeys,
    TriggerType,
)


class KafkaEventTriggerParser(EventTriggerParser):
    @staticmethod
    def _should_handle(event: Dict[Any, Any]) -> bool:
        return bool(event.get("eventSource") == "SelfManagedKafka")

    @staticmethod
    def safe_extract_message_ids(event: Dict[Any, Any]) -> List[str]:
        message_ids = []
        try:
            for records in event.get("records", {}).values():
                for record in records:
                    for header in record.get("headers", []):
                        traceparent = header.get("traceparent")
                        if traceparent and is_number_list(traceparent):
                            traceparent_string = ascii_to_string(traceparent)
                            message_ids.append(traceparent_string)
        except Exception:
            get_logger().info("failed extracting topic name from first record")

        return message_ids

    @staticmethod
    def handle(event: Dict[Any, Any], target_id: Optional[str]) -> TriggerType:
        bootstrap_servers = event.get("bootstrapServers")
        resource = None
        try:
            first_record_key = list(event["records"].keys())[0]
            first_record = event["records"][first_record_key][0]
            resource = first_record["topic"]
        except Exception:
            get_logger().info("failed extracting topic name from first record")

        return EventTriggerParser.build_trigger(
            target_id=target_id,
            resource_type="kafka",
            from_message_ids=KafkaEventTriggerParser.safe_extract_message_ids(
                event=event
            ),
            extra={
                ExtraKeys.RESOURCE: resource,
                ExtraKeys.BOOTSTRAP_SERVERS: bootstrap_servers,
            },
        )
