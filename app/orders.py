from app.stock import allocate


def place_order(conn, user_id: int, items: list[tuple[int, int]]) -> int:
    """Crée la commande et décrémente le stock, dans la transaction de `conn`.

    Si un produit manque de stock, InsufficientStock est levée : la transaction
    est annulée par l'appelant, donc rien n'est écrit (ni commande, ni stock).
    """
    # Un même produit ne peut apparaître qu'une fois (clé primaire order_items).
    totals: dict[int, int] = {}
    for product_id, quantity in items:
        totals[product_id] = totals.get(product_id, 0) + quantity

    order_id = conn.execute(
        "INSERT INTO orders(user_id) VALUES (%s) RETURNING id", (user_id,)
    ).fetchone()[0]

    # Produits triés pour verrouiller toujours dans le même ordre (évite les blocages).
    for product_id in sorted(totals):
        quantity = totals[product_id]
        # FOR UPDATE : deux commandes simultanées ne peuvent pas dépasser le stock.
        stocks = conn.execute(
            "SELECT user_id, quantity FROM user_stocks "
            "WHERE product_id = %s AND quantity > 0 ORDER BY user_id FOR UPDATE",
            (product_id,),
        ).fetchall()

        for stock_user_id, taken in allocate(product_id, stocks, quantity):
            conn.execute(
                "UPDATE user_stocks SET quantity = quantity - %s "
                "WHERE user_id = %s AND product_id = %s",
                (taken, stock_user_id, product_id),
            )
        conn.execute(
            "INSERT INTO order_items(order_id, product_id, quantity) VALUES (%s, %s, %s)",
            (order_id, product_id, quantity),
        )
    return order_id
