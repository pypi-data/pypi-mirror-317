from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
import uuid


@dataclass
class Mention:
    name: str
    number: str
    uuid: uuid.uuid4
    start: int
    length: int


# https://github.com/bbernhard/signal-cli-rest-api/blob/911b6867787fc79c878064dbf7db9cfa078b1144/src/datastructs/datastructs.go#L15
@dataclass
class SendMention(JSONWizard):
    start: int
    length: int
    author: str


@dataclass
class GroupInfo:
    groupId: str
    type: str


@dataclass
class DataMessage(JSONWizard):
    timestamp: int
    message: str
    expiresInSeconds: int
    viewOnce: bool
    mentions: list[Mention] = field(default_factory=list)
    groupInfo: GroupInfo | None = None


@dataclass
class ReceiptMessage:
    when: int
    isDelivery: bool
    isRead: bool
    isViewed: bool
    timestamps: list[int] = field(default_factory=list)


@dataclass
class Envelope(JSONWizard):
    source: str
    sourceNumber: str | None
    sourceUuid: uuid.uuid4
    sourceName: str
    sourceDevice: int
    timestamp: int
    dataMessage: DataMessage | None = None
    receiptMessage: ReceiptMessage | None = None


@dataclass
class Message(JSONWizard):
    account: str
    envelope: Envelope
