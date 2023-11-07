from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    rating: int
    status: str
    description: str

    def get_description_for(self, your_faction):
        enhanced_description = self.description.replace('you', your_faction)
        return f"This faction now considers {your_faction}, {self.status} and {enhanced_description}"


# Now, you can create instances of Status for each rating.
# can we can format all these descriptions to be ready to replace the you?
statuses = {
    3: Status(3, "Allies",
              "This faction will help you even if it’s not in their best interest to do so. They expect you to do the "
              "same for them."),
    2: Status(2, "Friendly",
              "This faction will help you if it doesn’t create serious problems for them. They expect you to do the "
              "same."),
    1: Status(1, "Helpful",
              "This faction will help you if it causes no problems or significant cost for them. They expect the same "
              "from you."),
    0: Status(0, "Neutral", "This faction has other concerns than you"),
    -1: Status(-1, "Interfering",
               "This faction will look for opportunities to cause trouble for you (or profit from your misfortune) as "
               "long as it causes no problems or significant cost for them. They expect the same from you."),
    -2: Status(-2, "Hostile",
               "This faction will look for opportunities to hurt you as long as it doesn’t create serious problems "
               "for them. They expect you to do the same, and take precautions against you."),
    -3: Status(-3, "at War",
               "This faction will go out of its way to hurt you even if it’s not in their best interest to do so. "
               "They expect you to do the same, and take precautions against you.")
}


def normalize_opinion(opinion: float) -> int:
    # Clamp the opinion to be within -3 to 3
    clamped_opinion = max(min(opinion, 3), -3)
    # Convert to integer to strip off the decimal part
    normalized_opinion = int(clamped_opinion)
    return normalized_opinion


def get_status(opinion: float) -> Status:
    return statuses[normalize_opinion(opinion)]
