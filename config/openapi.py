from django.db.models import TextChoices


class Tags(TextChoices):
    # Framework
    EXPLORE = "explore", "Explore"
    SUBSCRIPTIONS = "subscriptions", "Subscriptions"
    STATS = "stats", "Stats"
    ACCOUNT_MODE = "account-mode", "Account Mode"
    READING_MODE = "reading-mode", "Reading Mode"
    COMMENTS = "comments", "Comments"
    PROFILE = "profile", "Profile"


TAGS = [{"name": name, "x-displayName": display} for name, display in Tags.choices]

TAG_GROUPS = [
    {
        "name": "Explore",
        "tags": [
            Tags.EXPLORE,
        ],
    },
    {
        "name": "subscriptions",
        "tags": [
            Tags.SUBSCRIPTIONS,
        ],
    },
    {
        "name": "Stats",
        "tags": [
            Tags.STATS,
        ],
    },
    {
        "name": "Account Mode",
        "tags": [
            Tags.ACCOUNT_MODE,
        ],
    },
    {
        "name": "Reading Mode",
        "tags": [
            Tags.READING_MODE,
        ],
    },
    {
        "name": "Comments",
        "tags": [
            Tags.COMMENTS,
        ],
    },
    {
        "name": "Profile",
        "tags": [
            Tags.PROFILE,
        ],
    },
]

EXTENSIONS_ROOT = {
    "x-tagGroups": TAG_GROUPS,
}
