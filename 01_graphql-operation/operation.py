#╔═════════════════════════════════════════════════════════════════════════════╗
#║══════════════════❯ 💫 AxieAPI | GraphQL | Operation 💫
#╚═════════════════════════════════════════════════════════════════════════════╝


# ═════════════════════════════════════════════════════════════════════════════❯ 📦 Dependencies 📦
# ╚════════❯ 📦 Built-in Dependencies:
# ╚════════❯ 📦 External Dependencies:
# ╚════════❯ 📦 Internal Dependencies:
# ═════════════════════════════════════════════════════════════════════════════╝


# ═════════════════════════════════════════════════════════════════════════════❯ 📨 GraphQL Operation 📨
class GraphQLOperation:
    """
    A class that represents a GraphQL operation,
    and is used to generate a valid payload dictionary.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a 'GraphQLOperation' instance.

        Args:
            ➤ name (str): The operation name.

        Raises:
            ➤ TypeError: If 'name' is not a string.
            ➤ ValueError: If 'name' is not a valid operation name.
        """

        # ┗━━━━━➤ 🚦 Perform checks:
        self._check_operation(name)

        # ┗━━━━━➤ 📌 Define attributes:
        self._name = name
        self._query = self._set_query()
        self._variables = self._extract_query_vars()
        self._payload = {
            "operationName": self._name,
            "query": self._query,
            "variables": self._variables
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__module__}.{self.__class__.__name__} '{self.name}' object at {hex(id(self))}>"

    @classmethod
    def _check_operation(cls, name: str) -> None:
        """
        Checks if the operation name is valid.

        Args:
            ➤ name (str): The operation name.

        Raises:
            ➤ TypeError: If 'name' is not a string.
            ➤ ValueError: If 'name' is not a valid operation name.
        """

        valid_operations = [attr for attr in cls.ValidOperations.__dict__ if not attr.startswith('__')]
        if not isinstance(name, str):
            raise TypeError(f"Operation '{name}' ({type(name)}) is not valid. It must be a string.")
        elif name not in valid_operations:
            raise ValueError(f"Operation '{name}' not found. It must be a valid operation: {valid_operations}.")

    def _set_query(self) -> str:
        """
        Searches for the query string associated with the operation name.

        Returns:
            ➤ str: The query string for the operation.

        Raises:
            ➤ AttributeError: If the operation name can't be found in the 'ValidOperations' class.
        """

        return getattr(self.ValidOperations, self.name)

    def _extract_query_vars(self) -> dict:
        """
        Extracts all variables from the query string.

        Returns:
            ➤ dict: A dictionary of the query variables,
                    where each key is a variable (name:type).
        """

        def extract_substring(txt, start="<", end=">") -> str:
            """
            """

            return txt[txt.index(start)+len(start):txt.index(end)]

        # Return an empty dict if no variable can be found:
        if self.query.find("(") == -1:
            return {}

        # Extract variables from the query string:
        variables: str = extract_substring(self.query, start="(", end=")")
        # Clean up whitespaces:
        variables: str = "".join(variables.split())
        # List each variable 'key:value':
        variables: list = [var[1:] for var in variables.split(",")]
        # Convert the list of variables to a dict:
        variables: dict = dict(var.split(":") for var in variables)

        return variables

    @property
    def name(self) -> str:
        """
        """

        return self._name

    @property
    def query(self) -> str:
        """
        """

        return self._query

    @property
    def variables(self) -> dict:
        """
        """

        return self._variables

    @property
    def payload(self) -> dict:
        """
        """

        return self._payload

    # ═════════════════════════════════════════════════════════════════════════❯ 📨 Valid Operations 📨
    class ValidOperations:
        """
        A class that contains all valid GraphQL operations,
        with all fragments they can possibly use.
        """

        # ═════════════════════════════════════════════════════════════════════❯ 🪆 Valid Fragments 🪆
        class ValidFragments:
            """
            A class that contains all valid fragments used in GraphQL operations.
            """

            # ┗━━━━━➤ 💱 Marketplace:
            SettlementStats = (
                """
                fragment SettlementStats on SettlementStats {
                    count
                    axieCount
                    volume
                    volumeUsd
                    __typename
                }
                """
            )
            AssetInfo = (
                """
                fragment AssetInfo on Asset {
                    erc
                    address
                    id
                    quantity
                    orderId
                    __typename
                }
                """
            )
            OrderInfo = (
                """
                fragment OrderInfo on Order {
                    id
                    maker
                    kind
                    assets {
                        ...AssetInfo
                        __typename
                    }
                    expiredAt
                    paymentToken
                    startedAt
                    basePrice
                    endedAt
                    endedPrice
                    expectedState
                    nonce
                    marketFeePercentage
                    signature
                    hash
                    duration
                    timeLeft
                    currentPrice
                    suggestedPrice
                    currentPriceUsd
                    __typename
                }
                """
                + AssetInfo
            )
            OrdersInfo = (
                """
                fragment OrdersInfo on Orders {
                    total
                    quantity
                    data {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + OrderInfo
            )
            TransferRecordInSettledAuction = (
                """
                fragment TransferRecordInSettledAuction on TransferRecord {
                    txHash
                    timestamp
                    from
                    to
                    withPrice
                    withPriceUsd
                    fromProfile {
                        name
                        __typename
                    }
                    toProfile {
                        name
                        __typename
                    }
                    __typename
                }
                """
            )
            TransferHistoryInSettledAuction = (
                """
                fragment TransferHistoryInSettledAuction on TransferRecords {
                    total
                    results {
                        ...TransferRecordInSettledAuction
                        __typename
                    }
                    __typename
                }
                """
                + TransferRecordInSettledAuction
            )
            TransferRecords = (
                """
                fragment TransferRecords on TransferRecords {
                    total
                    results {
                        txHash
                        timestamp
                        from
                        to
                        withPrice
                        __typename
                    }
                    __typename
                }
                """
            )

            # ┗━━━━━➤ 👤 Account:
            AccountAddresses = (
                """
                fragment AccountAddresses on NetAddresses {
                    ronin
                    ethereum
                    __typename
                }
                """
            )
            AccountReferral = (
                """
                fragment AccountReferral on AccountReferral {
                    code
                    address
                    addedAt
                    __typename
                }
                """
            )
            PublicProfile = (
                """
                fragment PublicProfile on PublicProfile {
                    name
                    accountId
                    addresses {
                        ...AccountAddresses
                        __typename
                    }
                    __typename
                }
                """
                + AccountAddresses
            )
            PrivateProfile = (# 🔐
                """
                fragment PrivateProfile on AccountProfile {
                    name
                    accountId
                    addresses {
                        ...AccountAddresses
                        __typename
                    }
                    activated
                    email
                    settings {
                        unsubscribeNotificationEmail
                        __typename
                    }
                    referral {
                        ...AccountReferral
                        __typename
                    }
                    isScholar
                    __typename
                }
                """
                + AccountAddresses
                + AccountReferral
            )
            # << Only for Activity:
            BuyAxie = (
                """
                fragment BuyAxie on BuyAxie {
                    axieId
                    price
                    owner
                    txHash
                    __typename
                }
                """
            )
            ListAxie = (
                """
                fragment ListAxie on ListAxie {
                    axieId
                    priceFrom
                    priceTo
                    duration
                    txHash
                    __typename
                }
                """
            )
            UnlistAxie = (
                """
                fragment UnlistAxie on UnlistAxie {
                    axieId
                    txHash
                    __typename
                }
                """
            )
            GiftAxie = (
                """
                fragment GiftAxie on GiftAxie {
                    axieId
                    destination
                    txHash
                    __typename
                }
                """
            )
            MakeAxieOffer = (
                """
                fragment MakeAxieOffer on MakeAxieOffer {
                    axieId
                    price
                    txHash
                    __typename
                }
                """
            )
            CancelAxieOffer = (
                """
                fragment CancelAxieOffer on CancelAxieOffer {
                    axieId
                    txHash
                    __typename
                }
                """
            )
            SyncExp = (
                """
                fragment SyncExp on SyncExp {
                    axieId
                    exp
                    txHash
                    __typename
                }
                """
            )
            MorphToPetite = (
                """
                fragment MorphToPetite on MorphToPetite {
                    axieId
                    txHash
                    __typename
                }
                """
            )
            MorphToAdult = (
                """
                fragment MorphToAdult on MorphToAdult {
                    axieId
                    txHash
                    __typename
                }
                """
            )
            BreedAxies = (
                """
                fragment BreedAxies on BreedAxies {
                    sireId
                    matronId
                    lovePotionAmount
                    txHash
                    __typename
                }
                """
            )
            BuyLand = (
                """
                fragment BuyLand on BuyLand {
                    row
                    col
                    price
                    owner
                    txHash
                    __typename
                }
                """
            )
            ListLand = (
                """
                fragment ListLand on ListLand {
                    row
                    col
                    priceFrom
                    priceTo
                    duration
                    txHash
                    __typename
                }
                """
            )
            UnlistLand = (
                """
                fragment UnlistLand on UnlistLand {
                    row
                    col
                    txHash
                    __typename
                }
                """
            )
            GiftLand = (
                """
                fragment GiftLand on GiftLand {
                    row
                    col
                    destination
                    txHash
                    __typename
                }
                """
            )
            MakeLandOffer = (
                """
                fragment MakeLandOffer on MakeLandOffer {
                    row
                    col
                    price
                    txHash
                    __typename
                }
                """
            )
            CancelLandOffer = (
                """
                fragment CancelLandOffer on CancelLandOffer {
                    row
                    col
                    txHash
                    __typename
                }
                """
            )
            BuyItem = (
                """
                fragment BuyItem on BuyItem {
                    tokenId
                    itemAlias
                    price
                    owner
                    txHash
                    __typename
                }
                """
            )
            ListItem = (
                """
                fragment ListItem on ListItem {
                    tokenId
                    itemAlias
                    priceFrom
                    priceTo
                    duration
                    txHash
                    __typename
                }
                """
            )
            UnlistItem = (
                """
                fragment UnlistItem on UnlistItem {
                    tokenId
                    itemAlias
                    txHash
                    __typename
                }
                """
            )
            GiftItem = (
                """
                fragment GiftItem on GiftItem {
                    tokenId
                    itemAlias
                    destination
                    txHash
                    __typename
                }
                """
            )
            MakeItemOffer = (
                """
                fragment MakeItemOffer on MakeItemOffer {
                    tokenId
                    itemAlias
                    price
                    txHash
                    __typename
                }
                """
            )
            CancelItemOffer = (
                """
                fragment CancelItemOffer on CancelItemOffer {
                    tokenId
                    itemAlias
                    txHash
                    __typename
                }
                """
            )
            BuyBundle = (
                """
                fragment BuyBundle on BuyBundle {
                    listingIndex
                    price
                    owner
                    txHash
                    __typename
                }
                """
            )
            ListBundle = (
                """
                fragment ListBundle on ListBundle {
                    numberOfItems
                    priceFrom
                    priceTo
                    duration
                    txHash
                    __typename
                }
                """
            )
            UnlistBundle = (
                """
                fragment UnlistBundle on UnlistBundle {
                    listingIndex
                    txHash
                    __typename
                }
                """
            )
            MakeBundleOffer = (
                """
                fragment MakeBundleOffer on MakeBundleOffer {
                    listingIndex
                    price
                    txHash
                    __typename
                }
                """
            )
            CancelBundleOffer = (
                """
                fragment CancelBundleOffer on CancelBundleOffer {
                    listingIndex
                    txHash
                    __typename
                }
                """
            )
            AddLoomBalance = (
                """
                fragment AddLoomBalance on AddLoomBalance {
                    amount
                    senderAddress
                    receiverAddress
                    txHash
                    __typename
                }
                """
            )
            WithdrawFromLoom = (
                """
                fragment WithdrawFromLoom on WithdrawFromLoom {
                    amount
                    senderAddress
                    receiverAddress
                    txHash
                    __typename
                }
                """
            )
            AddFundBalance = (
                """
                fragment AddFundBalance on AddFundBalance {
                    amount
                    senderAddress
                    txHash
                    __typename
                }
                """
            )
            WithdrawFromFund = (
                """
                fragment WithdrawFromFund on WithdrawFromFund {
                    amount
                    receiverAddress
                    txHash
                    __typename
                }
                """
            )
            WithdrawRoninWeth = (
                """
                fragment WithdrawRoninWeth on WithdrawRoninWeth {
                    amount
                    receiverAddress
                    txHash
                    receiverAddress
                    __typename
                }
                """
            )
            TopupRoninWeth = (
                """
                fragment TopupRoninWeth on TopupRoninWeth {
                    amount
                    receiverAddress
                    txHash
                    receiverAddress
                    __typename
                }
                """
            )
            # >>
            Activity = (# 🔐
                """
                fragment Activity on Activity {
                    activityId
                    accountId
                    action
                    timestamp
                    data {
                        ... on BuyAxie {
                            ...BuyAxie
                            __typename
                        }
                        ... on ListAxie {
                            ...ListAxie
                            __typename
                        }
                        ... on UnlistAxie {
                            ...UnlistAxie
                            __typename
                        }
                        ... on GiftAxie {
                            ...GiftAxie
                            __typename
                        }
                        ... on MakeAxieOffer {
                            ...MakeAxieOffer
                            __typename
                        }
                        ... on CancelAxieOffer {
                            ...CancelAxieOffer
                            __typename
                        }
                        ... on SyncExp {
                            ...SyncExp
                            __typename
                        }
                        ... on MorphToPetite {
                            ...MorphToPetite
                            __typename
                        }
                        ... on MorphToAdult {
                            ...MorphToAdult
                            __typename
                        }
                        ... on BreedAxies {
                            ...BreedAxies
                            __typename
                        }
                        ... on BuyLand {
                            ...BuyLand
                            __typename
                        }
                        ... on ListLand {
                            ...ListLand
                            __typename
                        }
                        ... on UnlistLand {
                            ...UnlistLand
                            __typename
                        }
                        ... on GiftLand {
                            ...GiftLand
                            __typename
                        }
                        ... on MakeLandOffer {
                            ...MakeLandOffer
                            __typename
                        }
                        ... on CancelLandOffer {
                            ...CancelLandOffer
                            __typename
                        }
                        ... on BuyItem {
                            ...BuyItem
                            __typename
                        }
                        ... on ListItem {
                            ...ListItem
                            __typename
                        }
                        ... on UnlistItem {
                            ...UnlistItem
                            __typename
                            }
                        ... on GiftItem {
                            ...GiftItem
                            __typename
                        }
                        ... on MakeItemOffer {
                            ...MakeItemOffer
                            __typename
                        }
                        ... on CancelItemOffer {
                            ...CancelItemOffer
                            __typename
                        }
                        ... on ListBundle {
                            ...ListBundle
                            __typename
                        }
                        ... on UnlistBundle {
                            ...UnlistBundle
                            __typename
                        }
                        ... on BuyBundle {
                            ...BuyBundle
                            __typename
                        }
                        ... on MakeBundleOffer {
                            ...MakeBundleOffer
                            __typename
                        }
                        ... on CancelBundleOffer {
                            ...CancelBundleOffer
                            __typename
                        }
                        ... on AddLoomBalance {
                            ...AddLoomBalance
                            __typename
                        }
                        ... on WithdrawFromLoom {
                            ...WithdrawFromLoom
                            __typename
                        }
                        ... on AddFundBalance {
                            ...AddFundBalance
                            __typename
                        }
                        ... on WithdrawFromFund {
                            ...WithdrawFromFund
                            __typename
                        }
                        ... on TopupRoninWeth {
                            ...TopupRoninWeth
                            __typename
                        }
                        ... on WithdrawRoninWeth {
                            ...WithdrawRoninWeth
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
                """
                + BuyAxie
                + ListAxie
                + UnlistAxie
                + GiftAxie
                + MakeAxieOffer
                + CancelAxieOffer
                + SyncExp
                + MorphToPetite
                + MorphToAdult
                + BreedAxies
                + BuyLand
                + ListLand
                + UnlistLand
                + GiftLand
                + MakeLandOffer
                + CancelLandOffer
                + BuyItem
                + ListItem
                + UnlistItem
                + GiftItem
                + MakeItemOffer
                + CancelItemOffer
                + BuyBundle
                + ListBundle
                + UnlistBundle
                + MakeBundleOffer
                + CancelBundleOffer
                + AddLoomBalance
                + WithdrawFromLoom
                + AddFundBalance
                + WithdrawFromFund
                + WithdrawRoninWeth
                + TopupRoninWeth
            )

            # 🚧 Quid add fragment TransferHistoryInSettledAuction in SettledBrief?

            # ┗━━━━━➤ 🐱 Axie:
            AxieCardAbility = (
                """
                fragment AxieCardAbility on AxieCardAbility {
                    id
                    name
                    attack
                    defense
                    energy
                    description
                    backgroundUrl
                    effectIconUrl
                    __typename
                }
                """
            )
            AxiePart = (
                """
                fragment AxiePart on AxiePart {
                    id
                    name
                    class
                    type
                    specialGenes
                    stage
                    __typename
                }
                """
            )
            AxiePartWithAbilities = (
                """
                fragment AxiePartWithAbilities on AxiePart {
                    id
                    name
                    class
                    type
                    specialGenes
                    stage
                    abilities {
                        ...AxieCardAbility
                        __typename
                    }
                    __typename
                }
                """
                + AxieCardAbility
            )
            AxieBattleInfo = (
                """
                fragment AxieBattleInfo on AxieBattleInfo {
                    banned
                    banUntil
                    level
                    __typename
                }
                """
            )
            AxieBannedStatus = (
                """
                fragment AxieBannedStatus on AxieBattleInfo {
                    banned
                    __typename
                }
                """
            )
            AxieDetail = (
                """
                fragment AxieDetail on Axie {
                    id
                    name
                    image
                    figure {
                        atlas
                        model
                        image
                        __typename
                    }
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    class
                    parts {
                        ...AxiePartWithAbilities
                        __typename
                    }
                    bodyShape
                    potentialPoints {
                        beast
                        aquatic
                        plant
                        bug
                        bird
                        reptile
                        mech
                        dawn
                        dusk
                        __typename
                    }
                    breedCount
                    genes
                    newGenes
                    birthDate
                    title
                    stage
                    matronId
                    matronClass
                    sireId
                    sireClass
                    children {
                        id
                        name
                        image
                        owner
                        class
                        breedCount
                        stage
                        __typename
                    }

                    level
                    battleInfo {
                        ...AxieBattleInfo
                        __typename
                    }
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + AxiePartWithAbilities
                + AxieBattleInfo
                + OrderInfo
            )
            AxieBrief = (# = AxieDetail without [figure, bodyShape, potentialPoints, birthDate, title, matronId, matronClass, sireId, sireClass, children]
                """
                fragment AxieBrief on Axie {
                    id
                    name
                    image
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    class
                    parts {
                        ...AxiePart
                        __typename
                    }
                    breedCount
                    genes
                    newGenes
                    stage
                    level
                    battleInfo {
                        ...AxieBannedStatus
                        __typename
                    }
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + AxiePart
                + AxieBannedStatus
                + OrderInfo
            )
            AxieSettledBrief = (# = AxieBrief without [owner, ownerProfile, order]
                """
                fragment AxieSettledBrief on Axie {
                    id
                    name
                    image
                    class
                    parts {
                        ...AxiePart
                        __typename
                    }
                    breedCount
                    genes
                    newGenes
                    stage
                    level
                    battleInfo {
                        ...AxieBannedStatus
                        __typename
                    }
                    __typename
                }
                """
                + AxiePart
                + AxieBannedStatus
            )
            AxieBreedingBrief = (# = AxieDetail without [figure, potentialPoints, title, level, battleInfo, order]
                """
                fragment AxieBreedingBrief on Axie {
                    id
                    name
                    image
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    class
                    parts {
                        ...AxiePart
                        __typename
                    }
                    bodyShape
                    breedCount
                    genes
                    newGenes
                    birthDate
                    stage
                    matronId
                    matronClass
                    sireId
                    sireClass
                    children {
                        id
                        name
                        image
                        owner
                        class
                        breedCount
                        stage
                        __typename
                    }
                    __typename
                }
                """
                + AxiePart
            )

            # ┗━━━━━➤ 💍 Accessory:
            Equipment = (
                """
                fragment Equipment on Equipment {
                    alias
                    name
                    equipmentType
                    slot
                    rarity
                    collections
                    total
                    equippedTotal
                    minPrice
                    __typename
                }
                """
                #+ ValidFragments.OrderInfo
            )
            EquipmentInstance = (
                """
                fragment EquipmentInstance on EquipmentInstance {
                    id: tokenId
                    tokenId
                    alias
                    name
                    equipmentId
                    equipmentType
                    slot
                    owner
                    equippedBy
                    rarity
                    collections
                    __typename
                }
                """
            )
            EquipmentSettledBrief = (# 🚧
                """
                fragment EquipmentSettledBrief on EquipmentInstance {
                    alias
                    name
                    equipmentId
                    equipmentType
                    slot
                    owner
                    equippedBy
                    rarity
                    collections
                }
                """
            )
            EquipmentDetail = (# 🚧
                """
                fragment EquipmentDetail on EquipmentInstance {
                    tokenId
                    alias
                    equipmentId
                    equipmentType
                    name
                    slot
                    rarity
                    collections
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + OrderInfo
            )

            # ┗━━━━━➤ 🔋 Rune/Charm:
            Erc1155TokenDetail = (# 🚧
                """
                fragment Erc1155TokenDetail on Erc1155Token {
                    id: tokenId
                    tokenId
                    tokenType
                    tokenAddress
                    total
                    __typename
                }
                """
            )
            Erc1155TokenSettledBrief = (# 🚧
                """
                fragment Erc1155TokenSettledBrief on Erc1155Token {
                    erc1155TokenId: tokenId
                    id: tokenId
                    tokenType
                    tokenAddress
                    total
                    __typename
                }
                """
            )

            # ┗━━━━━➤ 🗺 Land:
            LandDetail = (
                """
                fragment LandDetail on LandPlot {
                    tokenId
                    col
                    row
                    landType
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + OrderInfo
            )
            #LandBrief = LandDetail.replace("LandDetail", "LandBrief")
            LandSettledBrief = (# = LandBrief without [owner, ownerProfile, order]
                """
                fragment LandSettledBrief on LandPlot {
                    tokenId
                    col
                    row
                    landType
                    __typename
                }
                """
            )
            LandBundleBrief = (# = LandSettledBrief without [tokenId]
                """
                fragment LandBundleBrief on LandPlot {
                    col
                    row
                    landType
                    __typename
                }
                """
            )

            # ┗━━━━━➤ 🏺 Item:
            ItemDetail = (
                """
                fragment ItemDetail on LandItem {
                    tokenId
                    itemAlias
                    itemId
                    name
                    figureURL
                    landType
                    rarity
                    effects
                    description
                    tokenType
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + OrderInfo
            )
            ItemBrief = (# = ItemDetail without [effects, description, tokenType]
                """
                fragment ItemBrief on LandItem {
                    tokenId
                    itemAlias
                    itemId
                    name
                    figureURL
                    landType
                    rarity
                    owner
                    ownerProfile {
                        name
                        __typename
                    }
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + OrderInfo
            )
            ItemSettledBrief = (# = ItemBrief without [owner, ownerProfile, order]
                """
                fragment ItemSettledBrief on LandItem {
                    tokenId
                    itemAlias
                    itemId
                    name
                    figureURL
                    landType
                    rarity
                    __typename
                }
                """
            )
            ItemBundleBrief = (# = ItemSettledBrief without [tokenId]
                """
                fragment ItemBundleBrief on LandItem {
                    itemAlias
                    itemId
                    name
                    figureURL
                    landType
                    rarity
                    __typename
                }
                """
            )

            # ┗━━━━━➤ 🎁 Bundle:
            BundleDetail = (
                """
                fragment BundleDetail on Bundle {
                    listingIndex
                    name
                    items {
                        ...LandBundleBrief
                        ...ItemBundleBrief
                        __typename
                    }
                    owner
                    order {
                        ...OrderInfo
                        __typename
                    }
                    __typename
                }
                """
                + LandBundleBrief
                + ItemBundleBrief
                + OrderInfo
            )
            BundleSettledBrief = (
                """
                fragment BundleSettledBrief on Bundle {
                    listingIndex
                    name
                    items {
                        ...LandBundleBrief
                        ...ItemBundleBrief
                        __typename
                    }
                    __typename
                }
                """
                + LandBundleBrief
                + ItemBundleBrief
            )
        #╚═════════════════════════════════════════════════════════════════════╝

        # ┗━━━━━➤ 🔐 Authentication:
        CreateRandomMessage = (
            """
            mutation CreateRandomMessage {
                createRandomMessage
            }
            """
        )
        CreateAccessTokenWithSignature = (
            """
            mutation CreateAccessTokenWithSignature(
                $input: SignatureInput!
            )
            {
                createAccessTokenWithSignature(
                    input: $input
                )
                {
                    newAccount
                    result
                    accessToken
                    __typename
                }
            }
            """
        )

        # ┗━━━━━➤ 💱 Marketplace:
        # Stats:
        GetSettlementStats = (
            """
            query GetSettlementStats {
                marketStats {
                    last24Hours {
                        ...SettlementStats
                        __typename
                    }
                    last7Days {
                        ...SettlementStats
                        __typename
                    }
                    last30Days {
                        ...SettlementStats
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.SettlementStats
        )
        GetOverallStats = (
            """
            query GetOverallStats {
                overallMarketStats {
                    newAxies {
                        last7D
                        allTime
                        __typename
                    }
                    originBattles {
                        last7D
                        allTime
                        __typename
                    }
                    mkpVolume {
                        last7D
                        allTime
                        __typename
                    }
                    mkpTxs {
                        last7D
                        allTime
                        __typename
                    }
                    __typename
                }
                tokensStats {
                    axie {
                        totalSupply
                        holders
                        __typename
                    }
                    __typename
                }
            }
            """
        )
        GetTopAllSales = (
            """
            query GetTopAllSales(
                $item_type: TokenType!,
                $period_type: PeriodType!,
                $size: Int!
            )
            {
                topSales(
                    tokenType: $item_type,
                    periodType: $period_type,
                    size: $size
                )
                {
                    results {
                        orderId
                        settlePrice
                        settlePriceUsd
                        timestamp
                        tokenAsset {
                            __typename
                            ... on Axie {
                                ...AxieSettledBrief
                                __typename
                            }
                            ... on EquipmentInstance {
                                ...EquipmentSettledBrief
                                __typename
                            }
                            ... on Erc1155Token {
                                ...Erc1155TokenSettledBrief
                                __typename
                            }
                            ... on LandPlot {
                                ...LandSettledBrief
                                __typename
                            }
                            ... on LandItem {
                                ...ItemSettledBrief
                                __typename
                            }
                        }
                        __typename
                    }
                __typename
                }
            }
            """
            + ValidFragments.AxieSettledBrief
            + ValidFragments.EquipmentSettledBrief
            + ValidFragments.Erc1155TokenSettledBrief.replace("id: tokenId", "") # This operation doesn't accept 'id' from this fragment.
            + ValidFragments.LandSettledBrief
            + ValidFragments.ItemSettledBrief
        )
        GetTopSales = (
            """
            query GetTopSales(
                $item_type: TokenType!,
                $period_type: PeriodType!,
                $isAxie: Boolean = false,
                $isEquipment: Boolean = false,
                $isErc1155: Boolean = false,
                $isLandPlot: Boolean = false,
                $isLandItem: Boolean = false,
                $size: Int!
            )
            {
                topSales(
                    tokenType: $item_type,
                    periodType: $period_type,
                    size: $size
                )
                {
                    results {
                        orderId
                        settlePrice
                        settlePriceUsd
                        timestamp
                        axie: tokenAsset @include(if: $isAxie) {
                            ... on Axie {
                                ...AxieSettledBrief
                                __typename
                            }
                            __typename
                        }
                        equipment: tokenAsset @include(if: $isEquipment) {
                            ... on EquipmentInstance {
                                ...EquipmentSettledBrief
                                __typename
                            }
                            __typename
                        }
                        erc1155: tokenAsset @include(if: $isErc1155) {
                            ... on Erc1155Token {
                                ...Erc1155TokenSettledBrief
                                __typename
                            }
                            __typename
                        }
                        landPlot: tokenAsset @include(if: $isLandPlot) {
                            ... on LandPlot {
                                ...LandSettledBrief
                                __typename
                            }
                            __typename
                        }
                        landItem: tokenAsset @include(if: $isLandItem) {
                            ... on LandItem {
                                ...ItemSettledBrief
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                __typename
                }
            }
            """
            + ValidFragments.AxieSettledBrief
            + ValidFragments.EquipmentSettledBrief
            + ValidFragments.Erc1155TokenSettledBrief
            + ValidFragments.LandSettledBrief
            + ValidFragments.ItemSettledBrief
        )
        GetExchangeRates = (
            """
            query GetExchangeRates {
                exchangeRate {
                    eth {
                        usd
                        __typename
                    }
                    slp {
                        usd
                        __typename
                    }
                    ron {
                        usd
                        __typename
                    }
                    axs {
                        usd
                        __typename
                    }
                    usd {
                        usd
                        __typename
                    }
                    __typename
                }
            }
            """
        )

        # Recently Listed:
        GetRecentlyListedAxies = (
            """
            query GetRecentlyListedAxies(
                $auctionType: AuctionType,
                $criteria: AxieSearchCriteria,
                $sort: SortBy,
                $from: Int,
                $size: Int
            )
            {
                axies(
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size,
                )
                {
                    total
                    results {
                        ...AxieBrief
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.AxieBrief
        )
        GetRecentlyListedErc1155Tokens = (
            """
            query GetRecentlyListedErc1155Tokens(
                $tokenType: Erc1155Type!,
                $from: Int,
                $size: Int
            )
            {
                erc1155Token(
                    tokenType: $tokenType
                )
                {
                    ...Erc1155TokenDetail
                    orders(
                        sort: Latest,
                        from: $from,
                        size: $size
                    )
                    {
                        ...OrdersInfo
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.Erc1155TokenDetail
            + ValidFragments.OrdersInfo
        )
        GetRecentlyListedLands = (
            """
            query GetRecentlyListedLands(
                $auctionType: AuctionType,
                $criteria: LandSearchCriteria,
                $sort: SortBy!,
                $from: Int!,
                $size: Int!
            )
            {
                lands(
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...LandDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.LandDetail
        )
        GetRecentlyListedItems = (
            """
            query GetRecentlyListedItems(
                $auctionType: AuctionType,
                $criteria: ItemSearchCriteria,
                $sort: SortBy,
                $from: Int,
                $size: Int
            )
            {
                items(
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...ItemBrief
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.ItemBrief
        )
        GetRecentlyListedBundles = (
            """
            query GetRecentlyListedBundles(
                $criteria: BundleSearchCriteria,
                $sort: SortBy,
                $from: Int!,
                $size: Int!
            )
            {
                bundles(
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...BundleDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.BundleDetail
        )
        GetAccessoriesMarketplace = (# 🚧
            """
            query GetAccessoriesMarketplace(
            	$from: Int!,
            	$size: Int!,
            	$auctionType: AuctionType
            )
            {
            	equipments(
            		from: $from,
            		size: $size,
            		auctionType: $auctionType
            	)
            	{
            		total
            		results {
            			id: alias
            			alias
            			name
            			equipmentType
            			slot
            			rarity
            			collections
            			minPrice
            			__typename
            		}
            		__typename
            	}
            }
            """
        )
        GetRecentlyListedAccessoriesV0 = (# 🚧
            """
            query GetRecentlyListedAccessories(
                $owner: String,
                $auctionType: AuctionType,
                $sort: SortBy,
                $from: Int!,
                $size: Int!
            )
            {
                equipmentInstances(
                    auctionType: $auctionType
                    from: $from
                    sort: $sort
                    size: $size
                    owner: $owner
                )
                {
                    total
                    results {
                        ...EquipmentSettledBrief
                        __typename
                    }
                    __typename
                }
            }

            fragment EquipmentSettledBrief on EquipmentInstance {
                tokenId
                name
                rarity
                alias
                collections
                slot
                order {
                    id
                    currentPrice
                    currentPriceUsd
                    startedAt
                    __typename
                }
                __typename
            }
            """
        )
        GetRecentlyListedAccessories = (# 🚧
            """
            query GetRecentlyListedAccessories(
                $auctionType: AuctionType,
                $sort: SortBy,
                $from: Int!,
                $size: Int!
            )
            {
                equipmentInstances(
                    auctionType: $auctionType,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...EquipmentDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.EquipmentDetail
        )
        GetAccessoryOrders = (# 🚧
            """
            query GetAccessoryOrders(
                $equipmentType: Int!,
                $owner: String,
                $from: Int!,
                $size: Int!,
                $sort: SortBy!,
                $auctionType: AuctionType
            )
            {
                equipment(
                    owner: $owner
                    equipmentType: $equipmentType
                    auctionType: $auctionType
                )
                {
                    total
                    instances(
                        from: $from,
                        size: $size,
                        sort: $sort
                    )
                    {
                        ...EquipmentInstance
                        key: tokenId
                        order {
                            ...OrderInfo
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
        )

        # Recently Sold:
        GetRecentlySoldAxies = (
            """
            query GetRecentlySoldAxies(
                $from: Int,
                $size: Int
            )
            {
                settledAuctions {
                    axies(
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...AxieSettledBrief
                            transferHistory {
                                ...TransferHistoryInSettledAuction
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.AxieSettledBrief
            + ValidFragments.TransferHistoryInSettledAuction
        )
        GetRecentlySoldAccessories = (# 🚧
            """
            query GetRecentlySoldAccessories(
                $from: Int!,
                $size: Int!
            )
            {
                settledAuctions {
                    equipments(
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...EquipmentSettledBrief
                            transferHistory {
                                ...EquipmentTransferRecords
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }

            fragment EquipmentSettledBrief on EquipmentInstance {
                tokenId
                name
                rarity
                alias
                collections
                slot
                order {
                    id
                    currentPrice
                    currentPriceUsd
                    startedAt
                    __typename
                }
                __typename
            }

            fragment EquipmentTransferRecords on TransferRecords {
                total
                results {
                    from
                    to
                    txHash
                    timestamp
                    withPrice
                    withPriceUsd
                    fromProfile {
                        name
                        __typename
                    }
                    toProfile {
                        name
                        __typename
                    }
                    __typename
                }
                __typename
            }
            """
        )
        GetRecentlySoldErc1155Tokens = (
            """
            query GetRecentlySoldErc1155Tokens(
                $tokenType: Erc1155Type!,
                $from: Int,
                $size: Int
            )
            {
                settledAuctions {
                    erc1155Tokens(
                        tokenType: $tokenType,
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...Erc1155TokenSettledBrief
                            transferHistory {
                                ...TransferHistoryInSettledAuction
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.Erc1155TokenSettledBrief
            + ValidFragments.TransferHistoryInSettledAuction
        )
        GetRecentlySoldLands = (
            """
            query GetRecentlySoldLands(
                $from: Int,
                $size: Int
            )
            {
                settledAuctions {
                    lands(
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...LandSettledBrief
                            transferHistory {
                                ...TransferHistoryInSettledAuction
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.LandSettledBrief
            + ValidFragments.TransferHistoryInSettledAuction
        )
        GetRecentlySoldItems = (
            """
            query GetRecentlySoldItems(
                $from: Int,
                $size: Int
            )
            {
                settledAuctions {
                    items(
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...ItemSettledBrief
                            transferHistory {
                                ...TransferHistoryInSettledAuction
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.ItemSettledBrief
            + ValidFragments.TransferHistoryInSettledAuction
        )
        GetRecentlySoldBundles = (
            """
            query GetRecentlySoldBundles(
                $from: Int,
                $size: Int
            )
            {
                settledAuctions {
                    bundles(
                        from: $from,
                        size: $size
                    )
                    {
                        total
                        results {
                            ...BundleSettledBrief
                            transferHistory {
                                ...TransferHistoryInSettledAuction
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.BundleSettledBrief
            + ValidFragments.TransferHistoryInSettledAuction
        )

        # Minimum Price:
        GetMinPriceErc1155Tokens = (
            """
            query GetMinPriceErc1155Tokens(
                $from: Int,
                $size: Int
            )
            {
                erc1155Tokens(
                    from: $from,
                    size: $size
                )
                {
                    results {
                        id: tokenId
                        tokenId
                        tokenType
                        minPrice
                        __typename
                    }
                    __typename
                }
            }
            """
        )
        GetMinPriceAxie = (
            """
            query GetMinPriceAxie(
                $axieId: ID!
            )
            {
                axie(
                    axieId: $axieId
                )
                {
                    id
                    minPrice
                    __typename
                }
            }
            """
        )

        # Order:
        CreateOrder = (# 🔐
            """
            mutation CreateOrder(
                $order: InputOrder!,
                $signature: String!
            )
            {
                createOrder(
                    order: $order,
                    signature: $signature
                )
                {
                    ...OrderInfo
                    __typename
                }
            }
            """
            + ValidFragments.OrderInfo
        )

        # ┗━━━━━➤ 👤 Account:
        GetPublicProfileWithRoninAddress = (
            """
            query GetPublicProfileWithRoninAddress(
                $roninAddress: String!
            )
            {
                publicProfileWithRoninAddress(
                    roninAddress: $roninAddress
                )
                {
                    ...PublicProfile
                    __typename
                }
            }
            """
            + ValidFragments.PublicProfile
        )
        GetPublicProfileWithAccountID = (
            """
            query GetPublicProfileWithAccountID(
                $accountId: UUID!
            )
            {
                publicProfile(
                    id: $accountId
                )
                {
                    ...PublicProfile
                    __typename
                }
            }
            """
            + ValidFragments.PublicProfile
        )
        GetPrivateProfile = (# 🔐
            """
            query GetPrivateProfile {
                profile {
                    ...PrivateProfile
                    __typename
                }
            }
            """
            + ValidFragments.PrivateProfile
        )
        GetActivityLog = (# 🔐
            """
            query GetActivityLog(
                $from: Int,
                $size: Int
            )

            {
                profile {
                    activities(
                        from: $from,
                        size: $size
                    )
                    {
                        ...Activity
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.Activity
        )
        AddActivity = (# 🔐
            """
            mutation AddActivity(
                $action: Action!,
                $data: ActivityDataInput!
            )
            {
                createActivity(
                    action: $action,
                    data: $data
                )
                {
                    result
                    __typename
                }
            }
            """
        )
        UpdateProfileName = (# 🔐
            """
            mutation UpdateProfileName(
                $name: String!
            )
            {
                updateProfileName(
                    name: $name
                )
                {
                    accountProfile {
                        ...PrivateProfile
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.PrivateProfile
        )
        UpdatePassword = (# 🔐
            """
            mutation UpdatePassword(
                $password: String!,
                $oldPassword: String!
            )
            {
                updatePassword(
                    newPassword: $password,
                    password: $oldPassword
                )
                {
                    result
                    __typename
                }
            }
            """
        )

        GetOwnerAxieList = (
            """
            query GetOwnerAxieList(
                $owner: String,
                $auctionType: AuctionType,
                $criteria: AxieSearchCriteria,
                $sort: SortBy,
                $from: Int,
                $size: Int
            )
            {
                axies(
                    owner: $owner,
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...AxieBrief
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.AxieBrief
        )
        GetOwnerAxieBreederList = (
            """
            query GetOwnerAxieBreederList(
                $owner: String,
                $auctionType: AuctionType,
                $criteria: AxieSearchCriteria,
                $sort: SortBy,
                $from: Int,
                $size: Int
            )
            {
                axies(
                    owner: $owner,
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...AxieBreedingBrief
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.AxieBreedingBrief
        )
        GetOwnerAccessoryList = (# 🚧
            """
            query GetOwnerAccessoryList(
                $owner: String,
                $auctionType: AuctionType,
                $sort: SortBy!,
                $from: Int!,
                $size: Int!,
                $includeInstances: Boolean = false,
                $instancesFrom: Int,
                $instancesSize: Int,
                $includeEquippedTotal: Boolean = false,
                $includeEquippedBy: Boolean = false
            )
            {
                equipments(
                    owner: $owner,
                    auctionType: $auctionType,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...Equipment
                        instances(
                            size: $instancesSize,
                            from: $instancesFrom,
                            sort: $sort
                        )
                        @include(if: $includeInstances) {
                            id: tokenId
                            tokenId
                            alias
                            name
                            equipmentId
                            equipmentType
                            slot
                            rarity
                            collections
                            owner
                            equippedBy @include(if: $includeEquippedBy)
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }

            fragment Equipment on Equipment {
              alias
              name
              equipmentType
              slot
              rarity
              collections
              total
              equippedTotal @include(if: $includeEquippedTotal)
              lowestUnequippedTokenId @include(if: $includeEquippedTotal)
              minPrice
              __typename
            }
            """
        )
        GetOwnerAccessoryListV2 = (# 🚧
            """
            query GetOwnerAccessoryList(
                $equipmentType: Int!,
                $owner: String,
                $from: Int!,
                $size: Int!,
                $sort: SortBy!,
                $auctionType: AuctionType,
                $includeOrder: Boolean = false,
                $includeInstances: Boolean = false
            )
            {
                equipment(
                    owner: $owner
                    equipmentType: $equipmentType
                    auctionType: $auctionType
                )
                {
                    ...Equipment
                    instances(
                        from: $from,
                        size: $size,
                        sort: $sort
                    )
                    @include(
                        if: $includeInstances
                    )
                    {
                        ...EquipmentInstance
                        order @include(
                            if: $includeOrder
                        )
                        {
                            ...OrderInfo
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.Equipment
            + ValidFragments.EquipmentInstance
        )
        GetOwnerErc1155TokenList = (
            """
            query GetOwnerErc1155TokenList(
                $owner: String!,
                $from: Int!,
                $size: Int!
            )
            {
                erc1155Tokens(
                    owner: $owner,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...Erc1155TokenDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.Erc1155TokenDetail
        )
        GetOwnerLandList = (
            """
            query GetOwnerLandList(
                $owner: String,
                $auctionType: AuctionType,
                $criteria: LandSearchCriteria,
                $sort: SortBy!,
                $from: Int!,
                $size: Int!
            )
            {
                lands(
                    owner: $owner,
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...LandDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.LandDetail
        )
        GetOwnerItemList = (
            """
            query GetOwnerItemList(
                $owner: String,
                $auctionType: AuctionType,
                $criteria: ItemSearchCriteria,
                $sort: SortBy,
                $from: Int,
                $size: Int
            )
            {
                items(
                    owner: $owner,
                    auctionType: $auctionType,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...ItemBrief
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.ItemBrief
        )
        GetOwnerBundleList = (
            """
            query GetOwnerBundleList(
                $seller: String,
                $criteria: BundleSearchCriteria,
                $sort: SortBy,
                $from: Int!,
                $size: Int!
            )
            {
                bundles(
                    seller: $seller,
                    criteria: $criteria,
                    sort: $sort,
                    from: $from,
                    size: $size
                )
                {
                    total
                    results {
                        ...BundleDetail
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.BundleDetail
        )

        # ┗━━━━━➤ 🐱 Axie:
        GetAxieDetail = (
            """
            query GetAxieDetail(
                $axieId: ID!
            )
            {
                axie(
                    axieId: $axieId
                )
                {
                    ...AxieDetail
                    __typename
                }
            }
            """
            + ValidFragments.AxieDetail
            )
        GetAxieBrief = (
            """
            query GetAxieBrief(
                $axieId: ID!
            )
            {
                axie(
                    axieId: $axieId
                )
                {
                    ...AxieBrief
                    __typename
                }
            }
            """
            + ValidFragments.AxieBrief
        )
        GetAxieBreedingBrief = (
            """
            query GetAxieBreedingBrief(
                $axieId: ID!
            )
            {
                axie(
                    axieId: $axieId
                )
                {
                    ...AxieBreedingBrief
                    __typename
                }
            }
            """
            + ValidFragments.AxieBreedingBrief
        )
        GetParentsBrief = (
            """
            query GetParentsBrief(
                $matronId: ID!,
                $sireId: ID!
            )
            {
                matron: axie(
                    axieId: $matronId
                )
                {
                    ...AxieBreedingBrief
                    __typename
                }
                sire: axie(
                    axieId: $sireId
                )
                {
                    ...AxieBreedingBrief
                    __typename
                }
            }
            """
            + ValidFragments.AxieBreedingBrief
        )
        RenameAxie = (# 🔐
            """
            mutation RenameAxie(
                $axieId: ID!,
                $name: String!
            )
            {
                renameAxie(
                    axieId: $axieId,
                    name: $name
                )
                {
                    result
                    __typename
                }
            }
            """
        )
        MorphAxie = (# 🔐
            """
            mutation MorphAxie(
                $axieId: ID!,
                $owner: String!,
                $signature: String!
            )
            {
                morphAxie(
                    axieId: $axieId,
                    owner: $owner,
                    signature: $signature
                )
            }
            """
        )

        # ┗━━━━━➤ 💍 Accessory:
        # ...

        # ┗━━━━━➤ 🔋 Rune/Charm:
        GetErc1155TokenDetail = (
            """
            query GetErc1155TokenDetail(
                $tokenType: Erc1155Type!,
                $tokenId: String!,
                $owner: String
            )
            {
                erc1155Token(
                    tokenType: $tokenType,
                    tokenId: $tokenId,
                    owner: $owner
                )
                {
                    ...Erc1155TokenDetail
                    __typename
                }
            }
            """
            + ValidFragments.Erc1155TokenDetail
        )

        # ┗━━━━━➤ 🗺 Land:
        GetLandDetail = (
            """
            query GetLandDetail(
                $col: Int!,
                $row: Int!
            )
            {
                land(
                    col: $col,
                    row: $row
                )
                {
                    ...LandDetail
                    __typename
                }
            }
            """
            + ValidFragments.LandDetail
        )

        # ┗━━━━━➤ 🏺 Item:
        GetItemDetail = (
            """
            query GetItemDetail(
                $itemAlias: String!,
                $itemId: Int!
            )
            {
                item(
                    itemAlias: $itemAlias,
                    itemId: $itemId
                )
                {
                    ...ItemDetail
                    __typename
                }
            }
            """
            + ValidFragments.ItemDetail
        )
        GetItemBrief = (
            """
            query GetItemBrief(
                $itemAlias: String!,
                $itemId: Int!
            )
            {
                item(
                    itemAlias: $itemAlias,
                    itemId: $itemId
                )
                {
                    ...ItemBrief
                    __typename
                }
            }
            """
            + ValidFragments.ItemBrief
        )

        # ┗━━━━━➤ 🎁 Bundle:
        GetBundleDetail = (
            """
            query GetBundleDetail(
                $listingIndex: Int!
            )
            {
                bundle(
                    listingIndex: $listingIndex
                )
                {
                    ...BundleDetail
                    __typename
                }
            }
            """
            + ValidFragments.BundleDetail
        )

        # ┗━━━━━➤ 📖 TransferHistory:
        GetAxieTransferHistory = (# 🚧
            """
            query GetAxieTransferHistory(
                $axieId: ID!,
                $from: Int!,
                $size: Int!
            )
            {
                axie(
                    axieId: $axieId
                )
                {
                    id
                    transferHistory(
                        from: $from,
                        size: $size
                    )
                    {
                        ...TransferRecords
                        __typename
                    }
                    ethereumTransferHistory(
                        from: $from,
                        size: $size
                    )
                    {
                        ...TransferRecords
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.TransferRecords
        )
        GetErc1155TokenOrders = (# 🚧
            """
            query GetErc1155TokenOrders(
                $tokenId: String!,
                $tokenType: Erc1155Type!,
                $maker: String,
                $from: Int!,
                $size: Int!,
                $sort: SortBy!,
                $owner: String
            )
            {
                erc1155Token(
                    tokenType: $tokenType,
                    tokenId: $tokenId,
                    owner: $owner
                )
                {
                    id: tokenId
                    tokenId
                    orders(
                        maker: $maker,
                        from: $from,
                        size: $size,
                        sort: $sort
                    )
                    {
                        ...OrdersInfo
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.OrdersInfo
        )
        GetLandTransferHistory = (# 🚧
            """
            query GetLandTransferHistory(
                $col: Int!,
                $row: Int!,
                $from: Int!,
                $size: Int!
            )
            {
                land(
                    col: $col,
                    row: $row
                )
                {
                    tokenId
                    transferHistory(
                        from: $from,
                        size: $size
                    )
                    {
                        ...TransferRecords
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.TransferRecords
        )
        GetItemTransferHistory = (# 🚧
            """
            query GetItemTransferHistory(
                $itemAlias: String!,
                $itemId: Int!,
                $from: Int!,
                $size: Int!
            )
            {
                item(
                    itemAlias: $itemAlias,
                    itemId: $itemId
                )
                {
                    tokenId
                    transferHistory(
                        from: $from,
                        size: $size
                    )
                    {
                        ...TransferRecords
                        __typename
                    }
                    __typename
                }
            }
            """
            + ValidFragments.TransferRecords
        )
    #╚═════════════════════════════════════════════════════════════════════════╝
#╚═════════════════════════════════════════════════════════════════════════════╝
