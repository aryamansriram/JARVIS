from livekit.agents import llm
import logging
from typing import Annotated
from enum import Enum

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


class Rooms(Enum):
    LIVING_ROOM = "LIVING_ROOM"
    BEDROOM = "BEDROOM"
    KITCHEN = "KITCHEN"


class Functions(llm.FunctionContext):
    """
    This class consists of all functions
    that can be called by the created agent
    """

    def __init__(self):
        super().__init__()

        self.light_info = {
            Rooms.LIVING_ROOM: "OFF",
            Rooms.BEDROOM: "OFF",
            Rooms.KITCHEN: "OFF",
        }

    @llm.ai_callable(
        name="get_light_status",
        description="Returns the current status of the lights in the given room",
    )
    def get_light_status(
        self,
        room: Annotated[
            Rooms,
            llm.TypeInfo(
                description="Enum of the room whose light status is to be retrieved"
            ),
        ],
    ):
        logger.info("Getting light status ")
        logger.info(f"Found room {Rooms(room)}")
        logger.info(f"CurrentStatus of all rooms {self.light_info}")
        return self.light_info[Rooms(room)]

    @llm.ai_callable(
        name="set_light_status",
        description="Sets the status of the lights in the given room",
    )
    def set_light_status(
        self,
        room: Annotated[
            Rooms,
            llm.TypeInfo(
                description="Enum of the room whose light status is to be set"
            ),
        ],
        status: Annotated[
            str, llm.TypeInfo(description="Light status to be set for the given room")
        ],
    ):
        logger.info("Setting light status ")
        self.light_info[Rooms(room)] = status
        logger.info(f"Light status set to {self.light_info[Rooms(room)]}")
        return f"Light status set to {self.light_info[Rooms(room)]}"
