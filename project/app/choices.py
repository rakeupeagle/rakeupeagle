from django.db.models import IntegerChoices


class RecipientStateChoices(IntegerChoices):
    ARCHIVED = -50, "Archived"
    # BLOCKED = -40, "Blocked"
    # IGNORED = -30, "Ignored"
    # INACTIVE = -10, "Inactive"
    NEW = 0, "New"
    INVITED = 5, "Invited"
    ACCEPTED = 7, "Accepted"
    CONFIRMED = 20, "Confirmed"
    ASSIGNED = 25, "Assigned"
    COMPLETED = 30, "Completed"
    DECLINED = 40, "Declined"
    CANCELLED = 50, "Cancelled"


class RecipientSizeChoices(IntegerChoices):
    SMALL = 110, "Small (1-15 bags)"
    MEDIUM = 120, "Medium (16-30 bags)"
    LARGE = 130, "Large (31+ bags)"


class TeamStateChoices(IntegerChoices):
    ARCHIVED = -50, "Archived"
    # BLOCKED = -40, "Blocked"
    # IGNORED = -30, "Ignored"
    # INACTIVE = -10, "Inactive"
    NEW = 0, "New"
    INVITED = 5, "Invited"
    ACCEPTED = 7, "Accepted"
    CONFIRMED = 20, "Confirmed"
    ASSIGNED = 25, "Assigned"
    COMPLETED = 30, "Completed"
    DECLINED = 40, "Declined"
    CANCELLED = 50, "Cancelled"


class TeamSizeChoices(IntegerChoices):
    SOLO = 105, "Solo (1 Adult)"
    XSMALL = 110, "Extra-Small (2-5 Adults)"
    SMALL = 120, "Small (6-10 Adults)"
    MEDIUM = 130, "Medium (11-15 Adults)"
    LARGE = 140, "Large (16-20 Adults)"
    XLARGE = 150, "Extra-Large (21+ Adults)"


class MessageStateChoices(IntegerChoices):
    NEW = 0, "New"
    SENT = 10, "Sent"
    READ = 20, "Read"


class DirectionChoices(IntegerChoices):
    INBOUND = 10, "Inbound"
    OUTBOUND = 20, "Outbound"


class EventStateChoices(IntegerChoices):
    ARCHIVE = -10, "Archive"
    NEW = 0, "New"
    CURRENT = 10, "Current"
    CLOSED = 20, "Closed"


class AssignmentStateChoices(IntegerChoices):
    FAILED = -20, "Failed"
    CANCELLED = -10, "Cancelled"
    NEW = 0, "New"
    ASSIGNED = 10, "Assigned"
    STARTED = 40, "Started"
    FINISHED = 50, "Finished"
