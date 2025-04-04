summary_query = f""" 
        WITH transactionsys AS (
                SELECT
                    t.amount,
                    t."userId"
                FROM transactions t
                WHERE t."userId" = %s
            ),
            budgetsys AS (
                SELECT
                    b.spent,
                    b.maximum,
                    b."userId"
                FROM budgets b
                WHERE b."userId" = %s
            ),
            potsys AS (
                SELECT
                    p.total,
                    p."userId"
                FROM pots p
                WHERE p."userId" = %s
            ),
            summary AS (
                SELECT
                    u.income AS income,
                    u.expenses AS expenses,
                    u.balance AS balance,
                    u.id AS id,
                    (SELECT SUM(p.total) FROM potsys p WHERE p."userId" = u.id) AS total_saved,
                    (SELECT SUM(b.maximum) FROM budgetsys b WHERE b."userId" = u.id) AS total_limits
                FROM "user" u
                WHERE u.id = %s
            ),
            limited_transactions AS (
                SELECT
                    t.name,
                    t.amount,
                    t.date,
                    t.avatar,
                    t."userId",
                    ROW_NUMBER() OVER (ORDER BY t.date DESC) AS rn
                FROM transactions t
                WHERE t."userId" = %s
            ),
            limited_budgets AS (
                SELECT
                    b.category,
                    b.theme,
                    b.spent,
                    b.maximum,
                    b."userId",
                    ROW_NUMBER() OVER (ORDER BY b.category) AS rn
                FROM budgets b
                WHERE b."userId" = %s
            ),
            limited_pots AS (
                SELECT
                    p.name,
                    p.target,
                    p.total,
                    p.theme,
                    p."userId",
                    ROW_NUMBER() OVER (ORDER BY p.name) AS rn
                FROM pots p
                WHERE p."userId" = %s
            ),
            limited_bills AS (
                SELECT
                    bi.due_day,
                    bi.amount,
                    bi.avatar,
                    bi.name,
                    bi."userId"
                FROM bills bi
                WHERE bi."userId" = %s
            )
        SELECT
            s.balance,
            s.expenses,
            s.income,
            s.total_saved,
            s.total_limits,
            (SELECT json_agg(
                json_build_object(
                    'name', lt.name,
                    'amount', lt.amount,
                    'date', lt.date,
                    'avatar', lt.avatar
                )
            )
            FROM limited_transactions lt
            WHERE lt."userId" = s.id AND lt.rn <= 5) AS transactions,
            
            (SELECT json_agg(
                json_build_object(
                    'category', lb.category,
                    'theme', lb.theme,
                    'spent', lb.spent,
                    'maximum', lb.maximum
                )
            )
            FROM limited_budgets lb
            WHERE lb."userId" = s.id AND lb.rn <= 4) AS budgets,

            (SELECT json_agg(
                json_build_object(
                    'name', lp.name,
                    'target', lp.target,
                    'total', lp.total,
                    'theme', lp.theme
                )
            )
            FROM limited_pots lp
            WHERE lp."userId" = s.id AND lp.rn <= 4) AS pots,

            (SELECT json_agg(
                json_build_object(
                    'due_day', lb.due_day,
                    'amount', lb.amount,
                    'avatar', lb.avatar,
                    'name', lb.name
                )
            )
            FROM limited_bills lb
            WHERE lb."userId" = s.id) AS bills
        FROM summary s 
    """