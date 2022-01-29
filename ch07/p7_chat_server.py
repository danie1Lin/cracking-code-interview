# websocket server
# message handler
# Many user can in the same room send receive message.
import enum
import asyncio
from typing import Optional

class MessageQuery:
    from_id: Optional[int]
    to_id: Optional[int]
    type: Optional[int]
    after: Optional[int]

class Room:
    ID: int
    user_ids: list[int]
    messages: list[Message]

    def can_join(self, user):
        return True

    def add_message(self, message: Message):
        pass

class User:
    ID: int
    # can be denormalized like this
    latest_read: dict[Room, Message]

class Message:
    from_id: int
    to_id: int
    ID: int
    content: str
    timestamp: int 
    read_by: list[User]

    def parse(self, raw: str):
        pass

    def to_raw(self) -> str:
        return f'{}'

class Repository:
    def get_user(ID: int) -> User:
        pass

    def get_room(ID: int) -> Room:
        pass

    def save_room(room: Room):
        pass

    def save_msg(msg: Message):
        pass

    def get_msg_after(msg: Message) -> list[Message]:
        pass

class UserService:
    def get_users_from_room(id: int) -> list[User]:
        return [User()]

    def get_user(self, token: str) -> User:
        return User()

    def get_available_room(self) -> List[Room]:
        pass

    def join_room(self, user: User, room: Room):
        pass

    def get_user_room(self, user: User) -> Room:
        pass

class ChatService:
    repo: Repository

    def create_room(self, room: Room):
        pass

    def send_message(self, message: Message):
        self.repo.save_msg(message)

    def get_message(self, query: MessageQuery) -> list[Message]:
        # if request is large it might need cache or turn into push model
        pass

class OperationType(enum.Enum):
    Join=1
    Leave=2
    Setting=3
class RoomOperation:
    type: OperationType 

# if maintain websocket connection is more cheap and http reconnet overhead
class WebSocketHandler:
    pass

class HttpHandler:
    chat_svc: ChatService
    user_svc: UserService
    def handle_send(self, payload: str):
        self.chat_svc.send_message(self.transform_message(payload)) 

    def handle_get_message(self, payload: str) -> List[Message]:
        query = self.transform_query(payload)
        return self.chat_svc.get_message(query)

    def handle_get_available_room(self, payload: str):
        pass

    def handle_room_operation(self, payload: str):
        pass

    def transform_query(self, payload: str) -> MessageQuery:
        user = self.user_svc.get_user(payload)
        message = MessageQuery()
        message.from_id = user.id
        return MessageQuery()

    def transform_message(self, payload:str) -> Message:
        user = self.user_svc.get_user(payload)
        message = Message()
        message.from_id = user.id
        # assign destination
        return message

# Repository may use SQL database to save user and room
# message can use NoSQL to store because it don't need join operation and we can aslo be more scalable 
# we can also use cache system like redis to cache online user message to decrease database loading

# The hardest problem to deal?
# 1. When users growing a lot how the server endure the loading users polling latest messages?
# Q: when read operation is more then write we can write cache when writing to database.
# if write operation is the bottle neck we can split message by region into different databases and message id can use composition id can retrieve the region id.

# 2. How to delete the message already sent?
# Q: We can create a type of message call delete message. It will delete message from database and send to other user client to delete from devices.

# 3. How to record users latest message to prevent race condition?
# if we use timestamp we can still retrieve the messages in that second or millisecond and check it again

# 4. When a long term offline user online, the user will pull a lot of message. How to decease the latency and loading?
# we can split pages to retrieve other message
# client can send the request specific group the user will most likely to check also.

# 5. How to prevent DOS?
# A: 1. WAF 2. rate limmiter 3. circuit breaker
# waf will be the first layer it analyze from layer 4 / layer 7
# If the attack still into the application, we have rate limmiter to block mulbehaved clients
# If above strategies are useless then the last thing we can do it open the circuit breaker (maybe only certain area) from the load balancer or gateway to protect our resource from dieing.
