class InsufficientStock(Exception):
    """La quantité commandée dépasse le stock disponible."""

    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Stock insuffisant pour le produit {product_id} : "
            f"demandé {requested}, disponible {available}"
        )


def allocate(product_id: int, stocks: list[tuple[int, int]], requested: int) -> list[tuple[int, int]]:
    """Répartit `requested` sur les stocks [(user_id, quantité)].

    Renvoie [(user_id, quantité à retirer)]. Lève InsufficientStock si
    la quantité demandée dépasse le stock total (règle : commande > stock -> refus).
    """
    available = sum(q for _, q in stocks)
    if requested > available:
        raise InsufficientStock(product_id, requested, available)

    to_take = []
    remaining = requested
    for user_id, quantity in stocks:
        if remaining == 0:
            break
        taken = min(quantity, remaining)
        if taken > 0:
            to_take.append((user_id, taken))
            remaining -= taken
    return to_take
