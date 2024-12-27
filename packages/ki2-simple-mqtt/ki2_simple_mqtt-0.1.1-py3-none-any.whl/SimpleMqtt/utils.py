from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass


def topic_matches_pattern(topic: str, pattern: str) -> bool:
    """
    Checks if an MQTT topic matches a given MQTT pattern.

    Args:
        topic (str): The topic to check (e.g., "home/livingroom/temperature").
        pattern (str): The pattern to match against (e.g., "home/+/temperature"
        or "home/#").

    Returns:
        bool: True if the topic matches the pattern, False otherwise.
    """
    # Split the topic and pattern into levels
    topic_levels = topic.split("/")
    pattern_levels = pattern.split("/")

    # If the pattern is longer than the topic
    if len(pattern_levels) > len(topic_levels):
        return False

    # Iterate through the pattern and topic levels
    for i, pattern_level in enumerate(pattern_levels):
        if pattern_level == "#":
            # "#" matches everything from this point onward
            return True

        if pattern_level != "+" and pattern_level != topic_levels[i]:
            # If the pattern level is neither "+" nor an exact match
            return False

    # Ensure both the topic and pattern are fully consumed
    return len(topic_levels) == len(pattern_levels)


def is_pattern_topic(topic: str) -> bool:
    """
    Checks if an MQTT topic contains a pattern (i.e., "+", "#").

    Args:
        topic (str): The topic to check (e.g., "home/livingroom/temperature" or
        "home/+/temperature").

    Returns:
        bool: True if the topic contains a pattern, False otherwise.
    """

    return "+" in topic or "#" in topic
